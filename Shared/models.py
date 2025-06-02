# shared/models.py

from sqlalchemy import (
    Column, String, Date, Boolean, DECIMAL, Integer, Text, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class InvoiceHeaderORM(Base):
    __tablename__ = "invoiceheader"  # make sure this matches your lowercase-or-camel case accordingly

    Id                         = Column(String(32), primary_key=True)
    Name                       = Column(String(32))
    FIN_Invoice_Date__c        = Column("FIN_Invoice_Date", Date)
    Total_Amount__c            = Column("Total_Amount", DECIMAL(12,2))
    FIN_Due_Date__c            = Column("FIN_Due_Date", Date)
    Dispute_Comments__c        = Column("Dispute_Comments", Text)
    CID_Cancelled__c           = Column("CID_Cancelled", Boolean)
    blng__InvoiceBatches__c    = Column("blng_InvoiceBatches", String(16))
    Bill_To_Account_SF_Id      = Column(String(32))
    Bill_To_AccountNumber      = Column(String(32))
    Bill_To_AccountName        = Column(String(64))
    BillingCity                = Column(String(64))
    BillingState               = Column(String(8))
    BillingPostalCode          = Column(String(16))
    BillingStreet              = Column(String(128))
    Email_List                 = Column(String(256))
    FIN_Langauge__c            = Column("FIN_Language", String(32))
    FIN_Invoice_Delivery_Method__c = Column("FIN_Invoice_Delivery", String(16))

    # Backref relationship
    details = relationship("InvoiceDetailORM", back_populates="header", cascade="all, delete-orphan")


class InvoiceDetailORM(Base):
    __tablename__ = "invoicedetail"

    Line_Id                    = Column(Integer, primary_key=True, autoincrement=True)
    Header_Id                  = Column(String(32), ForeignKey("invoiceheader.Id"))
    Invoice_SF_Id              = Column(String(32))
    Invoice_Number             = Column(String(32))
    Invoice_Date               = Column(Date)
    Invoice_Line_SF_Id         = Column(String(32))
    FIN_Invoice_Ship_to_Account__c = Column(String(255), nullable=True)
    Ship_To_AccountNumber      = Column(String(32))
    Ship_To_AccountName        = Column(String(64))
    blng__BillingFrequency__c  = Column("blng_BillingFrequency", String(16))
    Order_Product_SF_ID        = Column(String(32))
    Contract_Line__c           = Column("Contract_Line", String(32))
    External_Order_Item_ID__c  = Column("External_Order_Item_ID", String(32))
    blng__RequiredBy__c        = Column("blng_RequiredBy", String(32))
    blng__Notes__c             = Column("blng_Notes", Text)
    Product_SF_ID              = Column(String(32))
    ProductCode                = Column(String(32))
    Description                = Column(String(128))
    blng__ChargeType__c        = Column("blng_ChargeType", String(16))
    blng__Quantity__c          = Column("blng_Quantity", DECIMAL(12,2))
    blng__Subtotal__c          = Column("blng_Subtotal", DECIMAL(12,2))
    blng__TaxAmount__c         = Column("blng_TaxAmount", DECIMAL(12,2))
    blng__TotalAmount__c       = Column("blng_TotalAmount", DECIMAL(12,2))

    header = relationship("InvoiceHeaderORM", back_populates="details")
