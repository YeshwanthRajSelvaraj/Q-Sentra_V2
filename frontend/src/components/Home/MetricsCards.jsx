import React from 'react';
import { Server, ShieldAlert, AlertTriangle, ShieldCheck } from 'lucide-react';
import { ASSET_STATS } from '../../mockData';

export default function MetricsCards({ summary }) {
  const tot = summary?.total_assets !== undefined ? summary.total_assets : ASSET_STATS.total;
  const avg = summary?.avg_pqc_score !== undefined ? summary.avg_pqc_score.toFixed(1) : ASSET_STATS.avgScore;
  const risk = summary?.at_risk_count !== undefined ? summary.at_risk_count : ASSET_STATS.critical;
  const ready = summary?.pqc_ready_count !== undefined ? summary.pqc_ready_count : ASSET_STATS.safe;

  const cards = [
    { label: 'Total Public Assets', value: tot, icon: Server, color: '#3b82f6', trend: '↑', valColor: 'white', bg: 'rgba(59,130,246,0.1)' },
    { label: 'Enterprise PQC Score', value: avg, icon: ShieldAlert, color: '#a855f7', trend: '↑', valColor: 'white', bg: 'rgba(168,85,247,0.1)' },
    { label: 'Assets at Risk (<40)', value: risk, icon: AlertTriangle, color: '#ef4444', trend: '↓', valColor: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
    { label: 'PQC Ready (≥70)', value: ready, icon: ShieldCheck, color: '#22c55e', trend: '↑', valColor: '#22c55e', bg: 'rgba(34,197,94,0.1)' }
  ];

  return (
    <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: 24, gap: 16 }}>
      {cards.map((k, i) => (
        <div key={i} className="card hover-effect" style={{ flex: 1, padding: 20 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <div style={{ background: k.bg, padding: 10, borderRadius: 10 }}>
              <k.icon size={22} style={{ color: k.color }} />
            </div>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: k.trend === '↑' ? '#22c55e' : (k.trend === '↓' && k.color !== '#ef4444' ? '#ef4444' : '#22c55e'), display: 'flex', alignItems: 'center' }}>
               {k.trend} 2% this week
            </div>
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: k.valColor, marginBottom: 4 }}>{k.value}</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text-secondary)' }}>{k.label}</div>
        </div>
      ))}
    </div>
  );
}
