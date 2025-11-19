"""
═══════════════════════════════════════════════════════════════════════════════
🎯 PROMETHEUS METRICS - Export de métriques MLOps
═══════════════════════════════════════════════════════════════════════════════
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
import os

# ═══════════════════════════════════════════════════════════════════════════
# 📊 MÉTRIQUES CUSTOM - Spécifiques au modèle CV cats/dogs
# ═══════════════════════════════════════════════════════════════════════════

database_status = Gauge(
    'cv_database_connected',
    'Database connection status (1=connected, 0=disconnected)'
)

# ═══════════════════════════════════════════════════════════════════════════
# 🔧 SETUP - Configuration de l'instrumentation Prometheus
# ═══════════════════════════════════════════════════════════════════════════
def setup_prometheus(app):
    """
    Configure Prometheus pour FastAPI
    Compatible avec l'API existante V2
    """
    if os.getenv('ENABLE_PROMETHEUS', 'false').lower() == 'true':
        Instrumentator().instrument(app).expose(app, endpoint="/metrics")
        print("✅ Prometheus metrics enabled at /metrics")
    else:
        print("ℹ️  Prometheus metrics disabled")

# ═══════════════════════════════════════════════════════════════════════════
# 📝 HELPERS - Fonctions de tracking appelées par l'API
# ═══════════════════════════════════════════════════════════════════════════

def update_db_status(is_connected: bool):
    """
    Met à jour le statut de la base de données
    """
    database_status.set(1 if is_connected else 0)