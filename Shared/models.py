# shared/models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class InvoiceHeader(BaseModel):
    Id: str = Field(..., description="Primary key for the invoice")
    Name: Optional[str]
    FIN_Invoice_Date__c: Optional[date]
    Total_Amount__c: Optional[float]
    FIN_Due_Date__c: Optional[date]
    Dispute_Comments__c: Optional[str]
    CID_Cancelled__c: Optional[bool]
    blng__InvoiceBatches__c: Optional[str]
    Bill_To_Account_SF_Id: Optional[str]
    Bill_To_AccountNumber: Optional[str]
    Bill_To_AccountName: Optional[str]
    BillingCity: Optional[str]
    BillingState: Optional[str]
    BillingPostalCode: Optional[str]
    BillingStreet: Optional[str]
    Email_List: Optional[str]
    FIN_Langauge__c: Optional[str]
    FIN_Invoice_Delivery_Method__c: Optional[str]

class InvoiceDetail(BaseModel):
    Invoice_SF_Id:        Optional[str]
    Invoice_Number:       Optional[str]
    Invoice_Date:         Optional[date]
    Invoice_Line_SF_Id:   Optional[str]
    FIN_Invoice_Ship_to_Account__c: Optional[str]
    Ship_To_AccountNumber: Optional[str]
    Ship_To_AccountName:   Optional[str]
    blng__BillingFrequency__c: Optional[str]
    Order_Product_SF_ID:   Optional[str]
    Contract_Line__c:      Optional[str]
    External_Order_Item_ID__c: Optional[str]
    blng__RequiredBy__c:   Optional[str]
    blng__Notes__c:        Optional[str]
    Product_SF_ID:         Optional[str]
    ProductCode:           Optional[str]
    Description:           Optional[str]
    blng__ChargeType__c:   Optional[str]
    blng__Quantity__c:     Optional[str]
    blng__Subtotal__c:     Optional[str]
    blng__TaxAmount__c:    Optional[str]
    blng__TotalAmount__c:  Optional[str]

class InvoicePayload(BaseModel):
    Consolidated_Invoice: InvoiceHeader
    Invoice_Details: List[InvoiceDetail]
