from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="client")

    tattoos: Mapped[list["TattooSession"]] = relationship("TattooSession", back_populates="artist")
    client_appointments = relationship("Appointment", foreign_keys="Appointment.client_id", back_populates="client")
    artist_appointments = relationship("Appointment", foreign_keys="Appointment.artist_id", back_populates="artist")

class TattooSession(Base):
    __allow_unmapped__ = True
    __tablename__ = "tattoos"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    artist = relationship("User", back_populates="tattoos")
    appointments = relationship("Appointment", back_populates="tattoo", cascade="all, delete-orphan")

class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        UniqueConstraint("tattoo_id", "date_time", name="unique_tattoo_booking"),
    )

    id = Column(Integer, primary_key=True, index=True)
    tattoo_id = Column(Integer, ForeignKey("tattoos.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    artist_id = Column(Integer, ForeignKey("users.id"))
    date_time = Column(DateTime, nullable=False)
    status = Column(String, default="pending")  # pending/completed/cancelled

    tattoo = relationship("TattooSession", back_populates="appointments")
    client = relationship("User", foreign_keys=[client_id], back_populates="client_appointments")
    artist = relationship("User", foreign_keys=[artist_id], back_populates="artist_appointments")

    __allow_unmapped__ = True
    __tablename__ = "appointments"
    __table_args__ = (UniqueConstraint("tattoo_id", "date_time", name="unique_tattoo_booking"),)
    __table_args__ = (UniqueConstraint("tattoo_id", "date_time", name="unique_tattoo_booking"),)


    id = Column(Integer, primary_key=True, index=True)
    tattoo_id = Column(Integer, ForeignKey("tattoos.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    artist_id = Column(Integer, ForeignKey("users.id"))
    date_time = Column(DateTime, nullable=False)
    status = Column(String, default="pending")  # pending/completed/cancelled

    tattoo = relationship("TattooSession", back_populates="appointments")
    client = relationship("User", foreign_keys=[client_id], back_populates="client_appointments")
    artist = relationship("User", foreign_keys=[artist_id], back_populates="artist_appointments")

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  # ✅ primary key
    tattoo_id: Mapped[int] = mapped_column(Integer, ForeignKey("tattoos.id"))
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    tattoo: Mapped["TattooSession"] = relationship("TattooSession")
    client: Mapped["User"] = relationship("User")

    