from sqlalchemy import Column, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InvoiceCharges(Base):
    __tablename__ = "invoice_charges"

    Invoice_SF_Id = Column(String(50))
    Ship_To_Account_SF = Column(String(50))
    Ship_To_Account_Number = Column(String(50))
    Ship_To_Account_Name = Column(String(100))
    Total_Recurring = Column(DECIMAL(10,2), nullable=False)
    Total_Contractual_One_Time = Column(DECIMAL(10,2), nullable=False)
    Total_Variable = Column(DECIMAL(10,2), nullable=False)
    Total_tax = Column(DECIMAL(10,2), nullable=False)
    Total = Column(DECIMAL(10,2), nullable=False)
