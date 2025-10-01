from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from app import schemas, models, database
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "supersecretkey"   # keep in .env later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

def require_role(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        # current_user here can be username; fetch from DB for role
        from sqlalchemy.orm import Session
        db: Session = next(database.get_db())
        user = db.query(models.User).filter(models.User.username == current_user).first()
        if not user or user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role} role"
            )
        return user
    return role_checker

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.post("/registerUser", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw,role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
