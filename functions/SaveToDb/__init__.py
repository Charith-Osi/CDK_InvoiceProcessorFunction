# SaveToDb/__init__.py

import logging
from db_utils.repository import SessionLocal
from db_utils.models    import InvoiceHeaderORM, InvoiceDetailORM

def main(payload: dict) -> None:
    """
    payload is a Python dict (Durable Function activityTrigger)
    whose shape is exactly your invoice JSON (header + details).
    """

    logging.info("SaveToDb received payload:\n%s", payload)

    header_data = payload.get("Consolidated_Invoice", {})
    details_data = payload.get("Invoice_Details", [])

    session = SessionLocal()

    try:
        hdr = InvoiceHeaderORM(
            Id                      = header_data["Id"],
            Name                    = header_data.get("Name"),
            FIN_Invoice_Date__c     = header_data.get("FIN_Invoice_Date__c")
                                         and __parse_date(header_data["FIN_Invoice_Date__c"]),
            Total_Amount__c         = header_data.get("Total_Amount__c"),
            FIN_Due_Date__c         = header_data.get("FIN_Due_Date__c")
                                         and __parse_date(header_data["FIN_Due_Date__c"]),
            Dispute_Comments__c     = header_data.get("Dispute_Comments__c"),
            CID_Cancelled__c        = header_data.get("CID_Cancelled__c"),
            blng__InvoiceBatches__c = header_data.get("blng__InvoiceBatches__c"),
            Bill_To_Account_SF_Id   = header_data.get("Bill_To_Account_SF_Id"),
            Bill_To_AccountNumber   = header_data.get("Bill_To_AccountNumber"),
            Bill_To_AccountName     = header_data.get("Bill_To_AccountName"),
            BillingCity             = header_data.get("BillingCity"),
            BillingState            = header_data.get("BillingState"),
            BillingPostalCode       = header_data.get("BillingPostalCode"),
            BillingStreet           = header_data.get("BillingStreet"),
            Email_List              = header_data.get("Email_List"),
            FIN_Langauge__c         = header_data.get("FIN_Langauge__c"),
            FIN_Invoice_Delivery_Method__c = header_data.get("FIN_Invoice_Delivery_Method__c"),
        )

        details_objs = []
        for d in details_data:
            dt = InvoiceDetailORM(
                Header_Id                    = header_data["Id"],
                Invoice_SF_Id                = d.get("Invoice_SF_Id"),
                Invoice_Number               = d.get("Invoice_Number"),
                Invoice_Date                 = d.get("Invoice_Date")
                                                  and __parse_date(d["Invoice_Date"]),
                Invoice_Line_SF_Id           = d.get("Invoice_Line_SF_Id"),
                FIN_Invoice_Ship_to_Account__c = d.get("FIN_Invoice_Ship_to_Account__c"),
                Ship_To_AccountNumber        = d.get("Ship_To_AccountNumber"),
                Ship_To_AccountName          = d.get("Ship_To_AccountName"),
                blng__BillingFrequency__c    = d.get("blng__BillingFrequency__c"),
                Order_Product_SF_ID          = d.get("Order_Product_SF_ID"),
                Contract_Line__c             = d.get("Contract_Line__c"),
                External_Order_Item_ID__c    = d.get("External_Order_Item_ID__c"),
                blng__RequiredBy__c          = d.get("blng__RequiredBy__c"),
                blng__Notes__c               = d.get("blng__Notes__c"),
                Product_SF_ID                = d.get("Product_SF_ID"),
                ProductCode                  = d.get("ProductCode"),
                Description                  = d.get("Description"),
                blng__ChargeType__c          = d.get("blng__ChargeType__c"),
                blng__Quantity__c            = float(d.get("blng__Quantity__c") or 0),
                blng__Subtotal__c            = float(d.get("blng__Subtotal__c") or 0),
                blng__TaxAmount__c           = float(d.get("blng__TaxAmount__c") or 0),
                blng__TotalAmount__c         = float(d.get("blng__TotalAmount__c") or 0),
            )
            details_objs.append(dt)

        session.add(hdr)
        session.add_all(details_objs)
        session.commit()
        logging.info("SaveToDb: insert succeeded for header id %s", header_data["Id"])
    except Exception as e:
        session.rollback()
        logging.error("SaveToDb ERROR: %s", e)
        raise
    finally:
        session.close()


def __parse_date(date_str: str):
    """Helper: convert 'YYYY-MM-DD' → python.date"""
    from datetime import datetime
    return datetime.strptime(date_str, "%Y-%m-%d").date()
