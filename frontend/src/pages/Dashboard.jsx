import React, { useEffect, useRef } from 'react';
import { Shield, Server, AlertTriangle, Award, IndianRupee, Clock, Wifi } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, BarChart, Bar, Legend } from 'recharts';
import { MOCK_ASSETS, ASSET_STATS, MOCK_ACTIVITY, CIPHER_STATS, CA_STATS, getScoreColor, getScoreClass, getRiskIcon } from '../mockData';

const SCORE_DIST = [
  { name: 'Critical (0-29)', value: ASSET_STATS.critical, color: '#ef4444' },
  { name: 'High Risk (30-59)', value: ASSET_STATS.high, color: '#f97316' },
  { name: 'Moderate (60-89)', value: ASSET_STATS.moderate, color: '#eab308' },
  { name: 'Safe (90-100)', value: ASSET_STATS.safe, color: '#22c55e' },
];

const TYPE_DIST = [
  { name: 'Web Apps', value: ASSET_STATS.webApps, color: '#6366f1' },
  { name: 'APIs', value: ASSET_STATS.apis, color: '#06b6d4' },
  { name: 'Servers', value: ASSET_STATS.servers, color: '#8b5cf6' },
  { name: 'Load Balancers', value: ASSET_STATS.loadBalancers, color: '#a855f7' },
  { name: 'Other', value: ASSET_STATS.others, color: '#64748b' },
];

const TREND = [
  { month: 'Oct', score: 12, assets: 45 }, { month: 'Nov', score: 18, assets: 62 },
  { month: 'Dec', score: 22, assets: 78 }, { month: 'Jan', score: 28, assets: 95 },
  { month: 'Feb', score: 35, assets: 112 }, { month: 'Mar', score: ASSET_STATS.avgScore, assets: 128 },
];

const CERT_EXPIRY = [
  { name: '0-30 Days', value: ASSET_STATS.expiringCerts, color: '#ef4444' },
  { name: '30-60 Days', value: Math.round(ASSET_STATS.total * 0.06), color: '#f97316' },
  { name: '60-90 Days', value: Math.round(ASSET_STATS.total * 0.04), color: '#eab308' },
  { name: '>90 Days', value: Math.round(ASSET_STATS.total * 0.7), color: '#22c55e' },
];

const IP_DIST = [
  { name: 'IPv4', value: ASSET_STATS.ipv4, color: '#6366f1' },
  { name: 'IPv6', value: ASSET_STATS.ipv6, color: '#06b6d4' },
];

const riskPct = Math.round(ASSET_STATS.critical / ASSET_STATS.total * 100);

export default function Dashboard() {
  const mapRef = useRef(null);
  const mapInst = useRef(null);

  useEffect(() => {
    if (mapRef.current && !mapInst.current && window.L) {
      const map = window.L.map(mapRef.current, { zoomControl: false, attributionControl: false }).setView([22, 79], 5);
      window.L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 18 }).addTo(map);
      MOCK_ASSETS.forEach(a => {
        if (!a.latitude) return;
        const c = getScoreColor(a.quantumScore);
        const icon = window.L.divIcon({ className: '', html: `<div style="width:10px;height:10px;border-radius:50%;background:${c};box-shadow:0 0 8px ${c}80;border:1.5px solid rgba(255,255,255,0.25)"></div>`, iconSize: [10, 10] });
        window.L.marker([a.latitude, a.longitude], { icon }).bindPopup(`<div style="font-family:Inter;font-size:11px"><b>${a.domain}</b><br>Score: ${a.quantumScore} | ${a.keyExchange}<br>TLS ${a.tlsVersion} | ${a.city}</div>`).addTo(map);
      });
      mapInst.current = map;
    }
    return () => { if (mapInst.current) { mapInst.current.remove(); mapInst.current = null; } };
  }, []);

  return (
    <div className="fade-in">
      {/* KPI Row 1 */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(6, 1fr)' }}>
        {[
          { label: 'Total Assets', value: ASSET_STATS.total, icon: <Server size={18}/>, accent: 'quantum' },
          { label: 'Public Web Apps', value: ASSET_STATS.webApps, icon: <Wifi size={18}/>, accent: 'primary' },
          { label: 'APIs', value: ASSET_STATS.apis, icon: <Shield size={18}/>, accent: 'quantum' },
          { label: 'Servers', value: ASSET_STATS.servers, icon: <Server size={18}/>, accent: 'primary' },
          { label: 'Expiring Certs', value: ASSET_STATS.expiringCerts + ASSET_STATS.expiredCerts, icon: <Clock size={18}/>, accent: 'danger' },
          { label: 'High Risk Assets', value: ASSET_STATS.critical, icon: <AlertTriangle size={18}/>, accent: 'danger' },
        ].map((k, i) => (
          <div className={`kpi-card accent-${k.accent}`} key={i}>
            <div className={`kpi-icon ${k.accent}`}>{k.icon}</div>
            <div className="kpi-value">{k.value}</div>
            <div className="kpi-label">{k.label}</div>
          </div>
        ))}
      </div>

      {/* Row 2: Type + Risk + CertExpiry + IPVersion */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 16, marginBottom: 20 }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Asset Type Distribution</span></div>
          <ResponsiveContainer width="100%" height={180}>
            <PieChart><Pie data={TYPE_DIST} cx="50%" cy="50%" innerRadius={40} outerRadius={70} paddingAngle={3} dataKey="value" stroke="none">
              {TYPE_DIST.map((e, i) => <Cell key={i} fill={e.color} />)}
            </Pie><Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} /></PieChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, justifyContent: 'center' }}>
            {TYPE_DIST.map((d, i) => <span key={i} style={{ fontSize: '0.65rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 8, height: 8, borderRadius: 2, background: d.color, display: 'inline-block' }}/>{d.name} {d.value}</span>)}
          </div>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Asset Risk Distribution</span></div>
          <div style={{ textAlign: 'center', marginBottom: 8 }}><span style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ef4444' }}>{riskPct}%</span><br/><span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>High Risk</span></div>
          <ResponsiveContainer width="100%" height={120}>
            <BarChart data={SCORE_DIST} barCategoryGap="15%">
              <XAxis dataKey="name" hide /><YAxis hide />
              <Bar dataKey="value" radius={[4,4,0,0]}>{SCORE_DIST.map((e,i)=><Cell key={i} fill={e.color}/>)}</Bar>
            </BarChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', justifyContent: 'space-around', fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: 4 }}>
            {['Critical','High','Medium','Low'].map((l,i) => <span key={i}>{l}</span>)}
          </div>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Certificate Expiry Timeline</span></div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, padding: '8px 0' }}>
            {CERT_EXPIRY.map((c, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ width: 10, height: 10, borderRadius: 2, background: c.color, flexShrink: 0 }}/>
                <span style={{ fontSize: '0.78rem', flex: 1, color: 'var(--text-secondary)' }}>{c.name}</span>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: c.color }}>{c.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">IP Version Breakdown</span></div>
          <ResponsiveContainer width="100%" height={140}>
            <PieChart><Pie data={IP_DIST} cx="50%" cy="50%" innerRadius={35} outerRadius={55} paddingAngle={4} dataKey="value" stroke="none">
              {IP_DIST.map((e,i) => <Cell key={i} fill={e.color}/>)}
            </Pie><Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} /></PieChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 16, fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            {IP_DIST.map((d,i)=><span key={i} style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 8, height: 8, borderRadius: 2, background: d.color, display: 'inline-block' }}/>{d.name} {Math.round(d.value/(ASSET_STATS.ipv4+ASSET_STATS.ipv6)*100)}%</span>)}
          </div>
        </div>
      </div>

      {/* Asset Inventory Preview + Map */}
      <div className="dashboard-grid">
        <div className="card" style={{ overflow: 'hidden' }}>
          <div className="card-header">
            <span className="card-title">Asset Inventory (Top 10)</span>
            <div style={{ display: 'flex', gap: 6 }}>
              <button className="btn btn-outline" style={{ fontSize: '0.7rem', padding: '4px 10px' }}>Scan All</button>
            </div>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead><tr><th>Asset Name</th><th>Type</th><th>Owner</th><th>Risk</th><th>TLS</th><th>Key Length</th><th>Last Scan</th></tr></thead>
              <tbody>
                {MOCK_ASSETS.slice(0, 10).map(a => (
                  <tr key={a.id}>
                    <td className="domain">{a.domain}</td>
                    <td style={{ fontSize: '0.75rem' }}>{a.assetType}</td>
                    <td style={{ fontSize: '0.75rem' }}>{a.owner}</td>
                    <td><span className={`score-badge ${getScoreClass(a.quantumScore)}`}>{getRiskIcon(a.quantumScore)} {a.risk}</span></td>
                    <td><span className={`chip ${a.tlsVersion === '1.3' ? 'tls13' : 'tls12'}`}>TLS {a.tlsVersion}</span></td>
                    <td style={{ fontSize: '0.8rem' }}>{a.keySize}-bit</td>
                    <td style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{new Date(a.lastScanAt).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Geographic Asset Distribution</span></div>
          <div className="map-container" ref={mapRef} />
        </div>
      </div>

      {/* Row: Crypto Overview + Trend + Activity */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginTop: 20 }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Crypto & Security Overview</span></div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {CIPHER_STATS.slice(0, 5).map((c, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontSize: '0.72rem', flex: 1, color: 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c.name}</span>
                <div style={{ width: 80, height: 6, background: 'var(--bg-elevated)', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ width: `${c.count / ASSET_STATS.total * 100}%`, height: '100%', background: 'var(--accent-primary)', borderRadius: 3 }}/>
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-primary)', width: 24, textAlign: 'right' }}>{c.count}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 14, paddingTop: 12, borderTop: '1px solid var(--border-color)' }}>
            <div className="card-title" style={{ marginBottom: 8 }}>Encryption Protocols</div>
            <div style={{ display: 'flex', gap: 12 }}>
              {[{ l: 'TLS 1.3', v: ASSET_STATS.tls13, c: '#22c55e' },{ l: 'TLS 1.2', v: ASSET_STATS.tls12, c: '#eab308' },{ l: 'TLS 1.1', v: ASSET_STATS.tls11, c: '#f97316' },{ l: 'TLS 1.0', v: ASSET_STATS.tls10, c: '#ef4444' }].map((t,i)=>(
                <div key={i} style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                  <span style={{ width: 8, height: 8, borderRadius: 2, background: t.c, display: 'inline-block', marginRight: 4 }}/>{t.l}: <b style={{ color: t.c }}>{t.v}</b>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Quantum Score Trend</span><span className={`score-badge ${getScoreClass(ASSET_STATS.avgScore)}`}>{ASSET_STATS.avgScore} Avg</span></div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={TREND}>
              <defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/><stop offset="95%" stopColor="#6366f1" stopOpacity={0}/></linearGradient></defs>
              <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false}/>
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} domain={[0,100]}/>
              <Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }}/>
              <Area type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={2} fill="url(#sg)"/>
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="card" style={{ maxHeight: 340, overflow: 'hidden' }}>
          <div className="card-header"><span className="card-title">Recent Scans & Activity</span></div>
          <div className="activity-feed">
            {MOCK_ACTIVITY.map(item => (
              <div className="activity-item" key={item.id}>
                <div className={`activity-dot ${item.severity}`}/>
                <div><div className="activity-msg">{item.message}</div><div className="activity-time">{item.time}</div></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
