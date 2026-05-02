#!/usr/bin/env python3
"""
csv_to_json.py — Orvian Colombia
Convierte pedidos.csv → data/pedidos.json para el reporte en GitHub Pages.

Uso:
    python scripts/csv_to_json.py

El script lee data/pedidos.csv y escribe data/pedidos.json.
Luego el workflow de GitHub Actions hace commit del JSON actualizado.
"""

import json
import csv
import os
import ast
from pathlib import Path

# Rutas relativas a la raíz del repositorio
BASE = Path(__file__).parent.parent
CSV_PATH = BASE / "data" / "pedidos.csv"
JSON_PATH = BASE / "data" / "pedidos.json"

# Campos numéricos (se convierten a int/float)
INT_FIELDS = {"valor", "costo", "ganancia", "recaudo", "intentos_entrega", "monto_reembolsado"}

# Campos booleanos
BOOL_FIELDS = {"nov_activa", "proceso_dev_completo"}

# Campos que son listas JSON (alertas_hist)
LIST_FIELDS = {"alertas_hist"}


def parse_value(key: str, raw: str):
    """Convierte un string CSV al tipo Python correcto."""
    val = raw.strip()

    # Lista JSON
    if key in LIST_FIELDS:
        if not val or val in ("", "[]", "null"):
            return []
        try:
            return json.loads(val)
        except Exception:
            try:
                return ast.literal_eval(val)
            except Exception:
                return []

    # Booleano
    if key in BOOL_FIELDS:
        return val.lower() in ("true", "1", "si", "sí", "yes")

    # Numérico
    if key in INT_FIELDS:
        if not val:
            return 0
        try:
            f = float(val.replace(",", ".").replace("$", "").replace(".", "").replace(",", "."))
            return int(f) if f == int(f) else f
        except ValueError:
            return 0

    # Vacío → None
    if val == "":
        return None

    return val


def convert():
    if not CSV_PATH.exists():
        print(f"[ERROR] No se encontró: {CSV_PATH}")
        return

    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Saltar filas vacías
            if not any(v.strip() for v in row.values()):
                continue
            parsed = {k: parse_value(k, v) for k, v in row.items()}
            rows.append(parsed)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(rows)} pedido(s) exportados → {JSON_PATH}")


if __name__ == "__main__":
    convert()
