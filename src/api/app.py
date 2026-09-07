from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.database.repository import get_all_routes, get_price_history, get_latest_price

app = FastAPI(
    title="AZAL Flight Tracker API",
    description="Automated price tracking and analytics API for Azerbaijan Airlines routes.",
    version="1.0.0"
)

# Frontend entegrasyonu (React/Vue vb.) için CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "azal-flight-tracker"}

@app.get("/api/routes", tags=["Routes"])
def list_routes():
    routes = get_all_routes()
    result = []
    for r in routes:
        latest = get_latest_price(r["id"])
        result.append({
            **r,
            "latest_price": latest
        })
    return {"routes": result}

@app.get("/api/routes/{route_id}/history", tags=["Analytics"])
def fetch_history(route_id: int):
    history = get_price_history(route_id)
    if not history:
        raise HTTPException(status_code=404, detail="Bu rota için fiyat geçmişi bulunamadı.")
    return {
        "route_id": route_id,
        "count": len(history),
        "history": history
    }
