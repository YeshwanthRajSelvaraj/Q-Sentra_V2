"""Domain models for PostgreSQL."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base

class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    hostname = Column(String(255), nullable=False)
    ip_address = Column(INET)
    asset_type = Column(String(50))
    company_name = Column(String(100), default='PNB')
    registrar = Column(String(255))
    registration_date = Column(Date)
    detection_date = Column(DateTime, server_default=func.current_timestamp())
    status = Column(String(20), default='confirmed')
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class DiscoveryQueue(Base):
    __tablename__ = 'discovery_queue'

    id = Column(Integer, primary_key=True)
    hostname = Column(String(255), nullable=False)
    ip_address = Column(INET)
    source = Column(String(50))
    first_seen = Column(DateTime, server_default=func.current_timestamp())
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, server_default=func.current_timestamp())

class CBOM(Base):
    __tablename__ = 'cbom'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    hostname = Column(String(255), nullable=False)
    scan_timestamp = Column(DateTime, server_default=func.current_timestamp())
    cbom_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

class PQCScore(Base):
    __tablename__ = 'pqc_scores'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    score = Column(Integer, nullable=False)
    confidence = Column(Float)
    shap_explanation = Column(JSONB)
    model_version = Column(String(50))
    scanned_at = Column(DateTime, server_default=func.current_timestamp())

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    activity_type = Column(String(50))
    description = Column(String)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    created_at = Column(DateTime, server_default=func.current_timestamp())

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    report_type = Column(String(50))
    file_path = Column(String(500))
    created_at = Column(DateTime, server_default=func.current_timestamp())
