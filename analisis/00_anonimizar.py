"""
Fase 0 — Anonimización de inputs_raw/*.xlsx -> inputs_clean/*.parquet

Qué hace:
  1. Elimina columnas de identificación directa (PII) por nombre.
  2. Escanea columnas de texto libre y reemplaza emails, teléfonos y RUT por [PII_*].
  3. Agrega row_id estable (archivo + número de fila original) para citar sin nombres.
  4. Escribe un parquet por archivo en inputs_clean/.

Después de correr este script NO se vuelve a abrir inputs_raw/.
Nunca imprime filas crudas: solo conteos.

Cómo reproducirlo (desde la raíz del proyecto):
    python3 analisis/00_anonimizar.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "inputs_raw"
CLEAN = ROOT / "inputs_clean"

# Columnas que se eliminan completas (PII directa o nombres de personas).
DROP_COLS = {
    "email", "nombre", "teléfono", "telefono", "rut", "rut_cliente", "nombre_cliente",
    "correo_cliente", "telefono_cliente", "correo_electronico", "patente_vin", "vin",
    "nombre_recepcionista", "nombre_mecanico", "nombre_vendedor", "nombre_gerente",
    "nombre_ot", "url",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RUT_RE = re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")
PHONE_RE = re.compile(r"(?:\+?56\s?)?(?:9\s?\d{4}\s?\d{4}|\(?\d{2,3}\)?[\s-]?\d{3}[\s-]?\d{4})")
VIN_RE = re.compile(r"\b[A-HJ-NPR-Z0-9]{17}\b")


def scrub_text(value: object) -> object:
    if not isinstance(value, str):
        return value
    out = EMAIL_RE.sub("[PII_EMAIL]", value)
    out = RUT_RE.sub("[PII_RUT]", out)
    out = VIN_RE.sub("[PII_VIN]", out)
    out = PHONE_RE.sub("[PII_TEL]", out)
    return out


def clean_file(path: Path) -> dict:
    stats = {"archivo": path.name, "hojas": {}}
    sheets = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    for sheet, df in sheets.items():
        n_original = len(df)
        df = df.reset_index(drop=True)
        dropped = [c for c in df.columns if str(c).strip().lower() in DROP_COLS]
        df = df.drop(columns=dropped)
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].map(scrub_text)
                # Parquet exige tipos homogéneos en columnas object.
                df[col] = df[col].map(lambda v: None if pd.isna(v) else str(v))
        df.insert(0, "row_id", [f"{path.stem[:20]}#{i + 2}" for i in range(len(df))])
        out = CLEAN / f"{path.stem}__{re.sub(r'[^A-Za-z0-9]+', '_', sheet).strip('_').lower()}.parquet"
        df.to_parquet(out, index=False)
        stats["hojas"][sheet] = {
            "filas": n_original,
            "columnas_eliminadas_pii": len(dropped),
            "salida": out.name,
        }
    return stats


def main() -> None:
    CLEAN.mkdir(exist_ok=True)
    files = sorted(RAW.glob("*.xlsx"))
    if not files:
        raise SystemExit("No hay .xlsx en inputs_raw/")
    for f in files:
        s = clean_file(f)
        for sheet, info in s["hojas"].items():
            print(f"{s['archivo']} | {sheet} | filas={info['filas']} | pii_cols_eliminadas={info['columnas_eliminadas_pii']} -> {info['salida']}")


if __name__ == "__main__":
    main()
