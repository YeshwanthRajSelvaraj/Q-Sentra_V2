-- Assets inventory
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    ip_address INET,
    asset_type VARCHAR(50), -- domain, ip, subnet
    company_name VARCHAR(100) DEFAULT 'PNB',
    registrar VARCHAR(255),
    registration_date DATE,
    detection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'confirmed', -- confirmed, new, false_positive
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discovery queue
CREATE TABLE IF NOT EXISTS discovery_queue (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    ip_address INET,
    source VARCHAR(50), -- CT_LOG, DNS, REVERSE
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, ignored
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CBOM data
CREATE TABLE IF NOT EXISTS cbom (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id),
    hostname VARCHAR(255) NOT NULL,
    scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cbom_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PQC Scores
CREATE TABLE IF NOT EXISTS pqc_scores (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id),
    score INTEGER NOT NULL,
    confidence FLOAT,
    shap_explanation JSONB,
    model_version VARCHAR(50),
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activities for dashboard
CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    activity_type VARCHAR(50),
    description TEXT,
    asset_id INTEGER REFERENCES assets(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR(50),
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
