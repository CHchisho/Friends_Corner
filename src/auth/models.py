from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData

from database import Base, metadata



# role = Table(
#     "role",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("permissions", JSON),
# )

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    # Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),

    Column("phone_number", String),
    Column("gender", String, nullable=False),
    Column("regions", String, nullable=False),
    Column("your_age", Integer, nullable=False),
    Column("hobbies", String),
    Column("friend_gender", String, nullable=False),
    Column("friend_age_from", Integer, nullable=False),
    Column("friend_age_to", Integer, nullable=False),
)
#   email
#   password
#   is_active
#   is_superuser
#   is_verified
#   username

#   phone_number
#   gender
#   regions
#   your_age
#   hobbies
#   friend_gender
#   friend_age_from
#   friend_age_to

# требуется для fastapi_users \/, она их использует
class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)

    phone_number = Column(String)
    gender = Column(String, nullable=False)
    regions = Column(String, nullable=False)
    your_age = Column(Integer, nullable=False)
    hobbies = Column(String)
    friend_gender = Column(String, nullable=False)
    friend_age_from = Column(Integer, nullable=False)
    friend_age_to = Column(Integer, nullable=False)

    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    # role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

