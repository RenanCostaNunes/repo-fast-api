import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Base properties for User
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: str | None = Field(default=None, max_length=255)

# Properties for creating a new user
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# Properties for user registration
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

# Properties for updating user details
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

# Specific updates for user profile (self)
class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

# Model for updating passwords
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# Database model for User, with relationships
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete"})

# Public properties for returning user details via API
class UserPublic(UserBase):
    id: uuid.UUID

# Model for paginated user responses
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# Base properties for Item
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

# Properties for creating a new item
class ItemCreate(ItemBase):
    pass

# Properties for updating an item
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# Database model for Item, with relationships
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")

# Public properties for returning item details via API
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID

# Model for paginated item responses
class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int

# Generic message model
class Message(SQLModel):
    message: str

# Model for JWT token response
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token payload
class TokenPayload(SQLModel):
    sub: str | None = None

# Model for updating password using token
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
