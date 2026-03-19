import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LayoutDashboard, Server, Search, FileText, Shield, GitBranch, Star, Wrench, Award, ClipboardCheck, BarChart3 } from 'lucide-react';

const NAV = [
  { section: 'Monitor', items: [
    { id: 'dashboard', label: 'Home', icon: LayoutDashboard, path: '/' },
    { id: 'assets', label: 'Asset Inventory', icon: Server, path: '/assets', badge: '128' },
    { id: 'discovery', label: 'Asset Discovery', icon: Search, path: '/discovery' },
  ]},
  { section: 'Analysis', items: [
    { id: 'cbom', label: 'CBOM', icon: FileText, path: '/cbom' },
    { id: 'posture', label: 'Posture of PQC', icon: Shield, path: '/posture' },
    { id: 'blast-radius', label: 'Blast Radius', icon: GitBranch, path: '/blast-radius' },
    { id: 'cyber-rating', label: 'Cyber Rating', icon: Star, path: '/cyber-rating' },
  ]},
  { section: 'Manage', items: [
    { id: 'remediation', label: 'Remediation', icon: Wrench, path: '/remediation', badge: '11', badgeType: 'warning' },
    { id: 'certificates', label: 'Certificates', icon: Award, path: '/certificates' },
    { id: 'compliance', label: 'Compliance', icon: ClipboardCheck, path: '/compliance' },
    { id: 'reporting', label: 'Reporting', icon: BarChart3, path: '/reporting' },
  ]},
];

export default function Sidebar({ currentPage, onNavigate }) {
  const navigate = useNavigate();
  const go = (item) => { onNavigate(item.id); navigate(item.path); };

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="6" fill="url(#sg)"/><text x="16" y="22" fontFamily="Inter" fontSize="17" fontWeight="800" fill="white" textAnchor="middle">Q</text><defs><linearGradient id="sg" x1="0" y1="0" x2="32" y2="32"><stop stopColor="#06b6d4"/><stop offset=".5" stopColor="#6366f1"/><stop offset="1" stopColor="#a855f7"/></linearGradient></defs></svg>
        </div>
        <div className="sidebar-brand-text">
          <h1>Q-Sentra</h1>
          <p>PNB QuantumGuard</p>
        </div>
      </div>
      <nav className="sidebar-nav">
        {NAV.map(s => (
          <div className="sidebar-section" key={s.section}>
            <div className="sidebar-section-title">{s.section}</div>
            {s.items.map(item => (
              <div key={item.id} className={`sidebar-link ${currentPage === item.id ? 'active' : ''}`} onClick={() => go(item)}>
                <item.icon size={17} />
                <span>{item.label}</span>
                {item.badge && <span className={`sidebar-badge ${item.badgeType || 'critical'}`}>{item.badge}</span>}
              </div>
            ))}
          </div>
        ))}
      </nav>
      <div style={{ padding: '12px 16px', borderTop: '1px solid var(--border-color)', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
          <div style={{ width: 28, height: 28, borderRadius: '50%', background: 'var(--gradient-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', fontWeight: 600, color: 'white' }}>SA</div>
          <div><div style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>hackathon_user</div><div>admin@pnb.co.in</div></div>
        </div>
        <div style={{ opacity: 0.5 }}>PNB Hackathon 2026 · v1.0.0</div>
      </div>
    </aside>
  );
}
