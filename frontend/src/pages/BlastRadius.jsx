import React, { useEffect, useRef, useState } from 'react';
import { GRAPH_NODES, GRAPH_EDGES, getScoreColor } from '../mockData';

export default function BlastRadius() {
  const canvasRef = useRef(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [showHndl, setShowHndl] = useState(false);
  const positionsRef = useRef({});

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width; canvas.height = 520;
    const W = canvas.width, H = canvas.height;
    const cX = W / 2, cY = H / 2;

    // Position nodes in concentric circles
    const positions = {};
    const inner = GRAPH_NODES.filter(n => n.score >= 60);
    const outer = GRAPH_NODES.filter(n => n.score < 60);

    inner.forEach((n, i) => {
      const a = (2 * Math.PI * i / inner.length) - Math.PI / 2;
      positions[n.id] = { ...n, x: cX + 120 * Math.cos(a), y: cY + 100 * Math.sin(a) };
    });
    outer.forEach((n, i) => {
      const a = (2 * Math.PI * i / outer.length) - Math.PI / 2;
      positions[n.id] = { ...n, x: cX + 220 * Math.cos(a), y: cY + 180 * Math.sin(a) };
    });
    positionsRef.current = positions;

    ctx.clearRect(0, 0, W, H);

    // Edges
    GRAPH_EDGES.forEach(e => {
      const s = positions[e.source], t = positions[e.target];
      if (!s || !t) return;
      const isHndl = showHndl && (s.score < 60 || t.score < 60);
      ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(t.x, t.y);
      ctx.strokeStyle = isHndl ? 'rgba(239,68,68,0.45)' : 'rgba(99,102,241,0.12)';
      ctx.lineWidth = isHndl ? 2 : 1; ctx.stroke();
      // Arrow
      const dx = t.x - s.x, dy = t.y - s.y, len = Math.sqrt(dx*dx + dy*dy);
      if (len === 0) return;
      const nx = dx/len, ny = dy/len;
      const ax = t.x - nx * 20, ay = t.y - ny * 20;
      ctx.beginPath(); ctx.moveTo(ax, ay);
      ctx.lineTo(ax - nx*7 + ny*3, ay - ny*7 - nx*3);
      ctx.lineTo(ax - nx*7 - ny*3, ay - ny*7 + nx*3);
      ctx.closePath(); ctx.fillStyle = isHndl ? 'rgba(239,68,68,0.4)' : 'rgba(99,102,241,0.15)'; ctx.fill();
    });

    // Nodes
    Object.values(positions).forEach(n => {
      const r = 16; const c = getScoreColor(n.score);
      // Glow
      const g = ctx.createRadialGradient(n.x, n.y, r*0.3, n.x, n.y, r*2.5);
      g.addColorStop(0, c + '15'); g.addColorStop(1, 'transparent');
      ctx.beginPath(); ctx.arc(n.x, n.y, r*2.5, 0, Math.PI*2); ctx.fillStyle = g; ctx.fill();
      // Circle
      ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI*2); ctx.fillStyle = '#0f1629'; ctx.fill();
      ctx.strokeStyle = c; ctx.lineWidth = 2; ctx.stroke();
      // Score
      ctx.fillStyle = c; ctx.font = 'bold 10px Inter'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(n.score, n.x, n.y);
      // Label
      ctx.fillStyle = '#94a3b8'; ctx.font = '8px Inter'; ctx.fillText(n.label, n.x, n.y + r + 12);
    });

    const handleClick = (e) => {
      const br = canvas.getBoundingClientRect();
      const mx = e.clientX - br.left, my = e.clientY - br.top;
      const clicked = Object.values(positionsRef.current).find(n => Math.sqrt((n.x-mx)**2 + (n.y-my)**2) <= 18);
      setSelectedNode(clicked || null);
    };
    canvas.addEventListener('click', handleClick);
    return () => canvas.removeEventListener('click', handleClick);
  }, [showHndl]);

  const hndlData = {
    'www.pnb.co.in': { risk: 96.4, liability: '₹500 Cr', vector: 'RSA key harvest → Session decryption', years: 3.2 },
    'netbanking.pnb.co.in': { risk: 101.8, liability: '₹2,500 Cr', vector: 'RSA-2048 KEX harvest → Account exposure', years: 2.8 },
    'api.pnb.co.in': { risk: 62.9, liability: '₹800 Cr', vector: 'X25519 KEX → Post-quantum recovery required', years: 5.1 },
    'vpn.pnb.co.in': { risk: 88.2, liability: '₹400 Cr', vector: 'RSA-4096 key harvest → VPN tunnel exposure', years: 4.5 },
    'upi.pnb.co.in': { risk: 72.1, liability: '₹1,200 Cr', vector: 'X25519 → UPI transaction interception post-CRQC', years: 5.0 },
    'swift.pnb.co.in': { risk: 0.7, liability: '₹50 Cr', vector: 'Low — ML-KEM-768 active, quantum-safe', years: 15 },
    'treasury.pnb.co.in': { risk: 1.2, liability: '₹80 Cr', vector: 'Low — ML-KEM-1024 active', years: 15 },
  };

  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div><h1 className="page-title">Blast Radius Visualizer</h1><p className="page-subtitle">Network topology with quantum vulnerability propagation and HNDL attack path analysis</p></div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className={`btn ${showHndl ? 'btn-primary' : 'btn-outline'}`} onClick={() => setShowHndl(!showHndl)}>
            {showHndl ? '🔴 HNDL Paths ON' : '⚪ Show HNDL Paths'}
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: selectedNode ? '1fr 320px' : '1fr', gap: 16 }}>
        <div className="card">
          <div className="graph-container" style={{ height: 520 }}><canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} /></div>
          <div style={{ display: 'flex', gap: 14, padding: '10px 0', justifyContent: 'center' }}>
            {[{l:'Safe (90+)',c:'#22c55e'},{l:'Moderate (60-89)',c:'#eab308'},{l:'High (30-59)',c:'#f97316'},{l:'Critical (0-29)',c:'#ef4444'}].map(x=>(
              <span key={x.l} style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                <span style={{ width: 10, height: 10, borderRadius: '50%', background: x.c, display: 'inline-block' }}/>{x.l}
              </span>
            ))}
          </div>
        </div>

        {selectedNode && (
          <div className="card fade-in">
            <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: 14, color: getScoreColor(selectedNode.score) }}>{selectedNode.label}</h3>
            {[['Asset ID', selectedNode.id],['Quantum Score', selectedNode.score],['Type', selectedNode.type]].map(([k,v])=>(
              <div className="cert-detail-row" key={k}><span className="label">{k}</span><span className="value">{v}</span></div>
            ))}
            {hndlData[selectedNode.id] && (
              <div style={{ marginTop: 14, padding: 12, background: hndlData[selectedNode.id].risk > 10 ? 'var(--score-critical-bg)' : 'var(--score-safe-bg)', borderRadius: 8, border: `1px solid ${hndlData[selectedNode.id].risk > 10 ? 'rgba(239,68,68,0.2)' : 'rgba(34,197,94,0.2)'}` }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: hndlData[selectedNode.id].risk > 10 ? '#ef4444' : '#22c55e', marginBottom: 6 }}>HNDL Risk Assessment</div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
                  Risk Score: <b>{hndlData[selectedNode.id].risk}</b><br/>
                  Liability: <b>{hndlData[selectedNode.id].liability}</b><br/>
                  Years to CRQC: <b>{hndlData[selectedNode.id].years}</b><br/>
                  Vector: {hndlData[selectedNode.id].vector}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
