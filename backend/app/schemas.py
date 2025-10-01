from pydantic import BaseModel
from datetime import datetime

# Data user sends when signing up
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "client"

# Data API sends back
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str 

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TattooCreate(BaseModel):
    title: str
    description: str | None = None
    price: float

class TattooOut(BaseModel):
    id: int
    artist_id: int
    title: str
    description: str | None = None
    price: float
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

class TattooBase(BaseModel):
    title: str
    description: str | None = None
    price: int

class TattooCreate(TattooBase):
    pass

class TattooOut(TattooBase):
    id: int
    artist_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
    tattoo_id: int
    date_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentOut(AppointmentBase):
    id: int
    client_id: int
    artist_id: int
    status: str

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    tattoo_id: int
    rating: int
    comment: str | None = None

class ReviewOut(BaseModel):
    id: int
    tattoo_id: int
    client_id: int
    rating: int
    comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True
