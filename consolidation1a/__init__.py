import logging
import json
from Shared.db import engine
from sqlalchemy import text

def main(payload: str) -> dict:
    """
    1) invoice_id is a string like "a1VcW000003Wy2XUAS".
    2) We SELECT Payload from RawInvoice WHERE Id = :invoice_id
    3) json.loads(...) → original payload dict
    4) run the same parent/child “roll-up” on payload["Invoice_Details"]
    5) return {"Consolidated_Invoice": …, "Invoice_Details": […]}
    """
    invoice_id = payload

    # fetch raw JSON
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT Payload FROM RawInvoice WHERE Id = :iid"),
            {"iid": invoice_id}
        ).fetchone()

    if not row:
        raise ValueError(f"RawInvoice not found for Id={invoice_id}")

    raw_payload = row[0]
    if isinstance(raw_payload, str):
        payload = json.loads(raw_payload)
    else:
        payload = raw_payload

    logging.info("Consolidation1a IN (fetched from DB): %s", payload)

    consolidated = payload.get("Consolidated_Invoice", {})
    lines = payload.get("Invoice_Details", [])

    parents = [l.copy() for l in lines if not l.get("blng__RequiredBy__c")]

    sums = {}
    for l in lines:
        parent = l.get("blng__RequiredBy__c")
        if parent:
            amt = float(l.get("blng__TotalAmount__c") or 0)
            sums[parent] = sums.get(parent, 0) + amt

    for p in parents:
        pid = p.get("External_Order_Item_ID__c")
        if pid in sums:
            p["blng__TotalAmount__c"] = str(sums[pid])

    result = {
        "Consolidated_Invoice": consolidated,
        "Invoice_Details": parents
    }
    logging.info("Consolidation1a OUT: %s", result)
    return result
