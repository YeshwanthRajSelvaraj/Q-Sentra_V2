import React from 'react';
import { useParams } from 'react-router-dom';
import { Shield, CheckCircle, ExternalLink } from 'lucide-react';
import { MOCK_CERTS, getScoreColor, getScoreClass } from '../mockData';

export default function Verify() {
  const { assetId } = useParams();
  const cert = MOCK_CERTS.find(c => c.assetId === assetId);

  return (
    <div className="verify-container">
      <div className="verify-card">
        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <div style={{ width: 56, height: 56, borderRadius: 14, background: 'var(--gradient-quantum)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: 16 }}>
            <Shield size={28} color="white" />
          </div>
          <h1 style={{ fontSize: '1.4rem', fontWeight: 700 }}>Q-Sentra Certificate Verification</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: 4 }}>Punjab National Bank — Public Verification Portal</p>
        </div>

        {cert ? (
          <div className="fade-in">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: 16, background: 'var(--score-safe-bg)', borderRadius: 10, marginBottom: 20 }}>
              <CheckCircle size={20} color="#22c55e" />
              <span style={{ fontSize: '0.9rem', fontWeight: 500, color: '#22c55e' }}>Certificate Verified — Blockchain Anchored</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
              {[
                ['Certificate ID', cert.certId],
                ['Asset', cert.assetId],
                ['Quantum Score', cert.quantumScore],
                ['Algorithms', cert.algorithms.join(', ')],
                ['Issued', cert.issuedAt],
                ['Valid Until', cert.validUntil],
                ['Status', cert.status],
                ['Hash', cert.certificateHash],
                ['Blockchain TX', cert.blockchainTx],
                ['Block Number', cert.blockNumber],
                ['Network', cert.network],
              ].map(([k, v]) => (
                <div className="cert-detail-row" key={k}>
                  <span className="label">{k}</span>
                  <span className="value">{String(v)}</span>
                </div>
              ))}
            </div>
            <button className="btn btn-outline" style={{ width: '100%', marginTop: 16, justifyContent: 'center' }}>
              <ExternalLink size={14} /> View on Block Explorer
            </button>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
            <Shield size={48} strokeWidth={1} style={{ marginBottom: 16, opacity: 0.3 }} />
            <p>No quantum-safe certificate found for <strong>{assetId}</strong></p>
            <p style={{ fontSize: '0.82rem', marginTop: 8 }}>This asset has not yet achieved quantum-safe certification.</p>
          </div>
        )}

        <div style={{ textAlign: 'center', marginTop: 28, padding: '16px 0', borderTop: '1px solid var(--border-color)' }}>
          <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            Verified by Q-Sentra — Punjab National Bank Cybersecurity Division<br />
            Powered by Hyperledger Fabric Blockchain
          </p>
        </div>
      </div>
    </div>
  );
}
