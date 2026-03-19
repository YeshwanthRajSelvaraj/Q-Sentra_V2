// ═══════════════════════════════════════════════════════════════════════
// Q-Sentra Extended Mock Data — 128+ Assets, Full Enterprise Scale
// Punjab National Bank - Quantum-Proof Cryptographic Asset Management
// ═══════════════════════════════════════════════════════════════════════

const DOMAINS = [
  'www.pnb.co.in','netbanking.pnb.co.in','api.pnb.co.in','mobile.pnb.co.in','vpn.pnb.co.in',
  'mail.pnb.co.in','upi.pnb.co.in','imps.pnb.co.in','swift.pnb.co.in','cdn.pnb.co.in',
  'portal.pnb.co.in','crm.pnb.co.in','hrms.pnb.co.in','treasury.pnb.co.in','forex.pnb.co.in',
  'neft.pnb.co.in','rtgs.pnb.co.in','aeps.pnb.co.in','bbps.pnb.co.in','nach.pnb.co.in',
  'loan.pnb.co.in','insurance.pnb.co.in','mutual.pnb.co.in','demat.pnb.co.in','cards.pnb.co.in',
  'pos.pnb.co.in','atm.pnb.co.in','branch.pnb.co.in','audit.pnb.co.in','compliance.pnb.co.in',
  'kyc.pnb.co.in','aml.pnb.co.in','fraud.pnb.co.in','risk.pnb.co.in','analytics.pnb.co.in',
  'dms.pnb.co.in','cms.pnb.co.in','sms.pnb.co.in','email-gw.pnb.co.in','proxy.pnb.co.in',
  'ldap.pnb.co.in','dns1.pnb.co.in','dns2.pnb.co.in','ntp.pnb.co.in','siem.pnb.co.in',
  'soc.pnb.co.in','waf.pnb.co.in','ids.pnb.co.in','backup.pnb.co.in','dr.pnb.co.in',
  'staging.pnb.co.in','dev.pnb.co.in','test.pnb.co.in','uat.pnb.co.in','sandbox.pnb.co.in',
  'jenkins.pnb.co.in','gitlab.pnb.co.in','sonar.pnb.co.in','nexus.pnb.co.in','grafana.pnb.co.in',
  'prometheus.pnb.co.in','elk.pnb.co.in','kafka.pnb.co.in','redis-mgmt.pnb.co.in','mongo-mgmt.pnb.co.in',
  'pg-admin.pnb.co.in','vault.pnb.co.in','consul.pnb.co.in','k8s.pnb.co.in','docker.pnb.co.in',
  'nps.pnb.co.in','ppf.pnb.co.in','fd.pnb.co.in','rd.pnb.co.in','savings.pnb.co.in',
  'current.pnb.co.in','corporate.pnb.co.in','msme.pnb.co.in','agri.pnb.co.in','education.pnb.co.in',
  'pension.pnb.co.in','govt.pnb.co.in','tax.pnb.co.in','gst.pnb.co.in','tds.pnb.co.in',
  'report.pnb.co.in','dashboard.pnb.co.in','admin.pnb.co.in','super.pnb.co.in','bi.pnb.co.in',
  'etl.pnb.co.in','dwh.pnb.co.in','lake.pnb.co.in','ml.pnb.co.in','ai.pnb.co.in',
  'chatbot.pnb.co.in','ivr.pnb.co.in','whatsapp.pnb.co.in','push.pnb.co.in','notify.pnb.co.in',
  'otp.pnb.co.in','auth.pnb.co.in','sso.pnb.co.in','oauth.pnb.co.in','mfa.pnb.co.in',
  'cert.pnb.co.in','pki.pnb.co.in','ca.pnb.co.in','ocsp.pnb.co.in','crl.pnb.co.in',
  'log.pnb.co.in','trace.pnb.co.in','metric.pnb.co.in','alert.pnb.co.in','incident.pnb.co.in',
  'ticket.pnb.co.in','itsm.pnb.co.in','cmdb.pnb.co.in','asset-mgmt.pnb.co.in','patch.pnb.co.in',
  'antivirus.pnb.co.in','dlp.pnb.co.in','edr.pnb.co.in','xdr.pnb.co.in','ztna.pnb.co.in',
  'sdwan.pnb.co.in','mpls.pnb.co.in','wifi.pnb.co.in',
];

const TYPES = ['Web Application','API Endpoint','Server','VPN Gateway','Email Server','Payment Gateway','Banking Core','CDN','Load Balancer','Database','Microservice','Mobile API'];
const OWNERS = ['IT','DevOps','Infra','Security','Treasury','Retail Banking','Corporate Banking','Digital','Network'];
const TLS_VERSIONS = ['1.3','1.2','1.1','1.0'];
const TLS_WEIGHTS = [0.45, 0.40, 0.10, 0.05]; // probability weights
const CIPHERS_13 = ['TLS_AES_256_GCM_SHA384','TLS_AES_128_GCM_SHA256','TLS_CHACHA20_POLY1305_SHA256'];
const CIPHERS_12 = ['ECDHE-RSA-AES256-GCM-SHA384','ECDHE-ECDSA-AES256-GCM-SHA384','ECDHE-RSA-AES128-GCM-SHA256','DHE-RSA-AES256-GCM-SHA384','AES256-GCM-SHA384','AES128-GCM-SHA256','TLS_RSA_WITH_AES_128_CBC_SHA','TLS_RSA_WITH_DES_CBC_SHA'];
const KEX_OPTIONS = ['ML-KEM-768','ML-KEM-1024','X25519+Kyber768','X25519','ECDHE','DHE','RSA','DH'];
const SIG_OPTIONS = ['ML-DSA-65','ML-DSA-87','SLH-DSA-128f','ECDSA-SHA384','ECDSA-SHA256','RSA-SHA256','RSA-SHA384','SHA256withRSA'];
const KEY_SIZES = [256, 384, 768, 1024, 2048, 3072, 4096];
const ISSUERS = ['DigiCert','Let\'s Encrypt','GlobalSign','Comodo','Thawte','GeoTrust','PNB Internal CA','Symantec','Entrust','Sectigo'];
const CITIES = [
  {name:'New Delhi',lat:28.6139,lng:77.2090},{name:'Mumbai',lat:19.0760,lng:72.8777},{name:'Bangalore',lat:12.9716,lng:77.5946},
  {name:'Chennai',lat:13.0827,lng:80.2707},{name:'Kolkata',lat:22.5726,lng:88.3639},{name:'Hyderabad',lat:17.3850,lng:78.4867},
  {name:'Pune',lat:18.5204,lng:73.8567},{name:'Ahmedabad',lat:23.0225,lng:72.5714},{name:'Jaipur',lat:26.9124,lng:75.7873},
  {name:'Lucknow',lat:26.8467,lng:80.9462},{name:'Chandigarh',lat:30.7333,lng:76.7794},{name:'Patna',lat:25.6093,lng:85.1376},
];

function seededRandom(seed) {
  let x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

function pickWeighted(arr, weights, seed) {
  const r = seededRandom(seed);
  let sum = 0;
  for (let i = 0; i < weights.length; i++) { sum += weights[i]; if (r < sum) return arr[i]; }
  return arr[arr.length - 1];
}

function calcQuantumScore(tls, kex, sig, keySize) {
  const tlsScores = {'1.3':20,'1.2':5,'1.1':0,'1.0':0};
  const kexScores = {'ML-KEM-768':35,'ML-KEM-1024':35,'ML-KEM-512':30,'X25519+Kyber768':20,'X25519':10,'ECDHE':10,'DHE':5,'RSA':0,'DH':0};
  const sigScores = {'ML-DSA-87':30,'ML-DSA-65':30,'ML-DSA-44':28,'SLH-DSA-128f':28,'SLH-DSA-256f':30,'ECDSA-SHA384':10,'ECDSA-SHA256':10,'RSA-SHA256':0,'RSA-SHA384':0,'SHA256withRSA':0};
  const ks = kex.includes('ML-KEM') ? 15 : keySize >= 4096 ? 5 : keySize >= 3072 ? 3 : 0;
  return Math.min(100, (tlsScores[tls]||0) + (kexScores[kex]||0) + (sigScores[sig]||0) + ks);
}

// Generate 128 assets deterministically
export const MOCK_ASSETS = DOMAINS.map((domain, i) => {
  const seed = i + 42;
  const tls = pickWeighted(TLS_VERSIONS, TLS_WEIGHTS, seed);
  const cipher = tls === '1.3' ? CIPHERS_13[i % CIPHERS_13.length] : CIPHERS_12[i % CIPHERS_12.length];
  const kex = KEX_OPTIONS[i % KEX_OPTIONS.length];
  const sig = SIG_OPTIONS[i % SIG_OPTIONS.length];
  const keySize = KEY_SIZES[i % KEY_SIZES.length];
  const city = CITIES[i % CITIES.length];
  const score = calcQuantumScore(tls, kex, sig, keySize);
  const status = score >= 90 ? 'quantum_safe' : score >= 60 ? 'scanned' : score >= 30 ? 'warning' : 'critical';
  const type = TYPES[i % TYPES.length];
  const daysOffset = Math.floor(seededRandom(seed + 100) * 730);
  const expiry = new Date(2026, 0, 1);
  expiry.setDate(expiry.getDate() + daysOffset);

  return {
    id: String(i + 1),
    assetId: domain,
    domain,
    ip: `${10 + (i % 220)}.${(i * 7) % 256}.${(i * 13) % 256}.${(i * 3 + 1) % 256}`,
    port: 443,
    assetType: type,
    owner: OWNERS[i % OWNERS.length],
    tlsVersion: tls,
    cipherSuite: cipher,
    keyExchange: kex,
    signatureAlgorithm: sig,
    keySize,
    quantumScore: score,
    status,
    isPublic: seededRandom(seed + 200) > 0.3,
    latitude: city.lat + (seededRandom(seed + 300) - 0.5) * 0.1,
    longitude: city.lng + (seededRandom(seed + 400) - 0.5) * 0.1,
    city: city.name,
    lastScanAt: new Date(2026, 2, 10, 14, i % 60).toISOString(),
    discoveredAt: new Date(2026, 0, 1 + (i % 60)).toISOString(),
    certificate: {
      issuer: ISSUERS[i % ISSUERS.length],
      expiry: expiry.toISOString().split('T')[0],
      serial: `${(i*17+3).toString(16).toUpperCase()}:${(i*31+7).toString(16).toUpperCase()}:${(i*53+11).toString(16).toUpperCase()}`,
      status: daysOffset < 30 ? 'expiring' : daysOffset < 0 ? 'expired' : 'valid',
      keyLength: keySize,
    },
    risk: score < 30 ? 'High' : score < 60 ? 'Medium' : score < 90 ? 'Low' : 'Minimal',
  };
});

// Summary statistics
export const ASSET_STATS = {
  total: MOCK_ASSETS.length,
  webApps: MOCK_ASSETS.filter(a => a.assetType === 'Web Application').length,
  apis: MOCK_ASSETS.filter(a => a.assetType === 'API Endpoint').length,
  servers: MOCK_ASSETS.filter(a => a.assetType === 'Server').length,
  payments: MOCK_ASSETS.filter(a => a.assetType === 'Payment Gateway').length,
  vpns: MOCK_ASSETS.filter(a => a.assetType === 'VPN Gateway').length,
  loadBalancers: MOCK_ASSETS.filter(a => a.assetType === 'Load Balancer').length,
  others: MOCK_ASSETS.filter(a => !['Web Application','API Endpoint','Server','Payment Gateway','VPN Gateway','Load Balancer'].includes(a.assetType)).length,
  critical: MOCK_ASSETS.filter(a => a.quantumScore < 30).length,
  high: MOCK_ASSETS.filter(a => a.quantumScore >= 30 && a.quantumScore < 60).length,
  moderate: MOCK_ASSETS.filter(a => a.quantumScore >= 60 && a.quantumScore < 90).length,
  safe: MOCK_ASSETS.filter(a => a.quantumScore >= 90).length,
  avgScore: Math.round(MOCK_ASSETS.reduce((s, a) => s + a.quantumScore, 0) / MOCK_ASSETS.length * 10) / 10,
  expiringCerts: MOCK_ASSETS.filter(a => { const d = new Date(a.certificate.expiry); const now = new Date(2026, 2, 19); const diff = (d - now) / 86400000; return diff >= 0 && diff <= 30; }).length,
  expiredCerts: MOCK_ASSETS.filter(a => new Date(a.certificate.expiry) < new Date(2026, 2, 19)).length,
  tls13: MOCK_ASSETS.filter(a => a.tlsVersion === '1.3').length,
  tls12: MOCK_ASSETS.filter(a => a.tlsVersion === '1.2').length,
  tls11: MOCK_ASSETS.filter(a => a.tlsVersion === '1.1').length,
  tls10: MOCK_ASSETS.filter(a => a.tlsVersion === '1.0').length,
  ipv4: MOCK_ASSETS.length,
  ipv6: Math.round(MOCK_ASSETS.length * 0.14),
};

// Cipher usage stats
export const CIPHER_STATS = (() => {
  const map = {};
  MOCK_ASSETS.forEach(a => { map[a.cipherSuite] = (map[a.cipherSuite] || 0) + 1; });
  return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([name, count]) => ({ name: name.length > 30 ? name.slice(0, 30) + '...' : name, fullName: name, count }));
})();

// Key length stats
export const KEY_LENGTH_STATS = (() => {
  const map = {};
  MOCK_ASSETS.forEach(a => { const k = `${a.keySize}-bit`; map[k] = (map[k] || 0) + 1; });
  return Object.entries(map).sort((a, b) => parseInt(a[0]) - parseInt(b[0])).map(([name, count]) => ({ name, count }));
})();

// CA stats
export const CA_STATS = (() => {
  const map = {};
  MOCK_ASSETS.forEach(a => { map[a.certificate.issuer] = (map[a.certificate.issuer] || 0) + 1; });
  return Object.entries(map).sort((a, b) => b[1] - a[1]).map(([name, count]) => ({ name, count }));
})();

// Discovery records
export const DISCOVERY_DOMAINS = [
  { date: '03 Mar 2026', domain: 'www.cos.pnb.bank.in', regDate: '17 Feb 2005', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'confirmed' },
  { date: '17 Oct 2024', domain: 'www2.pnbrrbkiosk.in', regDate: '22 Mar 2021', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'new' },
  { date: '17 Oct 2024', domain: 'upload.pnbuniv.net.in', regDate: '22 Mar 2021', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'new' },
  { date: '17 Oct 2024', domain: 'postman.pnb.bank.in', regDate: '22 Mar 2021', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'false_positive' },
  { date: '17 Nov 2024', domain: 'proxy.pnb.bank.in', regDate: '22 Mar 2021', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'confirmed' },
  { date: '22 Dec 2024', domain: 'webmail.pnb.co.in', regDate: '15 Jun 2018', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'new' },
  { date: '05 Jan 2025', domain: 'uat-mobile.pnb.co.in', regDate: '10 Aug 2022', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'confirmed' },
  { date: '15 Jan 2025', domain: 'staging-api.pnb.co.in', regDate: '12 Sep 2022', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'new' },
  { date: '28 Jan 2025', domain: 'vpn2.pnb.co.in', regDate: '03 Mar 2020', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'confirmed' },
  { date: '10 Feb 2025', domain: 'testpay.pnb.co.in', regDate: '21 Nov 2023', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'false_positive' },
  { date: '01 Mar 2026', domain: 'swift-gw.pnb.co.in', regDate: '05 Jan 2024', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'new' },
  { date: '05 Mar 2026', domain: 'neft-api.pnb.co.in', regDate: '18 Feb 2024', registrar: 'National Internet Exchange of India', company: 'PNB', status: 'confirmed' },
];

export const DISCOVERY_SSL = [
  { domain: 'www.pnb.co.in', issuer: 'DigiCert', validFrom: '2025-06-01', validUntil: '2026-06-01', keyType: 'RSA-2048', sans: 3 },
  { domain: 'netbanking.pnb.co.in', issuer: 'DigiCert', validFrom: '2025-09-15', validUntil: '2026-09-15', keyType: 'RSA-2048', sans: 1 },
  { domain: 'api.pnb.co.in', issuer: "Let's Encrypt", validFrom: '2026-01-01', validUntil: '2026-04-01', keyType: 'ECDSA-P256', sans: 2 },
  { domain: 'upi.pnb.co.in', issuer: 'DigiCert', validFrom: '2025-07-15', validUntil: '2027-01-15', keyType: 'RSA-4096', sans: 1 },
  { domain: 'swift.pnb.co.in', issuer: 'PNB Internal CA', validFrom: '2026-01-01', validUntil: '2028-01-01', keyType: 'ML-KEM-768', sans: 1 },
];

export const DISCOVERY_IPS = Array.from({length: 34}, (_, i) => {
  const specificIPs = [
    '203.0.113.14',
    '198.51.100.93',
    '49.51.98.173',
    '49.52.123.215',
    '40.59.99.173',
    '40.101.27.212'
  ];
  const ip = i < specificIPs.length ? specificIPs[i] : `${10 + i}.${(i*7+3)%256}.${(i*13+5)%256}.${(i*3+1)%256}`;
  return {
    ip,
    subnet: `${ip}/${[24,16,28,24][i%4]}`,
    type: ['Server','Router','Firewall','Load Balancer','Switch'][i%5],
    ports: [443, 80, 8080, 22, 8443].slice(0, 1 + (i%4)),
    os: ['Linux','Windows Server','FortiOS','PAN-OS','Cisco IOS'][i%5],
    lastSeen: `${2026}-03-${String(1+(i%19)).padStart(2,'0')}`,
  };
});

// Remediation tasks
export const MOCK_TASKS = [
  { taskId: "REM-001", assetId: "www.pnb.co.in", title: "Upgrade web portal to TLS 1.3 with ML-KEM", priority: "critical", status: "pending", phase: 1, effortHours: 40, dueDate: "2026-06-30" },
  { taskId: "REM-002", assetId: "netbanking.pnb.co.in", title: "Migrate net banking to quantum-safe TLS", priority: "critical", status: "in_progress", phase: 1, effortHours: 80, dueDate: "2026-07-31" },
  { taskId: "REM-003", assetId: "api.pnb.co.in", title: "API gateway PQC upgrade", priority: "high", status: "pending", phase: 2, effortHours: 60, dueDate: "2026-09-30" },
  { taskId: "REM-004", assetId: "vpn.pnb.co.in", title: "VPN quantum-safe migration", priority: "high", status: "pending", phase: 2, effortHours: 50, dueDate: "2026-10-31" },
  { taskId: "REM-005", assetId: "upi.pnb.co.in", title: "UPI payment gateway PQC hardening", priority: "critical", status: "pending", phase: 1, effortHours: 100, dueDate: "2026-08-31" },
  { taskId: "REM-006", assetId: "mail.pnb.co.in", title: "Email server TLS upgrade", priority: "medium", status: "pending", phase: 3, effortHours: 30, dueDate: "2026-12-31" },
  { taskId: "REM-007", assetId: "cdn.pnb.co.in", title: "CDN edge PQC configuration", priority: "medium", status: "pending", phase: 3, effortHours: 20, dueDate: "2027-01-31" },
  { taskId: "REM-008", assetId: "mobile.pnb.co.in", title: "Mobile API PQC integration", priority: "high", status: "in_progress", phase: 2, effortHours: 70, dueDate: "2026-09-30" },
  { taskId: "REM-009", assetId: "imps.pnb.co.in", title: "IMPS gateway optimization", priority: "low", status: "completed", phase: 1, effortHours: 25, dueDate: "2026-04-30" },
  { taskId: "REM-010", assetId: "swift.pnb.co.in", title: "SWIFT ML-DSA certificate renewal", priority: "low", status: "completed", phase: 1, effortHours: 15, dueDate: "2026-03-15" },
  { taskId: "REM-011", assetId: "treasury.pnb.co.in", title: "Treasury system PQC migration", priority: "critical", status: "in_progress", phase: 1, effortHours: 90, dueDate: "2026-07-15" },
  { taskId: "REM-012", assetId: "forex.pnb.co.in", title: "Forex gateway quantum hardening", priority: "high", status: "pending", phase: 2, effortHours: 55, dueDate: "2026-10-15" },
];

export const MOCK_CERTS = [
  { certId: "QCERT-001", assetId: "swift.pnb.co.in", quantumScore: 95, algorithms: ["ML-KEM-768", "ML-DSA-65"], issuedAt: "2026-03-01", validUntil: "2027-03-01", status: "active", certificateHash: "a1b2c3d4e5f6789012345678901234567890abcdef", blockchainTx: "TX-HLF-98765-ABCDE", blockNumber: 98765, network: "Hyperledger Fabric" },
  { certId: "QCERT-002", assetId: "imps.pnb.co.in", quantumScore: 72, algorithms: ["X25519+Kyber768", "ECDSA-SHA384"], issuedAt: "2026-02-15", validUntil: "2027-02-15", status: "active", certificateHash: "b2c3d4e5f6789012345678901234567890abcdef12", blockchainTx: "TX-HLF-98764-BCDEF", blockNumber: 98764, network: "Hyperledger Fabric" },
  { certId: "QCERT-003", assetId: "treasury.pnb.co.in", quantumScore: 91, algorithms: ["ML-KEM-1024", "ML-DSA-87"], issuedAt: "2026-03-10", validUntil: "2027-03-10", status: "active", certificateHash: "c3d4e5f6789012345678901234567890abcdef1234", blockchainTx: "TX-HLF-98763-CDEFG", blockNumber: 98763, network: "Hyperledger Fabric" },
];

export const MOCK_ACTIVITY = [
  { id: 1, type: "scan", message: "Full scan completed — 128 assets analyzed", severity: "success", time: "2 min ago" },
  { id: 2, type: "alert", message: "Critical: 14 assets using RSA key exchange — quantum vulnerable", severity: "critical", time: "5 min ago" },
  { id: 3, type: "discovery", message: "CT Log Monitor: 3 new domains discovered under *.pnb.co.in", severity: "info", time: "12 min ago" },
  { id: 4, type: "remediation", message: "REM-002 in progress: Net banking PQC migration at 45%", severity: "info", time: "1 hr ago" },
  { id: 5, type: "certificate", message: "QCERT-003 issued for treasury.pnb.co.in — Score: 91", severity: "success", time: "6 hrs ago" },
  { id: 6, type: "alert", message: "HNDL Risk: netbanking.pnb.co.in liability ₹2,500 Cr", severity: "critical", time: "8 hrs ago" },
  { id: 7, type: "compliance", message: "ISO 27001:2022 A.8.24 quarterly audit — PASSED", severity: "success", time: "1 day ago" },
  { id: 8, type: "scan", message: "Weak cipher detected: TLS_RSA_WITH_DES_CBC_SHA on atm.pnb.co.in", severity: "critical", time: "1 day ago" },
  { id: 9, type: "certificate", message: "Certificate expiring soon: api.pnb.co.in (12 days)", severity: "warning", time: "2 days ago" },
  { id: 10, type: "discovery", message: "New asset confirmed: neft-api.pnb.co.in added to inventory", severity: "info", time: "3 days ago" },
];

// Topology graph nodes (for the network graph view)
export const GRAPH_NODES = MOCK_ASSETS.slice(0, 40).map((a, i) => ({
  id: a.domain, label: a.domain.split('.')[0], score: a.quantumScore, type: a.assetType,
  x: 100 + (i % 8) * 120 + Math.sin(i) * 30, y: 80 + Math.floor(i / 8) * 100 + Math.cos(i) * 20,
}));

export const GRAPH_EDGES = [
  ...MOCK_ASSETS.slice(0, 10).map(a => ({ source: a.domain, target: 'api.pnb.co.in' })),
  ...['upi.pnb.co.in','imps.pnb.co.in','neft.pnb.co.in','rtgs.pnb.co.in'].map(d => ({ source: d, target: 'swift.pnb.co.in' })),
  ...['loan.pnb.co.in','insurance.pnb.co.in','mutual.pnb.co.in','demat.pnb.co.in'].map(d => ({ source: d, target: 'api.pnb.co.in' })),
  { source: 'api.pnb.co.in', target: 'swift.pnb.co.in' },
  { source: 'api.pnb.co.in', target: 'treasury.pnb.co.in' },
  { source: 'mail.pnb.co.in', target: 'vpn.pnb.co.in' },
  { source: 'www.pnb.co.in', target: 'cdn.pnb.co.in' },
  { source: 'netbanking.pnb.co.in', target: 'api.pnb.co.in' },
  { source: 'mobile.pnb.co.in', target: 'api.pnb.co.in' },
  { source: 'portal.pnb.co.in', target: 'crm.pnb.co.in' },
  { source: 'sso.pnb.co.in', target: 'auth.pnb.co.in' },
  { source: 'auth.pnb.co.in', target: 'ldap.pnb.co.in' },
  { source: 'grafana.pnb.co.in', target: 'prometheus.pnb.co.in' },
  { source: 'siem.pnb.co.in', target: 'elk.pnb.co.in' },
].filter(e => GRAPH_NODES.find(n => n.id === e.source) && GRAPH_NODES.find(n => n.id === e.target));

// Cyber rating calculation
export const CYBER_RATING = (() => {
  const avgScore = MOCK_ASSETS.reduce((s, a) => s + a.quantumScore, 0) / MOCK_ASSETS.length;
  const tls13Pct = MOCK_ASSETS.filter(a => a.tlsVersion === '1.3').length / MOCK_ASSETS.length;
  const pqcPct = MOCK_ASSETS.filter(a => a.quantumScore >= 90).length / MOCK_ASSETS.length;
  const normalized = Math.round(avgScore * 3.5 + tls13Pct * 200 + pqcPct * 300);
  return {
    score: Math.min(1000, Math.max(0, normalized)),
    maxScore: 1000,
    tier: normalized >= 700 ? 'Elite-PQC' : normalized >= 400 ? 'Standard' : 'Legacy',
    breakdown: [
      { category: 'Quantum Score Average', value: Math.round(avgScore), max: 100, weight: 35 },
      { category: 'TLS 1.3 Adoption', value: Math.round(tls13Pct * 100), max: 100, weight: 20 },
      { category: 'PQC Algorithm Usage', value: Math.round(pqcPct * 100), max: 100, weight: 30 },
      { category: 'Certificate Health', value: 78, max: 100, weight: 15 },
    ],
  };
})();

// Utility functions
export function getScoreColor(score) {
  if (score >= 90) return '#22c55e';
  if (score >= 60) return '#eab308';
  if (score >= 30) return '#f97316';
  return '#ef4444';
}
export function getScoreLabel(score) {
  if (score >= 90) return 'Low Risk';
  if (score >= 60) return 'Moderate';
  if (score >= 30) return 'High Risk';
  return 'Severe';
}
export function getScoreClass(score) {
  if (score >= 90) return 'safe';
  if (score >= 60) return 'moderate';
  if (score >= 30) return 'high';
  return 'critical';
}
export function getRiskIcon(score) {
  if (score >= 90) return '🟢';
  if (score >= 60) return '🟡';
  if (score >= 30) return '🟠';
  return '🔴';
}
