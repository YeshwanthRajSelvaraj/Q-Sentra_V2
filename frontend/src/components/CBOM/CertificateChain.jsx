import React from 'react';
import { FileText, Key, CheckCircle, AlertTriangle } from 'lucide-react';

export default function CertificateChain({ chain }) {
  if (!chain || chain.length === 0) return <div>No certificate chain available.</div>;

  return (
    <div className="cert-chain">
      {chain.map((cert, index) => (
        <div key={index} className="cert-node" style={{
          marginLeft: `${index * 20}px`,
          padding: '16px',
          background: 'var(--bg-elevated)',
          borderLeft: '4px solid var(--accent-primary)',
          borderRadius: '8px',
          marginBottom: '16px',
          position: 'relative'
        }}>
          {index > 0 && <div style={{
             position: 'absolute', top: '-16px', left: '-12px', width: '2px', height: '16px', background: 'var(--border-color)'
          }} />}
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <FileText size={24} style={{ color: 'var(--accent-secondary)' }} />
              <div>
                <h4 style={{ margin: 0, color: 'var(--text-primary)' }}>{cert.subject}</h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>Issuer: {cert.issuer}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.8rem', color: 'var(--success)' }}>
               <CheckCircle size={16} /> Valid
            </div>
          </div>
          
          <div style={{ marginTop: '16px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '0.85rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Public Key</span>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
                <Key size={14} style={{ color: 'var(--accent-primary)' }}/>
                {cert.public_key.algorithm} ({cert.public_key.size}-bit)
              </div>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Signature Algorithm</span>
              <div style={{ marginTop: 4 }}>{cert.signature_algorithm}</div>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Valid From</span>
              <div style={{ marginTop: 4 }}>{new Date(cert.valid_from).toLocaleDateString()}</div>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Valid Until</span>
              <div style={{ marginTop: 4 }}>{new Date(cert.valid_to).toLocaleDateString()}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
