import React, { useState } from 'react';
import { Play, Settings2, ChevronDown, ChevronUp } from 'lucide-react';

export default function DiscoveryControls({ onStartScan }) {
  const [expanded, setExpanded] = useState(false);
  const [scope, setScope] = useState('All PNB Domains');
  const [options, setOptions] = useState({
    enableCtLogs: true,
    enableDnsBruteforce: true,
    enableReverseDns: true,
    wordlist: 'medium'
  });
  const [scanning, setScanning] = useState(false);

  const handleStart = async () => {
    setScanning(true);
    await onStartScan(scope, options);
    setScanning(false);
  };

  return (
    <div className="card" style={{ marginBottom: 20, border: '1px solid var(--accent-primary)' }}>
      <div style={{ padding: '16px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
         <div style={{ display: 'flex', gap: 16, alignItems: 'center', flex: 1 }}>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
               <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 4 }}>Scan Scope</label>
               <select 
                 className="form-input" 
                 value={scope} 
                 onChange={e => setScope(e.target.value)}
                 style={{ padding: '8px 12px', background: 'var(--bg-elevated)', border: '1px solid var(--border-color)', color: 'white', borderRadius: 6, minWidth: 200 }}
               >
                 <option>All PNB Domains</option>
                 <option>Custom Domain List</option>
                 <option>IP Ranges</option>
               </select>
            </div>
            
            <button 
              className="btn btn-outline" 
              onClick={() => setExpanded(!expanded)} 
              style={{ marginTop: 18, display: 'flex', alignItems: 'center', gap: 6 }}
            >
              <Settings2 size={16} /> Advanced Options {expanded ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
            </button>
         </div>

         <button 
           className="btn btn-primary" 
           onClick={handleStart} 
           disabled={scanning}
           style={{ padding: '10px 24px', fontSize: '1rem', display: 'flex', alignItems: 'center', gap: 8 }}
         >
           <Play size={18} fill="currentColor" />
           {scanning ? 'Scanning Network...' : 'Start New Discovery Scan'}
         </button>
      </div>

      {expanded && (
        <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border-color)', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, background: 'rgba(0,0,0,0.2)' }}>
           <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem' }}>
             <input type="checkbox" checked={options.enableCtLogs} onChange={e => setOptions({...options, enableCtLogs: e.target.checked})} />
             Enable CT Logs scanning
           </label>
           <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem' }}>
             <input type="checkbox" checked={options.enableDnsBruteforce} onChange={e => setOptions({...options, enableDnsBruteforce: e.target.checked})} />
             Enable DNS Bruteforce
           </label>
           <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem' }}>
             <input type="checkbox" checked={options.enableReverseDns} onChange={e => setOptions({...options, enableReverseDns: e.target.checked})} />
             Enable Reverse DNS
           </label>
           <div style={{ display: 'flex', flexDirection: 'column' }}>
             <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 4 }}>DNS Wordlist</label>
             <select 
               value={options.wordlist} 
               onChange={e => setOptions({...options, wordlist: e.target.value})}
               style={{ padding: '4px 8px', background: 'var(--bg-elevated)', border: '1px solid var(--border-color)', color: 'white', borderRadius: 4 }}
             >
               <option value="small">Small (10k)</option>
               <option value="medium">Medium (100k)</option>
               <option value="large">Large (1M+)</option>
             </select>
           </div>
        </div>
      )}
    </div>
  );
}
