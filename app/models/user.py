from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Boolean
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from app import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # Bu satırı ekleyin

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), unique=True, nullable=False, index=True)
    username = mapped_column(String(255), unique=True,
                             nullable=False, index=True)
    password = mapped_column(String(255), nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)
    is_admin = mapped_column(Boolean, default=False, nullable=False)
    created_at = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

#   relationships:
    profile = relationship("Profile", back_populates="user")
    listings = relationship("Listing", back_populates="owner")
    wishlist_items = relationship("WishlistItem", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "password_debug": self.password
        }
