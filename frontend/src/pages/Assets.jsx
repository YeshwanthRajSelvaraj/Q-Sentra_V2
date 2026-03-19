import React, { useState } from 'react';
import { Search, Download, Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { MOCK_ASSETS, ASSET_STATS, getScoreColor, getScoreClass, getScoreLabel, getRiskIcon } from '../mockData';

export default function Assets() {
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('quantumScore');
  const [sortAsc, setSortAsc] = useState(true);
  const [page, setPage] = useState(0);
  const navigate = useNavigate();
  const PER_PAGE = 20;

  const filtered = MOCK_ASSETS
    .filter(a => !search || a.domain.toLowerCase().includes(search.toLowerCase()) || a.ip.includes(search) || a.keyExchange.toLowerCase().includes(search.toLowerCase()) || a.assetType.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => { const v = typeof a[sortBy] === 'number' ? a[sortBy] - b[sortBy] : String(a[sortBy]).localeCompare(String(b[sortBy])); return sortAsc ? v : -v; });

  const totalPages = Math.ceil(filtered.length / PER_PAGE);
  const paged = filtered.slice(page * PER_PAGE, (page + 1) * PER_PAGE);

  const handleSort = (col) => { if (sortBy === col) setSortAsc(!sortAsc); else { setSortBy(col); setSortAsc(true); } };

  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div>
          <h1 className="page-title">Asset Inventory</h1>
          <p className="page-subtitle">{ASSET_STATS.total} cryptographic assets across PNB infrastructure</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-outline"><Plus size={14} /> Add Asset</button>
          <button className="btn btn-outline"><Download size={14} /> Export CSV</button>
          <button className="btn btn-primary">🔍 Scan All</button>
        </div>
      </div>

      <div className="data-table-wrapper">
        <div className="data-table-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1 }}>
            <Search size={16} style={{ color: 'var(--text-muted)' }} />
            <input type="text" placeholder="Search by domain, IP, cipher, type..." value={search} onChange={e => { setSearch(e.target.value); setPage(0); }}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-primary)', fontSize: '0.85rem', outline: 'none', width: '100%' }} />
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{filtered.length} results · Page {page + 1}/{totalPages}</div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('domain')} style={{ cursor: 'pointer' }}>Asset Name ⬍</th>
                <th>URL</th>
                <th onClick={() => handleSort('assetType')} style={{ cursor: 'pointer' }}>Type</th>
                <th>Owner</th>
                <th onClick={() => handleSort('quantumScore')} style={{ cursor: 'pointer' }}>Risk ⬍</th>
                <th>Cert Status</th>
                <th>Key Length</th>
                <th>Last Scan</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {paged.map(asset => (
                <tr key={asset.id}>
                  <td className="domain">{asset.domain}</td>
                  <td style={{ fontSize: '0.72rem', color: 'var(--accent-secondary)' }}>https://{asset.domain}</td>
                  <td style={{ fontSize: '0.75rem' }}>{asset.assetType}</td>
                  <td style={{ fontSize: '0.75rem' }}>{asset.owner}</td>
                  <td><span className={`score-badge ${getScoreClass(asset.quantumScore)}`}>{getRiskIcon(asset.quantumScore)} {asset.risk}</span></td>
                  <td>
                    <span className={`score-badge ${asset.certificate.status === 'valid' ? 'safe' : asset.certificate.status === 'expiring' ? 'moderate' : 'critical'}`}>
                      {asset.certificate.status === 'valid' ? '✓ Valid' : asset.certificate.status === 'expiring' ? '⚠ Expiring' : '✗ Expired'}
                    </span>
                  </td>
                  <td style={{ fontSize: '0.8rem' }}>{asset.keySize}-bit</td>
                  <td style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{new Date(asset.lastScanAt).toLocaleDateString()}</td>
                  <td>
                    <button className="btn btn-outline" style={{ padding: '4px 8px', fontSize: '0.7rem' }} onClick={() => navigate(`/cbom?asset=${asset.domain}`)}>
                      View CBOM
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: 6, padding: '12px 0' }}>
          <button className="btn btn-outline" disabled={page === 0} onClick={() => setPage(p => p - 1)} style={{ fontSize: '0.75rem', padding: '4px 12px' }}>← Prev</button>
          {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => (
            <button key={i} className={`btn ${page === i ? 'btn-primary' : 'btn-outline'}`} onClick={() => setPage(i)} style={{ fontSize: '0.75rem', padding: '4px 10px', minWidth: 32 }}>{i + 1}</button>
          ))}
          <button className="btn btn-outline" disabled={page >= totalPages - 1} onClick={() => setPage(p => p + 1)} style={{ fontSize: '0.75rem', padding: '4px 12px' }}>Next →</button>
        </div>
      </div>

      {/* Nameserver Records */}
      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-header"><span className="card-title">Nameserver Records</span><span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Domain: pnb.co.in</span></div>
        <table className="data-table">
          <thead><tr><th>Hostname</th><th>Type</th><th>IP Address</th><th>IPv6 Address</th><th>TTL</th></tr></thead>
          <tbody>
            {[
              { host: 'ns1.pnb.co.in', type: 'NS', ip: '203.145.130.10', ipv6: '2001:0db8:85a3::1', ttl: 3600 },
              { host: 'ns2.pnb.co.in', type: 'NS', ip: '203.145.130.11', ipv6: '2001:0db8:85a3::2', ttl: 3600 },
              { host: 'ns3.pnb.co.in', type: 'NS', ip: '203.145.130.12', ipv6: '2001:0db8:85a3::3', ttl: 3600 },
              { host: 'www.pnb.co.in', type: 'A', ip: '34.12.11.45', ipv6: '2001:0db8:85a3::e', ttl: 300 },
              { host: 'mail.pnb.co.in', type: 'MX', ip: '35.11.44.10', ipv6: '2001:0db8:85a3::f', ttl: 300 },
            ].map((r, i) => (
              <tr key={i}>
                <td className="domain">{r.host}</td>
                <td><span className={`chip ${r.type === 'NS' ? 'tls13' : 'tls12'}`}>{r.type}</span></td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{r.ip}</td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.75rem', color: 'var(--text-muted)' }}>{r.ipv6}</td>
                <td>{r.ttl}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
