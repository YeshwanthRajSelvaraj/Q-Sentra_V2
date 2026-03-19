import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/Home/Dashboard';
import Assets from './pages/Assets';
import AssetDiscovery from './pages/AssetDiscovery';
import CbomDashboard from './pages/CbomDashboard';
import PosturePQC from './pages/PosturePQC';
import BlastRadius from './pages/BlastRadius';
import CyberRating from './pages/CyberRating';
import Remediation from './pages/Remediation';
import Certificates from './pages/Certificates';
import Compliance from './pages/Compliance';
import Reporting from './pages/Reporting';
import Login from './pages/Login';
import Verify from './pages/Verify';

export default function App() {
  const [isAuth, setIsAuth] = useState(!!localStorage.getItem('qsentra_token'));
  const [currentPage, setCurrentPage] = useState('dashboard');

  if (window.location.pathname.startsWith('/verify/')) {
    return <BrowserRouter><Routes><Route path="/verify/:assetId" element={<Verify />} /></Routes></BrowserRouter>;
  }

  if (!isAuth) return <Login onLogin={() => setIsAuth(true)} />;

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
        <div className="main-content">
          <Header currentPage={currentPage} onLogout={() => { localStorage.removeItem('qsentra_token'); setIsAuth(false); }} />
          <div className="page-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/assets" element={<Assets />} />
              <Route path="/discovery" element={<AssetDiscovery />} />
              <Route path="/cbom" element={<CbomDashboard />} />
              <Route path="/posture" element={<PosturePQC />} />
              <Route path="/blast-radius" element={<BlastRadius />} />
              <Route path="/cyber-rating" element={<CyberRating />} />
              <Route path="/remediation" element={<Remediation />} />
              <Route path="/certificates" element={<Certificates />} />
              <Route path="/compliance" element={<Compliance />} />
              <Route path="/reporting" element={<Reporting />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      </div>
    </BrowserRouter>
  );
}
