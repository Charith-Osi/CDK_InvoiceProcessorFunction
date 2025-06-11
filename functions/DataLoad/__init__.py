# DataLoad/__init__.py

import logging
import json
from db_utils.repository import SessionLocal
from db_utils.db         import engine
from sqlalchemy import text

def main(payload: dict) -> str:
    """
    1) payload is the exact JSON (header + details) that the orchestrator received.
    2) We insert it into RawInvoice (Id, Payload).
    3) Return the Id so that downstream activities only need that string.
    """

    header = payload.get("Consolidated_Invoice", {})
    invoice_id = header.get("Id")
    if not invoice_id:
        raise ValueError("No Consolidated_Invoice.Id found in payload")

    session = SessionLocal()
    try:
        # If a row with this Id already exists, skip (or you could overwrite if you prefer).
        existing = session.execute(
            text("SELECT 1 FROM RawInvoice WHERE Id = :iid"),
            {"iid": invoice_id}
        ).fetchone()

        if not existing:
            # store the raw JSON as a MySQL JSON string
            # We assume payload is JSON‐serializable:
            raw_json = json.dumps(payload)
            session.execute(
                text("INSERT INTO RawInvoice (Id, Payload) VALUES (:iid, CAST(:p AS JSON))"),
                {"iid": invoice_id, "p": raw_json}
            )
            session.commit()
            logging.info(f"DataLoad: inserted RawInvoice.Id = {invoice_id}")
        else:
            logging.info(f"DataLoad: RawInvoice.Id {invoice_id} already exists; skipping insert.")

        return invoice_id

    except Exception as e:
        session.rollback()
        logging.error("DataLoad ERROR: %s", e)
        raise

    finally:
        session.close()
