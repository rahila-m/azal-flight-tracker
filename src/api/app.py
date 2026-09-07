from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from src.database.repository import (
    get_all_routes, 
    get_price_history, 
    get_latest_price,
    get_or_create_route
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

app = FastAPI(
    title="AZAL Flight Tracker API",
    description="Automated price tracking and analytics API for Azerbaijan Airlines routes.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteCreateRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3, example="GYD")
    destination: str = Field(..., min_length=3, max_length=3, example="ADB")
    departure_date: str = Field(..., example="2026-10-20")
    target_price: Optional[float] = Field(None, gt=0, example=210.0)

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

@app.post("/api/routes", status_code=status.HTTP_201_CREATED, tags=["Routes"])
def add_new_route(route: RouteCreateRequest):
    origin = route.origin.upper().strip()
    dest = route.destination.upper().strip()
    
    if origin == dest:
        raise HTTPException(status_code=400, detail="Kalkış ve varış noktaları aynı olamaz.")
        
    route_id, target = get_or_create_route(
        origin=origin,
        destination=dest,
        departure_date=route.departure_date,
        target_price=route.target_price
    )
    return {
        "message": "Rota başarıyla eklendi.",
        "route_id": route_id,
        "origin": origin,
        "destination": dest,
        "departure_date": route.departure_date,
        "target_price": target
    }

@app.get("/api/routes/{route_id}/history", tags=["Analytics"])
def fetch_history(route_id: int):
    history = get_price_history(route_id)
    if not history:
        raise HTTPException(status_code=404, detail="Bu rota için henüz fiyat geçmişi bulunamadı.")
    return {
        "route_id": route_id,
        "count": len(history),
        "history": history
    }

# Web Dashboard Servisi
@app.get("/", include_in_schema=False)
def serve_dashboard():
    return FileResponse(BASE_DIR / "static" / "index.html")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")