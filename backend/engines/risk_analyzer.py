"""
Q-Sentra AI Risk Analysis Engine
Uses NetworkX for dependency graph analysis and blast radius computation.
Simulates GNN-based risk scoring with graph-theoretic metrics.

Features:
  - Dependency graph construction from asset scan data
  - Blast radius calculation (how many assets impacted by one compromise)
  - Centrality-based risk scoring
  - Attack path identification
  - Community detection for risk clustering
"""
import logging
import hashlib
import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timezone

import networkx as nx

logger = logging.getLogger("qsentra.risk")


class RiskAnalyzer:
    """AI-powered risk analysis using graph-theoretic methods."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self._risk_weights = {
            "shared_certificate": 0.8,
            "same_subnet": 0.6,
            "api_dependency": 0.9,
            "dns_dependency": 0.5,
            "load_balanced": 0.7,
            "database_backend": 0.95,
        }

    def build_graph(self, assets: List[Dict], scan_results: Dict[str, Dict] = None) -> nx.DiGraph:
        """
        Build a dependency graph from discovered assets and scan results.

        Nodes: individual assets (domains/IPs)
        Edges: dependencies identified from:
          - Shared certificates (same issuer/SAN)
          - Same subnet (IP proximity)
          - Naming conventions (api.*, cdn.*, etc.)
          - Service dependencies (netbanking -> api -> db)
        """
        self.graph.clear()

        # ── Add Nodes ──
        for asset in assets:
            domain = asset.get("domain", "") or ""
            if not domain:
                continue
            scan = (scan_results or {}).get(domain, {})
            score = scan.get("quantum_score", 50)
            self.graph.add_node(domain, **{
                "ip": asset.get("ip", "") or "",
                "port": asset.get("port", 443),
                "quantum_score": score,
                "asset_type": self._classify_asset(domain),
                "risk_level": self._score_to_risk(score),
                "vulnerabilities": len(scan.get("vulnerabilities", [])),
            })

        # ── Add Edges (dependency inference) ──
        domains = [a.get("domain", "") for a in assets]
        for i, src in enumerate(domains):
            for j, dst in enumerate(domains):
                if i == j:
                    continue

                edge_type, weight = self._infer_dependency(src, dst, assets[i], assets[j], scan_results)
                if edge_type:
                    self.graph.add_edge(src, dst,
                                       dependency_type=edge_type,
                                       weight=weight)

        logger.info(f"Built graph: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        return self.graph

    def analyze_risk(self, target_asset: str = None) -> Dict:
        """
        Perform comprehensive risk analysis on the built graph.

        Returns:
            - blast_radius: for specific asset or top risky assets
            - risk_scores: centrality-based risk for all nodes
            - attack_paths: critical attack paths
            - communities: risk clusters
        """
        if self.graph.number_of_nodes() == 0:
            return {"error": "No graph data. Call build_graph() first."}

        results = {
            "graph_stats": self._graph_statistics(),
            "risk_scores": self._compute_risk_scores(),
            "communities": self._detect_communities(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if target_asset and target_asset in self.graph:
            results["blast_radius"] = self._compute_blast_radius(target_asset)
            results["attack_paths"] = self._find_attack_paths(target_asset)
        else:
            # Compute for top 5 riskiest nodes
            risk_scores = results["risk_scores"]
            top_risky = sorted(risk_scores.items(), key=lambda x: x[1]["composite_risk"], reverse=True)[:5]
            results["top_risks"] = [{
                "asset": node,
                "composite_risk": data["composite_risk"],
                "blast_radius": self._compute_blast_radius(node),
            } for node, data in top_risky]

        return results

    def _compute_blast_radius(self, target: str) -> Dict:
        """
        Calculate blast radius: how many assets are impacted if target is compromised.
        Uses BFS/DFS traversal with weighted propagation.
        """
        if target not in self.graph:
            return {"target": target, "blast_radius": 0, "impacted_assets": []}

        # Forward propagation (what does this asset affect)
        downstream = set()
        visited = set()
        queue = [(target, 1.0)]  # (node, propagation_strength)

        while queue:
            node, strength = queue.pop(0)
            if node in visited or strength < 0.1:
                continue
            visited.add(node)
            if node != target:
                downstream.add((node, strength))

            for neighbor in self.graph.successors(node):
                edge_data = self.graph.edges[node, neighbor]
                new_strength = strength * edge_data.get("weight", 0.5)
                queue.append((neighbor, new_strength))

        # Reverse propagation (what can compromise this asset)
        upstream = set()
        visited = set()
        queue = [(target, 1.0)]

        while queue:
            node, strength = queue.pop(0)
            if node in visited or strength < 0.1:
                continue
            visited.add(node)
            if node != target:
                upstream.add((node, strength))

            for neighbor in self.graph.predecessors(node):
                edge_data = self.graph.edges[neighbor, node]
                new_strength = strength * edge_data.get("weight", 0.5)
                queue.append((neighbor, new_strength))

        total_nodes = self.graph.number_of_nodes()
        blast_score = min(100, round(len(downstream) / max(1, total_nodes - 1) * 100, 1))

        return {
            "target": target,
            "blast_radius_score": blast_score,
            "downstream_impact": len(downstream),
            "upstream_exposure": len(upstream),
            "impacted_assets": [
                {"asset": node, "impact_strength": round(s, 2)}
                for node, s in sorted(downstream, key=lambda x: -x[1])
            ],
            "exposure_sources": [
                {"asset": node, "exposure_strength": round(s, 2)}
                for node, s in sorted(upstream, key=lambda x: -x[1])
            ],
            "total_assets": total_nodes,
        }

    def _compute_risk_scores(self) -> Dict:
        """
        Compute composite risk scores using multiple graph centrality measures.
        Simulates GNN node-level feature aggregation.
        """
        scores = {}

        # Centrality measures
        undirected = self.graph.to_undirected()
        degree_centrality = nx.degree_centrality(undirected)
        try:
            betweenness = nx.betweenness_centrality(undirected, weight="weight")
        except Exception:
            betweenness = {n: 0 for n in self.graph.nodes}
        try:
            closeness = nx.closeness_centrality(undirected)
        except Exception:
            closeness = {n: 0 for n in self.graph.nodes}

        pagerank = nx.pagerank(self.graph, weight="weight", max_iter=100) if self.graph.number_of_edges() > 0 else {n: 0 for n in self.graph.nodes}

        for node in self.graph.nodes:
            node_data = self.graph.nodes[node]
            qs = node_data.get("quantum_score", 50)
            vuln_count = node_data.get("vulnerabilities", 0)

            # Composite risk: weighted combination of centrality + vulnerability indicators
            composite = (
                0.25 * degree_centrality.get(node, 0) * 100 +
                0.20 * betweenness.get(node, 0) * 100 +
                0.15 * closeness.get(node, 0) * 100 +
                0.15 * pagerank.get(node, 0) * 1000 +
                0.15 * (100 - qs) +  # Inverse quantum score = vulnerability
                0.10 * min(100, vuln_count * 20)
            )

            scores[node] = {
                "degree_centrality": round(degree_centrality.get(node, 0), 4),
                "betweenness_centrality": round(betweenness.get(node, 0), 4),
                "closeness_centrality": round(closeness.get(node, 0), 4),
                "pagerank": round(pagerank.get(node, 0), 6),
                "quantum_score": qs,
                "vulnerability_count": vuln_count,
                "composite_risk": round(composite, 1),
                "risk_level": self._risk_level(composite),
            }

        return scores

    def _detect_communities(self) -> List[Dict]:
        """Detect risk communities/clusters using graph partitioning."""
        undirected = self.graph.to_undirected()
        if undirected.number_of_edges() == 0:
            return [{"id": 0, "assets": list(self.graph.nodes), "avg_risk": 50}]

        try:
            communities = list(nx.community.greedy_modularity_communities(undirected))
        except Exception:
            communities = [set(self.graph.nodes)]

        result = []
        for i, community in enumerate(communities):
            assets = list(community)
            avg_score = sum(self.graph.nodes[n].get("quantum_score", 50) for n in assets) / max(1, len(assets))
            result.append({
                "id": i,
                "size": len(assets),
                "assets": assets,
                "avg_quantum_score": round(avg_score, 1),
                "risk_level": self._score_to_risk(avg_score),
            })

        return result

    def _find_attack_paths(self, target: str) -> List[Dict]:
        """Find potential attack paths to/from a target asset."""
        paths = []

        # Find paths from vulnerable entry points to target
        for node in self.graph.nodes:
            if node == target:
                continue
            node_data = self.graph.nodes[node]
            if node_data.get("quantum_score", 50) < 40:  # Vulnerable entry point
                try:
                    path = nx.shortest_path(self.graph, node, target)
                    if len(path) > 1:
                        path_risk = sum(
                            100 - self.graph.nodes[n].get("quantum_score", 50)
                            for n in path
                        ) / len(path)
                        paths.append({
                            "source": node,
                            "target": target,
                            "path": path,
                            "hops": len(path) - 1,
                            "avg_vulnerability": round(path_risk, 1),
                            "attack_type": "HNDL" if "vpn" in (node or "").lower() or "api" in (node or "").lower() else "direct",
                        })
                except nx.NetworkXNoPath:
                    pass

        return sorted(paths, key=lambda p: -p["avg_vulnerability"])[:10]

    def _graph_statistics(self) -> Dict:
        """Compute overall graph statistics."""
        undirected = self.graph.to_undirected()
        stats = {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "density": round(nx.density(self.graph), 4),
            "avg_degree": round(sum(d for _, d in undirected.degree()) / max(1, self.graph.number_of_nodes()), 2),
        }

        try:
            if nx.is_connected(undirected):
                stats["diameter"] = nx.diameter(undirected)
                stats["avg_shortest_path"] = round(nx.average_shortest_path_length(undirected), 2)
            else:
                largest_cc = max(nx.connected_components(undirected), key=len)
                subgraph = undirected.subgraph(largest_cc)
                stats["diameter"] = nx.diameter(subgraph)
                stats["connected_components"] = nx.number_connected_components(undirected)
        except Exception:
            stats["diameter"] = -1

        return stats

    def _infer_dependency(self, src: str, dst: str, src_data: dict, dst_data: dict, scans: dict = None) -> Tuple[Optional[str], float]:
        """Infer dependency type between two assets."""
        src_parts = src.split(".")
        dst_parts = dst.split(".")

        # Same base domain → related
        if src_parts[-2:] == dst_parts[-2:]:
            src_prefix = src_parts[0] if len(src_parts) > 2 else ""
            dst_prefix = dst_parts[0] if len(dst_parts) > 2 else ""

            # API dependencies
            if "api" in dst_prefix and ("www" in src_prefix or "netbanking" in src_prefix or "mobile" in src_prefix):
                return "api_dependency", 0.9
            if "api" in src_prefix and ("db" in dst_prefix or "mongo" in dst_prefix):
                return "database_backend", 0.95

            # Load balancer
            if "cdn" in src_prefix or "lb" in src_prefix:
                return "load_balanced", 0.7

            # DNS / same IP
            src_ip = src_data.get("ip") or ""
            dst_ip = dst_data.get("ip") or ""
            if src_ip and dst_ip and src_ip == dst_ip:
                return "same_subnet", 0.6

            # Same certificate (shared infrastructure)
            if scans:
                src_scan = scans.get(src, {})
                dst_scan = scans.get(dst, {})
                src_issuer = src_scan.get("certificate", {}).get("issuer", {})
                dst_issuer = dst_scan.get("certificate", {}).get("issuer", {})
                if src_issuer and src_issuer == dst_issuer:
                    return "shared_certificate", 0.5

            # Generic same-domain dependency
            return "dns_dependency", 0.3

        return None, 0.0

    def _classify_asset(self, domain: str) -> str:
        """Classify asset type from domain name."""
        if not domain:
            return "Server"
        prefix = domain.split(".")[0].lower()
        type_map = {
            "www": "Web Application", "api": "API Endpoint", "mail": "Email Server",
            "vpn": "VPN Gateway", "cdn": "CDN", "mobile": "Mobile API",
            "netbanking": "Internet Banking", "upi": "UPI Gateway",
            "swift": "SWIFT Gateway", "neft": "NEFT Gateway",
            "imps": "IMPS Gateway", "treasury": "Treasury System",
            "portal": "Web Portal", "admin": "Admin Panel",
        }
        return type_map.get(prefix, "Server")

    def _score_to_risk(self, score: float) -> str:
        if score >= 90: return "minimal"
        if score >= 70: return "low"
        if score >= 50: return "medium"
        if score >= 30: return "high"
        return "critical"

    def _risk_level(self, composite: float) -> str:
        if composite >= 70: return "critical"
        if composite >= 50: return "high"
        if composite >= 30: return "medium"
        return "low"

    def get_graph_json(self) -> Dict:
        """Export graph as JSON for D3.js/Cytoscape frontend rendering."""
        nodes = []
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": node.split(".")[0],
                "type": data.get("asset_type", "Unknown"),
                "quantum_score": data.get("quantum_score", 50),
                "risk_level": data.get("risk_level", "medium"),
            })

        edges = []
        for src, dst, data in self.graph.edges(data=True):
            edges.append({
                "source": src,
                "target": dst,
                "type": data.get("dependency_type", "unknown"),
                "weight": data.get("weight", 0.5),
            })

        return {"nodes": nodes, "edges": edges}
