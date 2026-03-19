import React, { useState, useEffect } from 'react';
import { MOCK_ASSETS, ASSET_STATS, CYBER_RATING, getScoreColor } from '../mockData';

const TIER_CONFIG = {
  'Elite-PQC': { color: '#22c55e', bg: 'rgba(34,197,94,0.1)', desc: 'Indicates a stronger security posture', emoji: '✅' },
  'Standard': { color: '#eab308', bg: 'rgba(234,179,8,0.1)', desc: 'Moderate security — improvement needed', emoji: '⚠️' },
  'Legacy': { color: '#ef4444', bg: 'rgba(239,68,68,0.1)', desc: 'Critical — immediate action required', emoji: '🚨' },
};

export default function CyberRating() {
  const [ratingData, setRatingData] = useState(CYBER_RATING);
  const [assetScores, setAssetScores] = useState(MOCK_ASSETS.slice(0, 15).map(a => ({
    url: a.domain, score: Math.round(a.quantumScore * 10),
  })));

  useEffect(() => {
    async function loadRating() {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/rating');
        const data = await res.json();
        // The API returns {score, tier, breakdown, assetScores}
        if (data.score !== undefined) {
          setRatingData({
            score: data.score,
            tier: data.tier,
            breakdown: data.breakdown,
          });
          if (data.assetScores && data.assetScores.length > 0) {
            setAssetScores(data.assetScores);
          }
        }
      } catch (e) {
        console.error("Failed to load dynamic rating", e);
      }
    }
    loadRating();
  }, []);

  const tier = TIER_CONFIG[ratingData.tier] || TIER_CONFIG['Standard'];



  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div><h1 className="page-title">Cyber Rating</h1><p className="page-subtitle">Consolidated enterprise-level PQC cyber safety rating</p></div>
      </div>

      {/* Main Score Card */}
      <div className="card" style={{ textAlign: 'center', padding: '40px 24px', marginBottom: 24 }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 24, color: 'var(--text-primary)' }}>
          Consolidated Enterprise-Level Cyber-Rating Score
        </h2>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 24, padding: '20px 40px', background: tier.bg, borderRadius: 12, border: `2px solid ${tier.color}30` }}>
          <div style={{ fontSize: '3.5rem', fontWeight: 900, color: tier.color, fontFamily: 'Inter, sans-serif', lineHeight: 1 }}>
            {ratingData.score}
            <span style={{ fontSize: '1.2rem', fontWeight: 400, color: 'var(--text-muted)' }}>/1000</span>
          </div>
          <div style={{ textAlign: 'left' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: tier.color }}>{tier.emoji} {ratingData.tier}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{tier.desc}</div>
          </div>
        </div>
      </div>

      {/* Tier Legend */}
      <div className="card" style={{ marginBottom: 24 }}>
        <table className="data-table">
          <thead><tr><th>Status</th><th>PQC Rating For Enterprise</th></tr></thead>
          <tbody>
            {[
              { status: '🚨 Legacy', range: '< 400', color: '#ef4444' },
              { status: '⚠️ Standard', range: '400 till 700', color: '#eab308' },
              { status: '✅ Elite-PQC', range: '> 700', color: '#22c55e' },
            ].map((t, i) => (
              <tr key={i} style={{ background: ratingData.tier === t.status.split(' ')[1] ? tier.bg : 'transparent' }}>
                <td style={{ fontWeight: 600, color: t.color }}>{t.status}</td>
                <td>{t.range}</td>
              </tr>
            ))}
            <tr><td style={{ fontWeight: 500 }}>Maximum Score after normalisation*</td><td style={{ fontWeight: 700 }}>1000</td></tr>
          </tbody>
        </table>
      </div>

      {/* Rating Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 24 }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Rating Breakdown</span></div>
          {ratingData.breakdown.map((b, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 0', borderBottom: '1px solid var(--border-color)' }}>
              <span style={{ fontSize: '0.82rem', flex: 1, color: 'var(--text-secondary)' }}>{b.category}</span>
              <div style={{ width: 120, height: 8, background: 'var(--bg-elevated)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${b.value}%`, height: '100%', background: getScoreColor(b.value), borderRadius: 4, transition: 'width 0.6s ease' }} />
              </div>
              <span style={{ fontSize: '0.82rem', fontWeight: 600, color: getScoreColor(b.value), width: 50, textAlign: 'right' }}>{b.value}/{b.max}</span>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', width: 30 }}>×{b.weight}%</span>
            </div>
          ))}
        </div>

        {/* Per-URL PQC Scores */}
        <div className="card">
          <div className="card-header"><span className="card-title">Per-URL PQC Score</span></div>
          <table className="data-table">
            <thead><tr><th>URL</th><th>PQC Score</th></tr></thead>
            <tbody>
              {assetScores.map((a, i) => (
                <tr key={i}>
                  <td className="domain">{a.url}</td>
                  <td style={{ fontWeight: 700, fontSize: '1rem', color: getScoreColor(a.score / 10) }}>{a.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
