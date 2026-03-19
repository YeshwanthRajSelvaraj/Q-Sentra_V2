-- ============================================================================
-- Q-Sentra Database Initialization
-- Punjab National Bank - Quantum-Proof Cryptographic Asset Management
-- ============================================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─── Users & RBAC ─────────────────────────────────────────────────────────
CREATE TYPE user_role AS ENUM ('admin', 'analyst', 'devops', 'auditor', 'readonly');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'readonly',
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    mfa_enabled BOOLEAN DEFAULT false,
    mfa_secret VARCHAR(255),
    last_login TIMESTAMPTZ,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Assets ───────────────────────────────────────────────────────────────
CREATE TYPE asset_status AS ENUM ('discovered', 'scanning', 'scanned', 'critical', 'warning', 'secure', 'quantum_safe');

CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(255) NOT NULL,
    ip_address INET,
    port INTEGER DEFAULT 443,
    asset_type VARCHAR(50) DEFAULT 'web',
    organization VARCHAR(255) DEFAULT 'Punjab National Bank',
    tls_version VARCHAR(10),
    cipher_suite VARCHAR(255),
    key_exchange VARCHAR(100),
    signature_algorithm VARCHAR(100),
    key_size INTEGER,
    certificate_issuer VARCHAR(255),
    certificate_expiry TIMESTAMPTZ,
    certificate_serial VARCHAR(255),
    quantum_score INTEGER DEFAULT 0,
    status asset_status DEFAULT 'discovered',
    is_public BOOLEAN DEFAULT true,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    last_scan_at TIMESTAMPTZ,
    discovered_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_assets_domain ON assets(domain);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_quantum_score ON assets(quantum_score);

-- ─── Scan History ─────────────────────────────────────────────────────────
CREATE TYPE scan_status AS ENUM ('queued', 'running', 'completed', 'failed', 'cancelled');
CREATE TYPE scan_type AS ENUM ('full', 'tls', 'pqc', 'discovery', 'cbom');

CREATE TABLE scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_id VARCHAR(100) UNIQUE NOT NULL,
    asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    scan_type scan_type NOT NULL DEFAULT 'full',
    status scan_status NOT NULL DEFAULT 'queued',
    initiated_by UUID REFERENCES users(id),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER,
    results JSONB,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_scans_asset_id ON scans(asset_id);
CREATE INDEX idx_scans_status ON scans(status);

-- ─── PQC Validation Results ──────────────────────────────────────────────
CREATE TABLE pqc_validations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    scan_id VARCHAR(100) REFERENCES scans(scan_id),
    tls_score DOUBLE PRECISION DEFAULT 0,
    kex_score DOUBLE PRECISION DEFAULT 0,
    sig_score DOUBLE PRECISION DEFAULT 0,
    keysize_score DOUBLE PRECISION DEFAULT 0,
    quantum_score INTEGER DEFAULT 0,
    risk_category VARCHAR(50),
    fips_203_compliant BOOLEAN DEFAULT false,
    fips_204_compliant BOOLEAN DEFAULT false,
    fips_205_compliant BOOLEAN DEFAULT false,
    nist_sp800_57_level VARCHAR(50),
    recommendations JSONB,
    validated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── HNDL Risk Assessment ────────────────────────────────────────────────
CREATE TABLE hndl_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    data_value INTEGER DEFAULT 5,
    exposure DOUBLE PRECISION DEFAULT 0.5,
    years_to_crqc DOUBLE PRECISION DEFAULT 8.0,
    hndl_risk_score DOUBLE PRECISION,
    liability_exposure_inr NUMERIC(15,2),
    attack_vector TEXT,
    mitigation_priority INTEGER,
    assessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Remediation Tasks ───────────────────────────────────────────────────
CREATE TYPE remediation_status AS ENUM ('pending', 'in_progress', 'completed', 'blocked', 'cancelled');
CREATE TYPE remediation_priority AS ENUM ('critical', 'high', 'medium', 'low');

CREATE TABLE remediation_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(100) UNIQUE NOT NULL,
    asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    priority remediation_priority DEFAULT 'medium',
    status remediation_status DEFAULT 'pending',
    phase INTEGER DEFAULT 1,
    effort_hours INTEGER,
    assigned_to UUID REFERENCES users(id),
    playbook_id VARCHAR(100),
    ansible_yaml TEXT,
    terraform_config TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    due_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_remediation_status ON remediation_tasks(status);
CREATE INDEX idx_remediation_priority ON remediation_tasks(priority);

-- ─── Quantum Safe Certificates ───────────────────────────────────────────
CREATE TYPE cert_status AS ENUM ('active', 'expired', 'revoked', 'pending');

CREATE TABLE quantum_certificates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cert_id VARCHAR(100) UNIQUE NOT NULL,
    asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    quantum_score INTEGER NOT NULL,
    algorithms TEXT[] NOT NULL,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_until TIMESTAMPTZ NOT NULL,
    status cert_status DEFAULT 'active',
    certificate_hash VARCHAR(128) NOT NULL,
    blockchain_tx VARCHAR(255),
    block_number BIGINT,
    blockchain_network VARCHAR(50) DEFAULT 'hyperledger',
    issuer VARCHAR(255) DEFAULT 'Q-Sentra PNB Authority',
    subject_info JSONB,
    verification_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_certs_asset_id ON quantum_certificates(asset_id);
CREATE INDEX idx_certs_status ON quantum_certificates(status);

-- ─── Audit Log ───────────────────────────────────────────────────────────
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    hmac_signature VARCHAR(128),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id);

-- ─── Network Topology Edges ─────────────────────────────────────────────
CREATE TABLE network_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    target_asset_id VARCHAR(255) REFERENCES assets(asset_id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) DEFAULT 'depends_on',
    weight DOUBLE PRECISION DEFAULT 1.0,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── System Configuration ────────────────────────────────────────────────
CREATE TABLE system_config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════
-- SEED DATA
-- ═══════════════════════════════════════════════════════════════════════════

-- Default Admin User (password: QSentra@Admin2026)
INSERT INTO users (username, email, password_hash, full_name, role, department) VALUES
('admin', 'admin@pnb.co.in', '$2b$12$LJ3m4VKcK6fH1T5PsRQxZOYFGz5KGHxKpGvLcRuFkByNm6a9HmJqe', 'System Administrator', 'admin', 'Cybersecurity'),
('analyst01', 'analyst@pnb.co.in', '$2b$12$LJ3m4VKcK6fH1T5PsRQxZOYFGz5KGHxKpGvLcRuFkByNm6a9HmJqe', 'Security Analyst', 'analyst', 'SOC'),
('devops01', 'devops@pnb.co.in', '$2b$12$LJ3m4VKcK6fH1T5PsRQxZOYFGz5KGHxKpGvLcRuFkByNm6a9HmJqe', 'DevOps Engineer', 'devops', 'Infrastructure'),
('auditor01', 'auditor@pnb.co.in', '$2b$12$LJ3m4VKcK6fH1T5PsRQxZOYFGz5KGHxKpGvLcRuFkByNm6a9HmJqe', 'Compliance Auditor', 'auditor', 'Compliance');

-- Simulated PNB Assets (10 sample assets with realistic data)
INSERT INTO assets (asset_id, domain, ip_address, port, asset_type, tls_version, cipher_suite, key_exchange, signature_algorithm, key_size, certificate_issuer, certificate_expiry, quantum_score, status, is_public, latitude, longitude) VALUES
('web01.pnb.co.in', 'web01.pnb.co.in', '203.123.45.67', 443, 'web', '1.2', 'TLS_RSA_WITH_AES_128_CBC_SHA', 'RSA', 'RSA-SHA256', 2048, 'DigiCert', '2026-12-31T23:59:59Z', 15, 'critical', true, 28.6139, 77.2090),
('netbanking.pnb.co.in', 'netbanking.pnb.co.in', '203.123.45.68', 443, 'web', '1.2', 'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384', 'ECDHE', 'RSA-SHA256', 2048, 'DigiCert', '2026-09-15T23:59:59Z', 25, 'critical', true, 28.6139, 77.2090),
('api.pnb.co.in', 'api.pnb.co.in', '203.123.45.69', 443, 'api', '1.3', 'TLS_AES_256_GCM_SHA384', 'X25519', 'ECDSA-SHA384', 384, 'Let''s Encrypt', '2026-06-30T23:59:59Z', 45, 'warning', true, 28.6139, 77.2090),
('mobile.pnb.co.in', 'mobile.pnb.co.in', '203.123.45.70', 443, 'mobile_api', '1.3', 'TLS_AES_128_GCM_SHA256', 'X25519', 'ECDSA-SHA256', 256, 'DigiCert', '2027-03-31T23:59:59Z', 40, 'warning', true, 19.0760, 72.8777),
('vpn.pnb.co.in', 'vpn.pnb.co.in', '203.123.45.71', 443, 'vpn', '1.2', 'TLS_RSA_WITH_AES_256_CBC_SHA256', 'RSA', 'RSA-SHA256', 4096, 'Internal CA', '2027-06-30T23:59:59Z', 20, 'critical', false, 28.6139, 77.2090),
('mail.pnb.co.in', 'mail.pnb.co.in', '203.123.45.72', 443, 'email', '1.2', 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256', 'ECDHE', 'RSA-SHA256', 2048, 'GlobalSign', '2026-11-30T23:59:59Z', 30, 'warning', true, 28.6139, 77.2090),
('upi.pnb.co.in', 'upi.pnb.co.in', '203.123.45.73', 443, 'payment', '1.3', 'TLS_CHACHA20_POLY1305_SHA256', 'X25519', 'ECDSA-SHA384', 384, 'DigiCert', '2027-01-15T23:59:59Z', 50, 'warning', true, 12.9716, 77.5946),
('imps.pnb.co.in', 'imps.pnb.co.in', '203.123.45.74', 443, 'payment', '1.3', 'TLS_AES_256_GCM_SHA384', 'X25519+Kyber768', 'ECDSA-SHA384', 384, 'DigiCert', '2027-03-31T23:59:59Z', 72, 'scanned', true, 28.6139, 77.2090),
('swift.pnb.co.in', 'swift.pnb.co.in', '203.123.45.75', 443, 'banking_core', '1.3', 'TLS_AES_256_GCM_SHA384', 'ML-KEM-768', 'ML-DSA-65', 768, 'PNB Internal CA', '2028-01-01T23:59:59Z', 95, 'quantum_safe', false, 28.6139, 77.2090),
('cdn.pnb.co.in', 'cdn.pnb.co.in', '203.123.45.76', 443, 'cdn', '1.3', 'TLS_AES_128_GCM_SHA256', 'X25519', 'RSA-SHA256', 2048, 'Cloudflare', '2026-08-31T23:59:59Z', 35, 'warning', true, 22.5726, 88.3639);

-- Network Topology Edges
INSERT INTO network_edges (source_asset_id, target_asset_id, relationship_type, weight) VALUES
('web01.pnb.co.in', 'api.pnb.co.in', 'depends_on', 0.9),
('netbanking.pnb.co.in', 'api.pnb.co.in', 'depends_on', 0.95),
('mobile.pnb.co.in', 'api.pnb.co.in', 'depends_on', 0.9),
('api.pnb.co.in', 'swift.pnb.co.in', 'depends_on', 1.0),
('api.pnb.co.in', 'upi.pnb.co.in', 'depends_on', 0.85),
('api.pnb.co.in', 'imps.pnb.co.in', 'depends_on', 0.85),
('upi.pnb.co.in', 'swift.pnb.co.in', 'depends_on', 0.95),
('imps.pnb.co.in', 'swift.pnb.co.in', 'depends_on', 0.95),
('mail.pnb.co.in', 'vpn.pnb.co.in', 'connects_to', 0.5),
('web01.pnb.co.in', 'cdn.pnb.co.in', 'served_by', 0.7);

-- HNDL Risk Assessments
INSERT INTO hndl_assessments (asset_id, data_value, exposure, years_to_crqc, hndl_risk_score, liability_exposure_inr, attack_vector, mitigation_priority) VALUES
('web01.pnb.co.in', 7, 0.9, 7.0, 96.4, 500000000.00, 'Public web portal → RSA key harvest → Future decryption of session data', 1),
('netbanking.pnb.co.in', 10, 0.95, 7.0, 101.8, 2500000000.00, 'Net banking session → RSA-2048 KEX harvest → Account data decryption', 1),
('api.pnb.co.in', 8, 0.8, 7.0, 62.9, 800000000.00, 'API gateway → X25519 KEX → Post-quantum key recovery', 2),
('vpn.pnb.co.in', 9, 0.3, 7.0, 30.9, 400000000.00, 'VPN tunnel harvest → Internal network decryption', 2),
('upi.pnb.co.in', 10, 0.9, 7.0, 64.3, 3000000000.00, 'UPI transactions → ECDHE harvest → Payment data exposure', 1),
('swift.pnb.co.in', 10, 0.1, 7.0, 0.7, 50000000.00, 'Low risk - ML-KEM-768 quantum-safe', 4);

-- Remediation Tasks
INSERT INTO remediation_tasks (task_id, asset_id, title, description, priority, status, phase, effort_hours, due_date) VALUES
('REM-001', 'web01.pnb.co.in', 'Upgrade web01 to TLS 1.3 with ML-KEM', 'Replace RSA key exchange with ML-KEM-768, upgrade TLS to 1.3, deploy hybrid certificate', 'critical', 'pending', 1, 40, '2026-06-30T23:59:59Z'),
('REM-002', 'netbanking.pnb.co.in', 'Migrate net banking to quantum-safe TLS', 'Full PQC migration: ML-KEM-768 KEX, ML-DSA-65 signatures, update load balancers', 'critical', 'in_progress', 1, 80, '2026-07-31T23:59:59Z'),
('REM-003', 'api.pnb.co.in', 'API gateway PQC upgrade', 'Enable X25519+Kyber768 hybrid mode, update API gateway certificates', 'high', 'pending', 2, 60, '2026-09-30T23:59:59Z'),
('REM-004', 'vpn.pnb.co.in', 'VPN quantum-safe migration', 'Migrate VPN from RSA to ML-KEM, implement IKEv2 with PQC extensions', 'high', 'pending', 2, 50, '2026-10-31T23:59:59Z'),
('REM-005', 'upi.pnb.co.in', 'UPI payment gateway PQC hardening', 'Implement hybrid X25519+Kyber768, ML-DSA signatures for transaction signing', 'critical', 'pending', 1, 100, '2026-08-31T23:59:59Z'),
('REM-006', 'mail.pnb.co.in', 'Email server TLS upgrade', 'Upgrade mail server TLS, implement S/MIME with PQC algorithms', 'medium', 'pending', 3, 30, '2026-12-31T23:59:59Z'),
('REM-007', 'cdn.pnb.co.in', 'CDN edge PQC configuration', 'Configure Cloudflare PQC support, enable hybrid key exchange', 'medium', 'pending', 3, 20, '2027-01-31T23:59:59Z'),
('REM-008', 'mobile.pnb.co.in', 'Mobile API PQC integration', 'Update mobile SDK for PQC support, implement certificate pinning with PQC certs', 'high', 'in_progress', 2, 70, '2026-09-30T23:59:59Z'),
('REM-009', 'imps.pnb.co.in', 'IMPS gateway optimization', 'Optimize existing Kyber768 implementation, add ML-DSA signatures', 'low', 'completed', 1, 25, '2026-04-30T23:59:59Z');

-- Quantum Safe Certificates
INSERT INTO quantum_certificates (cert_id, asset_id, quantum_score, algorithms, issued_at, valid_until, status, certificate_hash, blockchain_tx, block_number) VALUES
('QCERT-001', 'swift.pnb.co.in', 95, ARRAY['ML-KEM-768', 'ML-DSA-65'], '2026-03-01T00:00:00Z', '2027-03-01T00:00:00Z', 'active', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678', 'TX-HLF-98765-ABCDE', 98765),
('QCERT-002', 'imps.pnb.co.in', 72, ARRAY['X25519+Kyber768', 'ECDSA-SHA384'], '2026-02-15T00:00:00Z', '2027-02-15T00:00:00Z', 'active', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456789a', 'TX-HLF-98764-BCDEF', 98764);

-- System configuration
INSERT INTO system_config (key, value, description) VALUES
('scan_interval_hours', '6', 'CT log monitoring interval in hours'),
('max_concurrent_scans', '10', 'Maximum concurrent scan jobs'),
('quantum_score_weights', '{"tls": 20, "kex": 35, "sig": 30, "keysize": 15}', 'Quantum score formula weights'),
('hndl_years_to_crqc', '7', 'Estimated years to cryptographically relevant quantum computer'),
('blockchain_network', '"hyperledger"', 'Active blockchain network for cert anchoring'),
('alert_thresholds', '{"critical": 30, "warning": 60, "info": 90}', 'Score thresholds for alerts');
