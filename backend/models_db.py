import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Index
from backend.database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    role = Column(String(50), default="researcher")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ResourceMetricsDB(Base):
    __tablename__ = "resource_metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    storage_usage = Column(Float, default=0.0)
    network_usage = Column(Float, default=0.0)
    request_count = Column(Float, default=0.0)

    __table_args__ = (
        Index('idx_res_timestamp', 'timestamp'),
    )


class PredictionDB(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    model_name = Column(String(50), nullable=False)
    predicted_cpu = Column(Float, nullable=False)
    predicted_memory = Column(Float, nullable=False)
    prediction_horizon = Column(Integer, default=12)


class AnomalyDB(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    metric = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    anomaly_score = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)  # Normal, Warning, Critical


class OptimizationLogDB(Base):
    __tablename__ = "optimization_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    current_utilization = Column(Float, nullable=False)
    predicted_utilization = Column(Float, nullable=False)
    recommendation = Column(String(50), nullable=False)  # SCALE UP, MAINTAIN, SCALE DOWN
    reason = Column(Text, nullable=True)


class CostLogDB(Base):
    __tablename__ = "cost_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    current_cost = Column(Float, nullable=False)
    optimized_cost = Column(Float, nullable=False)
    estimated_savings = Column(Float, nullable=False)
