from __future__ import annotations

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))

    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(back_populates="supplier")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    currency: Mapped[str] = mapped_column(String(5), default="EUR")
    expected_at: Mapped[datetime | None] = mapped_column(DateTime)

    supplier: Mapped[Supplier] = relationship(back_populates="purchase_orders")
    lines: Mapped[list["PurchaseOrderLine"]] = relationship(back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    po_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost_ex: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    purchase_order: Mapped[PurchaseOrder] = relationship(back_populates="lines")
