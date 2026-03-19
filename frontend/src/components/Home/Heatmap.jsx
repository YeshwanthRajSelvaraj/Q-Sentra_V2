import React, { useRef, useEffect } from 'react';
import { MOCK_ASSETS, getScoreColor } from '../../mockData';

export default function Heatmap() {
  const mapRef = useRef(null);
  const mapInst = useRef(null);

  useEffect(() => {
    if (mapRef.current && !mapInst.current && window.L) {
      const map = window.L.map(mapRef.current, { zoomControl: false, attributionControl: false }).setView([22, 79], 4);
      window.L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 18 }).addTo(map);
      MOCK_ASSETS.forEach(a => {
        if (!a.latitude) return;
        const c = getScoreColor(a.quantumScore);
        const icon = window.L.divIcon({ className: '', html: `<div style="width:12px;height:12px;border-radius:50%;background:${c};box-shadow:0 0 10px ${c}90;border:2px solid rgba(255,255,255,0.3)"></div>`, iconSize: [12, 12] });
        window.L.marker([a.latitude, a.longitude], { icon }).bindPopup(`<div style="font-family:Inter;font-size:11px;background:#0f1629;color:white;padding:4px"><b>${a.domain}</b><br>Score: ${a.quantumScore} | ${a.keyExchange}<br>TLS ${a.tlsVersion} | ${a.city}</div>`).addTo(map);
      });
      mapInst.current = map;
    }
    return () => { if (mapInst.current) { mapInst.current.remove(); mapInst.current = null; } };
  }, []);

  return <div className="map-container" ref={mapRef} style={{ height: '360px', width: '100%', borderRadius: 12, overflow: 'hidden' }} />;
}
