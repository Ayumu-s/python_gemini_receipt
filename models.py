from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, LargeBinary
from sqlalchemy.orm import deferred
from datetime import datetime
from database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=True)
    result = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    receipt_date = Column(Date, nullable=True)
    is_expense = Column(Boolean, default=True, nullable=False, server_default="true")
    image_data = deferred(Column(LargeBinary, nullable=True))  # 明示アクセス時のみ読み込む
    image_content_type = Column(String(50), nullable=True)
