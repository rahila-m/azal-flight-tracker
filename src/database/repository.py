import sqlite3
from typing import Optional, List, Dict, Any
from src.database.db import get_connection

def get_or_create_route(origin: str, destination: str, departure_date: str, target_price: Optional[float] = None) -> tuple[int, Optional[float]]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, target_price FROM tracked_routes 
        WHERE origin = ? AND destination = ? AND departure_date = ?
    """, (origin, destination, departure_date))
    row = cursor.fetchone()

    if row:
        route_id = row["id"]
        saved_target = row["target_price"]
        if target_price is not None and saved_target != target_price:
            cursor.execute("UPDATE tracked_routes SET target_price = ? WHERE id = ?", (target_price, route_id))
            conn.commit()
            saved_target = target_price
    else:
        cursor.execute("""
            INSERT INTO tracked_routes (origin, destination, departure_date, target_price)
            VALUES (?, ?, ?, ?)
        """, (origin, destination, departure_date, target_price))
        conn.commit()
        route_id = cursor.lastrowid
        saved_target = target_price

    conn.close()
    return route_id, saved_target

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

def get_all_routes() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, origin, destination, departure_date, target_price, is_active, created_at
        FROM tracked_routes
        ORDER BY created_at DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_price_history(route_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, price, currency, recorded_at
        FROM price_history
        WHERE route_id = ?
        ORDER BY recorded_at ASC
    """, (route_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
