from sqlalchemy import Column, DateTime, Text, String, UUID, Integer, Numeric, BINARY

from sqlalchemy.dialects.postgresql import BYTEA

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, unique=True, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    username = Column(Text, unique=True, nullable=False)
    email = Column(Text, primary_key=True, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    birthdate = Column(DateTime, nullable=True)
    gender = Column(Text, nullable=True)


class ForgotPassword(Base):
    __tablename__ = "forgot_password"

    user_id = Column(UUID, primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=True)
    status = Column(Text, nullable=False)
    identifier = Column(Text, nullable=True)


class Questions(Base):
    __tablename__ = "questions"

    question_id = Column(UUID, unique=True, nullable=False)
    user_id = Column(UUID, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    name = Column(Text, primary_key=True, nullable=True)
    category = Column(Text, nullable=True)
    value = Column(Text, nullable=True)


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(String, unique=True, nullable=False)
    user_id = Column(UUID, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    brand_name = Column(Text, nullable=True)
    medicine_name = Column(Text, nullable=True)
    dosage = Column(Numeric, nullable=True)
    dosage_unit = Column(Integer, nullable=True)
    stock = Column(Text, nullable=True)
    medication_type = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)


class Schedule(Base):
    __tablename__ = "schedule"

    schedule_id = Column(String, unique=True, nullable=False)
    user_id = Column(UUID, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    schedule_state = Column(Integer, nullable=True)
    time_to_take = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    quantity = Column(Numeric, nullable=True)
    image = Column(Text, nullable=True)

