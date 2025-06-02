import logging
from Shared.models import InvoiceHeader, InvoiceDetail, InvoicePayload
from Shared.repository import InvoiceRepository

def main(payload: dict):
    """
    Persist the final JSON payload—first header, then detail lines—
    using repository classes in shared/.
    """
    invoice_payload = InvoicePayload.parse_obj(payload)

    repo = InvoiceRepository()

    try:
        # repo.upsert_header(invoice_payload.Consolidated_Invoice)

        # repo.delete_details_for_header(invoice_payload.Consolidated_Invoice.Id)

        repo.insert_details(
            invoice_payload.Consolidated_Invoice.Id,
            invoice_payload.Invoice_Details
        )

        repo.commit_and_close()
        logging.info(
            "Successfully saved invoice %s with %d lines.",
            invoice_payload.Consolidated_Invoice.Id,
            len(invoice_payload.Invoice_Details)
        )
    except Exception as e:
        logging.exception("Error saving to DB: %s", e)
        raise

    return {"status": "OK", "Invoice_Id": invoice_payload.Consolidated_Invoice.Id}
