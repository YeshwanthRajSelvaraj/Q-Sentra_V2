export const dashboardService = {
  getMetrics: async () => {
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/dashboard/metrics');
      if (!resp.ok) return null;
      return await resp.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  },
  getRecentActivity: async () => {
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/dashboard/recent-activity');
      if (!resp.ok) return [];
      return await resp.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },
  getGeoDistribution: async () => {
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/dashboard/geodistribution');
      if (!resp.ok) return [];
      return await resp.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },
  scanOnDemand: async (target) => {
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/scan/on-demand', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
      });
      return await resp.json();
    } catch (e) {
      console.error(e);
      return { error: e.message };
    }
  }
};
