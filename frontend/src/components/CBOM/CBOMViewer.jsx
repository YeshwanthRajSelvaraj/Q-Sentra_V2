import React, { useState, useEffect } from 'react';
import { ShieldAlert, RefreshCw, Key, Lock, Download, FileCode } from 'lucide-react';
import CertificateChain from './CertificateChain';

export default function CBOMViewer({ hostname }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchCBOM = async (forceRefresh = false) => {
    try {
      const endpoint = forceRefresh 
        ? `/api/cbom/refresh/${hostname}` 
        : `/api/cbom/${hostname}`;
      
      const method = forceRefresh ? 'POST' : 'GET';
      const response = await fetch(`http://127.0.0.1:8000${endpoint}`, { method });
      const json = await response.json();
      setData(json);
    } catch (error) {
      console.error("Failed to load CBOM:", error);
      // Fallback for presentation purposes if backend is unavailable
      setData({ error: "Backend server unavailable. Please ensure Q-Sentra API is running." });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (hostname) {
      setLoading(true);
      fetchCBOM();
    }
  }, [hostname]);

  if (!hostname) {
    return (
      <div className="card" style={{ padding: '40px', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Select an asset from the inventory to view its CBOM.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="card" style={{ padding: '60px', textAlign: 'center' }}>
        <RefreshCw className="spin" size={32} style={{ color: 'var(--accent-primary)', marginBottom: 16 }} />
        <p>Scanning and generating CBOM for {hostname}...</p>
      </div>
    );
  }

  if (!data || data.error) {
    return (
      <div className="card" style={{ padding: '40px', textAlign: 'center', borderColor: 'var(--danger)' }}>
        <ShieldAlert size={48} style={{ color: 'var(--danger)', marginBottom: 16 }} />
        <h3 style={{ color: 'var(--danger)' }}>Scan Failed</h3>
        <p>{data?.error || "Could not retrieve CBOM data."}</p>
        <button 
           className="btn btn-outline" 
           onClick={() => { setLoading(true); fetchCBOM(true); }}
           style={{ marginTop: 16 }}
        >
           Retry Scan
        </button>
      </div>
    );
  }

  return (
    <div className="cbom-viewer">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 12 }}>
            <ShieldAlert size={24} style={{ color: 'var(--accent-secondary)' }} />
            {data.hostname}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', margin: '4px 0 0 0' }}>
            Last scan: {new Date(data.scan_timestamp).toLocaleString()}
          </p>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
           <button 
             className="btn btn-outline" 
             onClick={() => { setRefreshing(true); fetchCBOM(true); }}
             disabled={refreshing}
           >
             <RefreshCw size={14} className={refreshing ? 'spin' : ''} /> Rescan
           </button>
           <button className="btn btn-primary">
             <Download size={14} /> Download JSON
           </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
        <div className="card">
          <div className="card-header"><span className="card-title">TLS Configuration</span></div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: 8 }}>
              <span style={{ color: 'var(--text-muted)' }}>TLS Version</span>
              <span style={{ fontWeight: 600, color: 'var(--accent-primary)' }}>{data.tls_version}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: 8 }}>
              <span style={{ color: 'var(--text-muted)' }}>Cipher Suite</span>
              <span style={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>{data.cipher_suite}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: 8 }}>
              <span style={{ color: 'var(--text-muted)' }}>Key Exchange Mechanism</span>
              <span>{data.key_exchange?.mechanism}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Elliptic Curve</span>
              <span>{data.key_exchange?.curve}</span>
            </div>
          </div>
        </div>
        
        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ textAlign: 'center' }}>
             <Lock size={48} style={{ color: data.tls_version === 'TLSv1.3' ? 'var(--success)' : 'var(--warning)', margin: '0 auto 16px' }} />
             <h3 style={{ margin: '0 0 8px 0' }}>Protocol Status</h3>
             <p style={{ color: 'var(--text-muted)' }}>
               {data.tls_version === 'TLSv1.3' 
                 ? "Modern TLS is enabled, providing forward secrecy and strong ciphers."
                 : "Legacy TLS version detected. Upgrade to TLS 1.3 recommended for robust security."}
             </p>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-header"><span className="card-title">Certificate Chain</span></div>
        <CertificateChain chain={data.certificate_chain} />
      </div>

      <div className="card">
         <div className="card-header"><span className="card-title">Raw CBOM Data</span></div>
         <div style={{ background: '#0a0f1d', padding: 16, borderRadius: 8, overflowX: 'auto', fontFamily: 'monospace', fontSize: '0.8rem', color: '#6366f1' }}>
           <pre>{JSON.stringify(data, null, 2)}</pre>
         </div>
      </div>
    </div>
  );
}
