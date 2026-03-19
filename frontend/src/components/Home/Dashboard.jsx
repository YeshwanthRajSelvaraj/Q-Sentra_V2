import React, { useState, useEffect } from 'react';
import { Search, Loader2 } from 'lucide-react';
import MetricsCards from './MetricsCards';
import Heatmap from './Heatmap';
import { dashboardService } from '../../services/dashboardService';
import { MOCK_ACTIVITY } from '../../mockData';

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [activities, setActivities] = useState(MOCK_ACTIVITY);
  const [searchTarget, setSearchTarget] = useState("");
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);

  useEffect(() => {
    dashboardService.getMetrics().then(m => {
      if (m) setMetrics(m);
    });
    dashboardService.getRecentActivity().then(act => {
      if (act && act.length > 0) setActivities(act);
    });
  }, []);

  const handleScan = async (e) => {
    e.preventDefault();
    if (!searchTarget) return;
    setScanning(true);
    setScanResult(null);
    try {
      const res = await dashboardService.scanOnDemand(searchTarget);
      setScanResult(res);
    } catch (err) {
      setScanResult({ error: err.message });
    }
    setScanning(false);
  };

  return (
    <div className="fade-in">
      <div className="page-title-bar" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
          <div>
            <h1 className="page-title">Enterprise Dashboard</h1>
            <p className="page-subtitle">Real-time oversight of cryptographic assets and quantum readiness</p>
          </div>
          
          {/* Quick Scan Bar */}
          <form onSubmit={handleScan} style={{ display: 'flex', width: '100%', maxWidth: 450, position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: 16, top: 13, color: 'var(--text-muted)' }} />
            <input 
              type="text" 
              placeholder="Scan a new domain or IP address..." 
              value={searchTarget}
              onChange={e => setSearchTarget(e.target.value)}
              style={{ width: '100%', padding: '12px 16px 12px 42px', borderRadius: 8, background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', color: 'white', fontSize: '0.9rem', outline: 'none' }} 
            />
            <button type="submit" disabled={scanning} className="btn btn-primary" style={{ position: 'absolute', right: 4, top: 4, padding: '8px 16px' }}>
              {scanning ? <><Loader2 size={16} className="spin" style={{marginRight: 6}} /> Scanning</> : 'Quick Scan'}
            </button>
          </form>
        </div>
        
        {scanResult && (
          <div style={{ marginTop: 0, padding: 16, background: 'var(--bg-elevated)', borderRadius: 8, width: '100%', borderLeft: '4px solid var(--accent-primary)' }}>
             <h4 style={{ margin: '0 0 8px 0', color: 'white' }}>Scan Results for {searchTarget}</h4>
             {scanResult.error ? (
               <p style={{ color: 'var(--danger)', margin: 0, fontSize: '0.9rem' }}>{scanResult.error}</p>
             ) : (
               <div style={{ fontSize: '0.9rem', display: 'flex', gap: 24, color: 'var(--text-secondary)' }}>
                 <div><b style={{color:'var(--text-primary)'}}>TLS:</b> {scanResult.tls_version || 'Unknown'}</div>
                 <div><b style={{color:'var(--text-primary)'}}>Cipher Suite:</b> <span style={{fontFamily:'monospace'}}>{scanResult.cipher_suite || 'Unknown'}</span></div>
                 <div><b style={{color:'var(--text-primary)'}}>PQC Ready:</b> {scanResult.quantum_score > 70 ? <span style={{color:'var(--success)'}}>Yes</span> : <span style={{color:'var(--warning)'}}>No</span>}</div>
               </div>
             )}
          </div>
        )}
      </div>

      <MetricsCards summary={metrics} />

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1.2fr)', gap: 24 }}>
        {/* Heatmap Area */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="card-header"><span className="card-title">Geographic Asset Distribution</span></div>
          <div style={{ padding: 16, flex: 1 }}>
             <Heatmap />
          </div>
        </div>

        {/* Activity Feed */}
        <div className="card" style={{ maxHeight: 480, overflowY: 'auto' }}>
          <div className="card-header" style={{ position: 'sticky', top: 0, zIndex: 10, background: 'var(--bg-card)' }}>
             <span className="card-title">Recent Activity</span>
          </div>
          <div className="activity-feed" style={{ padding: '0 16px 16px 16px' }}>
            {activities.slice(0,10).map((act, i) => (
              <div className="activity-item" key={act.id || i} style={{ padding: '12px 0', borderBottom: '1px solid var(--border-color)', display: 'flex', gap: 12 }}>
                <div className={`activity-dot ${act.severity || 'info'}`} style={{ marginTop: 6 }}/>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)', lineHeight: 1.4 }}>{act.message || act.description}</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 6 }}>{act.time || new Date(act.created_at).toLocaleString()}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
