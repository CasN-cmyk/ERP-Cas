from __future__ import annotations

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base


class CRMLead(Base):
    __tablename__ = "crm_leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str | None] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="new")
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    notes: Mapped[str | None] = mapped_column(Text)


class CRMDeal(Base):
    __tablename__ = "crm_deals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id"))
    title: Mapped[str] = mapped_column(String(255))
    value_ex: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    stage: Mapped[str] = mapped_column(String(20), default="prospect")
    expected_close: Mapped[datetime | None] = mapped_column(DateTime)
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    customer = relationship("Customer", back_populates="deals")
    activities: Mapped[list["CRMActivity"]] = relationship(back_populates="deal", cascade="all, delete-orphan")


class CRMActivity(Base):
    __tablename__ = "crm_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deal_id: Mapped[int] = mapped_column(ForeignKey("crm_deals.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(20))
    subject: Mapped[str] = mapped_column(String(255))
    due_at: Mapped[datetime | None] = mapped_column(DateTime)
    done_at: Mapped[datetime | None] = mapped_column(DateTime)
    notes: Mapped[str | None] = mapped_column(Text)

    deal = relationship("CRMDeal", back_populates="activities")
