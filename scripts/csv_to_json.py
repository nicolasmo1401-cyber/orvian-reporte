#!/usr/bin/env python3
import json
import csv
from pathlib import Path

BASE = Path(__file__).parent.parent
CSV_PATH = BASE / "data" / "pedidos.csv"
JSON_PATH = BASE / "data" / "pedidos.json"

INT_FIELDS = {"valor", "costo", "ganancia", "recaudo", "intentos_entrega", "monto_reembolsado"}
BOOL_FIELDS = {"nov_activa", "proceso_dev_completo"}
LIST_FIELDS = {"alertas_hist"}

def parse_value(key, raw):
    if not isinstance(raw, str):
        raw = "" if raw is None else str(raw)
    val = raw.strip()
    if key in LIST_FIELDS:
        if not val or val in ("", "[]", "null"):
            return []
        try:
            return json.loads(val)
        except Exception:
            return []
    if key in BOOL_FIELDS:
        return val.lower() in ("true", "1", "si", "sí", "yes")
    if key in INT_FIELDS:
        if not val:
            return 0
        try:
            return int(float(val.replace("$", "").replace(" ", "")))
        except ValueError:
            return 0
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
            clean = {k: v for k, v in row.items() if k is not None}
            if not any(str(v).strip() for v in clean.values()):
                continue
            parsed = {k: parse_value(k, v) for k, v in clean.items()}
            rows.append(parsed)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(rows)} pedido(s) exportados → {JSON_PATH}")

if __name__ == "__main__":
    convert()
