import React, { useState, useEffect, useRef } from 'react';
import { DISCOVERY_DOMAINS, DISCOVERY_SSL, DISCOVERY_IPS, GRAPH_NODES, GRAPH_EDGES, getScoreColor } from '../mockData';
import DiscoveryControls from '../components/AssetDiscovery/DiscoveryControls';
import DiscoveryResults from '../components/AssetDiscovery/DiscoveryResults';

const TABS = ['Live Queue', 'Domains', 'SSL', 'IP Address/Subnets', 'Software'];
const DOMAIN_FILTERS = ['All', 'New', 'Confirmed', 'False Positive'];

export default function AssetDiscovery() {
  const [tab, setTab] = useState('Live Queue');
  const [filter, setFilter] = useState('All');
  const [view, setView] = useState('table');
  const canvasRef = useRef(null);

  const [liveQueue, setLiveQueue] = useState([]);

  const loadQueue = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/discovery/results');
      const data = await res.json();
      setLiveQueue(data || []);
    } catch (e) {
      console.error(e);
      setLiveQueue([
        { id: 1, first_seen: new Date().toISOString(), hostname: 'vpn.pnb.co.in', source: 'DNS', ip_address: '10.0.0.10', status: 'PENDING' },
        { id: 2, first_seen: new Date().toISOString(), hostname: 'dev.pnb.co.in', source: 'CT_LOG', ip_address: '10.0.0.11', status: 'CONFIRMED' },
      ]);
    }
  };

  useEffect(() => {
    loadQueue();
  }, []);

  const handleStartScan = async (scope, options) => {
    try {
      await fetch('http://127.0.0.1:8000/api/discovery/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scope, options })
      });
      alert(`Discovery started for scope: ${scope}`);
      setTimeout(loadQueue, 2000);
    } catch (e) {
      console.error(e);
    }
  };

  const handleQueueAction = async (action, id) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/discovery/${action}/${id}`, { method: 'POST' });
      loadQueue();
    } catch (e) {
      console.error(e);
    }
  };

  // Network graph rendering
  useEffect(() => {
    if (view !== 'graph' || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const W = canvas.parentElement.offsetWidth, H = 520;
    canvas.width = W; canvas.height = H;

    // Draw
    ctx.clearRect(0, 0, W, H);

    // Edges
    GRAPH_EDGES.forEach(e => {
      const s = GRAPH_NODES.find(n => n.id === e.source);
      const t = GRAPH_NODES.find(n => n.id === e.target);
      if (!s || !t) return;
      ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(t.x, t.y);
      ctx.strokeStyle = 'rgba(34,197,94,0.25)'; ctx.lineWidth = 1; ctx.stroke();
    });

    // Nodes
    GRAPH_NODES.forEach(n => {
      const r = 16;
      const c = getScoreColor(n.score);
      ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = '#0f1629'; ctx.fill();
      ctx.strokeStyle = c; ctx.lineWidth = 2; ctx.stroke();
      // Icon
      const icons = { 'Web Application': 'WEB', 'API Endpoint': 'API', 'Server': 'SRV', 'VPN Gateway': 'VPN',
        'Email Server': 'MAIL', 'Payment Gateway': 'PAY', 'Banking Core': 'CORE', 'CDN': 'CDN',
        'Load Balancer': 'LB', 'Database': 'DB', 'Microservice': 'μS', 'Mobile API': 'MOB' };
      ctx.fillStyle = c; ctx.font = 'bold 7px Inter'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(icons[n.type] || 'SRV', n.x, n.y);
      ctx.fillStyle = '#94a3b8'; ctx.font = '8px Inter';
      ctx.fillText(n.label, n.x, n.y + r + 10);
    });
  }, [view]);

  const filteredDomains = filter === 'All' ? DISCOVERY_DOMAINS :
    filter === 'New' ? DISCOVERY_DOMAINS.filter(d => d.status === 'new') :
    filter === 'Confirmed' ? DISCOVERY_DOMAINS.filter(d => d.status === 'confirmed') :
    DISCOVERY_DOMAINS.filter(d => d.status === 'false_positive');

  const counts = { 'Live Queue': liveQueue.length, Domains: DISCOVERY_DOMAINS.length, SSL: DISCOVERY_SSL.length, 'IP Address/Subnets': DISCOVERY_IPS.length, Software: 52 };
  const filterCounts = {
    All: DISCOVERY_DOMAINS.length,
    New: DISCOVERY_DOMAINS.filter(d => d.status === 'new').length,
    Confirmed: DISCOVERY_DOMAINS.filter(d => d.status === 'confirmed').length,
    'False Positive': DISCOVERY_DOMAINS.filter(d => d.status === 'false_positive').length,
  };

  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div><h1 className="page-title">Asset Discovery</h1><p className="page-subtitle">CT log monitoring, DNS reconnaissance, and OSINT-powered asset discovery</p></div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className={`btn ${view === 'table' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setView('table')}>📋 Table</button>
          <button className={`btn ${view === 'graph' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setView('graph')}>🕸️ Graph</button>
        </div>
      </div>

      <DiscoveryControls onStartScan={handleStartScan} />

      {view === 'table' ? (
        <>
          {/* Top tabs */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            {TABS.map(t => (
              <button key={t} className={`btn ${tab === t ? 'btn-primary' : 'btn-outline'}`} onClick={() => setTab(t)} style={{ fontSize: '0.85rem', padding: '6px 14px' }}>
                {t} ({counts[t]})
              </button>
            ))}
          </div>

          {/* Sub-filters */}
          {tab === 'Domains' && (
            <div style={{ display: 'flex', gap: 6, marginBottom: 16 }}>
              {DOMAIN_FILTERS.map(f => (
                <button key={f} className={`btn ${filter === f ? 'btn-primary' : 'btn-outline'}`} onClick={() => setFilter(f)} style={{ fontSize: '0.78rem', padding: '4px 12px' }}>
                  {f} ({filterCounts[f]})
                </button>
              ))}
            </div>
          )}

          <div className="data-table-wrapper">
            {tab === 'Live Queue' && (
              <DiscoveryResults results={liveQueue} onAction={handleQueueAction} />
            )}
            {tab === 'Domains' && (
              <table className="data-table">
                <thead><tr><th>Detection Date</th><th>Domain Name</th><th>Registration Date</th><th>Registrar</th><th>Company</th><th>Status</th></tr></thead>
                <tbody>
                  {filteredDomains.map((d, i) => (
                    <tr key={i}>
                      <td>{d.date}</td>
                      <td className="domain">{d.domain}</td>
                      <td>{d.regDate}</td>
                      <td style={{ fontSize: '0.78rem' }}>{d.registrar}</td>
                      <td>{d.company}</td>
                      <td><span className={`score-badge ${d.status === 'confirmed' ? 'safe' : d.status === 'new' ? 'moderate' : 'high'}`}>{d.status.replace('_', ' ')}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {tab === 'SSL' && (
              <table className="data-table">
                <thead><tr><th>Domain</th><th>Issuer</th><th>Valid From</th><th>Valid Until</th><th>Key Type</th><th>SANs</th></tr></thead>
                <tbody>
                  {DISCOVERY_SSL.map((s, i) => (
                    <tr key={i}>
                      <td className="domain">{s.domain}</td>
                      <td>{s.issuer}</td>
                      <td>{s.validFrom}</td>
                      <td>{s.validUntil}</td>
                      <td style={{ fontWeight: s.keyType.includes('ML-') ? 600 : 400, color: s.keyType.includes('ML-') ? '#22c55e' : 'var(--text-secondary)' }}>{s.keyType}</td>
                      <td>{s.sans}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {tab === 'IP Address/Subnets' && (
              <table className="data-table">
                <thead><tr><th>IP Address</th><th>Subnet</th><th>Type</th><th>Open Ports</th><th>OS</th><th>Last Seen</th></tr></thead>
                <tbody>
                  {DISCOVERY_IPS.slice(0, 15).map((ip, i) => (
                    <tr key={i}>
                      <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{ip.ip}</td>
                      <td>{ip.subnet}</td>
                      <td>{ip.type}</td>
                      <td style={{ fontSize: '0.78rem' }}>{ip.ports.join(', ')}</td>
                      <td>{ip.os}</td>
                      <td>{ip.lastSeen}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {tab === 'Software' && (
              <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
                <div style={{ fontSize: '2rem', marginBottom: 12 }}>📦</div>
                <p>52 software components detected across infrastructure</p>
                <p style={{ fontSize: '0.78rem', marginTop: 8 }}>OpenSSL 1.1.1 (23) · OpenSSL 3.x (14) · liboqs (3) · Java Crypto (8) · .NET Crypto (4)</p>
              </div>
            )}
          </div>
        </>
      ) : (
        <div className="card">
          <div className="card-header"><span className="card-title">Network Topology — Asset Dependency Graph</span></div>
          <div className="graph-container" style={{ height: 520 }}>
            <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
          </div>
          <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginTop: 8 }}>
            {[{l:'Web',c:'#6366f1'},{l:'API',c:'#06b6d4'},{l:'Payment',c:'#eab308'},{l:'Core',c:'#22c55e'},{l:'Infrastructure',c:'#f97316'}].map(x=>(
              <span key={x.l} style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                <span style={{ width: 10, height: 10, borderRadius: '50%', background: x.c, display: 'inline-block' }}/>{x.l}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
