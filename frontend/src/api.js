const API_BASE = '/api/v1';

async function fetchApi(endpoint, options = {}) {
  const token = localStorage.getItem('qsentra_token');
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

export const api = {
  // Auth
  login: (data) => fetchApi('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  // Dashboard
  getDashboard: () => fetchApi('/dashboard/overview'),
  getCompliance: () => fetchApi('/dashboard/compliance'),
  // Assets
  getAssets: (params = '') => fetchApi(`/assets${params}`),
  getAssetStats: () => fetchApi('/assets/stats'),
  getAsset: (id) => fetchApi(`/assets/${id}`),
  // Scans
  startScan: (data) => fetchApi('/scans', { method: 'POST', body: JSON.stringify(data) }),
  getScans: () => fetchApi('/scans'),
  // CBOM
  getCbom: (id) => fetchApi(`/cbom/${id}`),
  getCboms: () => fetchApi('/cbom'),
  // PQC
  validateAsset: (id) => fetchApi(`/pqc/validate/${id}`),
  validateAll: () => fetchApi('/pqc/validate-all'),
  getStandards: () => fetchApi('/pqc/standards'),
  // Risk
  getHndlRisks: () => fetchApi('/risk/hndl'),
  getBlastRadius: () => fetchApi('/risk/blast-radius'),
  getThreatIntel: () => fetchApi('/risk/threat-intel'),
  // Remediation
  getTasks: () => fetchApi('/remediation'),
  getRoadmap: () => fetchApi('/remediation/roadmap'),
  getPlaybook: (id) => fetchApi(`/remediation/${id}/playbook`),
  updateTask: (id, data) => fetchApi(`/remediation/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  // Certificates
  getCertificates: () => fetchApi('/certificates'),
  getCertificate: (id) => fetchApi(`/certificates/${id}`),
  verifyCert: (id) => fetchApi(`/certificates/${id}/verify`),
  // Discovery
  getCtLogs: () => fetchApi('/discovery/ct-logs'),
  triggerDiscovery: () => fetchApi('/discovery/trigger', { method: 'POST' }),
  // Public verify
  verifyAsset: (id) => fetchApi(`/verify/${id}`),
};

export default api;
