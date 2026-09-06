import sqlite3
from typing import Optional
from src.database.db import get_connection

def get_or_create_route(origin: str, destination: str, departure_date: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tracked_routes 
        WHERE origin = ? AND destination = ? AND departure_date = ?
    """, (origin, destination, departure_date))
    row = cursor.fetchone()

    if row:
        route_id = row["id"]
    else:
        cursor.execute("""
            INSERT INTO tracked_routes (origin, destination, departure_date)
            VALUES (?, ?, ?)
        """, (origin, destination, departure_date))
        conn.commit()
        route_id = cursor.lastrowid

    conn.close()
    return route_id

def get_latest_price(route_id: int) -> Optional[float]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT price FROM price_history
        WHERE route_id = ?
        ORDER BY recorded_at DESC, id DESC
        LIMIT 1
    """, (route_id,))
    row = cursor.fetchone()
    conn.close()
    return row["price"] if row else None

def save_price(route_id: int, price: float, currency: str = "AZN") -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO price_history (route_id, price, currency)
        VALUES (?, ?, ?)
    """, (route_id, price, currency))
    conn.commit()
    conn.close()
