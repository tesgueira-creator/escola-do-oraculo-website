import stripe
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean

# Try to import from the package (when running from root), else fallback to local (when running from folder)
try:
    from backend_server.database import engine, Base, get_db
except ImportError:
    from database import engine, Base, get_db

# --- PORT CONFIGURATION ---
PORT = int(os.getenv("PORT", 8000))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")


# --- INIT DB ---
# Initialize the database tables
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    subscription_status = Column(String, default="free")  # free, active, past_due
    stripe_customer_id = Column(String, nullable=True)  # ID do cliente no Stripe
    subscription_plan = Column(String, nullable=True)  # PRO, ELITE, RADIESTESIA


Base.metadata.create_all(bind=engine)

# --- CONFIG ---
# Replace with your actual Stripe Secret Key (SK)
# For dev, use "sk_test_..."
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_PLACEHOLDER")
stripe.api_key = STRIPE_SECRET_KEY
FRONTEND_URL = (
    "http://localhost:8000"  # Adjust if frontend is on a different port/domain in prod
)

app = FastAPI(title="Escola do Oraculo API", version="1.0.0")

# CORS setup - allow frontend to talk to backend
allowed_origins = ["*"]
if ENVIRONMENT == "production":
    # In production, restrict to your domain
    allowed_origins = [
        "https://escola-do-oraculo.com",
        "https://www.escola-do-oraculo.com",
        FRONTEND_URL,
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# --- Pydantic MODELS ---
class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


class UserDisplay(BaseModel):
    email: str
    full_name: Optional[str]
    subscription_status: str

    class Config:
        orm_mode = True


# --- ENDPOINTS ---


@app.get("/")
def read_root():
    return {"message": "Welcome to Escola do Oraculo API (Connected to SQLite)"}


@app.post("/auth/register", status_code=201, response_model=UserDisplay)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_pwd = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name,
        subscription_status="free",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # In a real app, generate a JWT token here. For now, we return a simulated token containing the user ID.
    return {
        "access_token": f"user_id:{db_user.id}",
        "token_type": "bearer",
        "user_email": db_user.email,
        "subscription": db_user.subscription_status,
    }


@app.get("/users/me", response_model=UserDisplay)
def read_users_me(token: str, db: Session = Depends(get_db)):
    # Simulating token decoding: Expected format "user_id:1"
    try:
        if not token.startswith("user_id:"):
            raise ValueError("Invalid token format")

        user_id_str = token.split(":")[1]
        user_id = int(user_id_str)

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


# --- PAYMENT ENDPOINTS ---


class CheckoutRequest(BaseModel):
    price_id: str  # Stripe Price ID (e.g. price_1Met...)
    user_email: str  # Email do utilizador


@app.post("/payments/create-checkout-session")
def create_checkout_session(request: CheckoutRequest, db: Session = Depends(get_db)):
    try:
        # Buscar utilizador
        user = db.query(User).filter(User.email == request.user_email).first()
        if not user:
            # Auto-register user if they don't exist
            # Note: In a real app, you'd send an email to set a password.
            # Here we just create the record to link the Stripe Customer.
            user = User(
                email=request.user_email,
                full_name=request.user_email.split("@")[0],
                hashed_password=get_password_hash("temporary_password"),
                is_active=True,
                subscription_status="free",
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Criar ou reutilizar customer no Stripe
        if user.stripe_customer_id:
            customer_id = user.stripe_customer_id
        else:
            customer = stripe.Customer.create(
                email=user.email, name=user.full_name or user.email
            )
            customer_id = customer.id
            user.stripe_customer_id = customer_id
            db.commit()

        # Criar sessão de checkout
        checkout_session = stripe.checkout.Session.create(
            customer=customer_id,
            line_items=[
                {
                    "price": request.price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=FRONTEND_URL
            + "/pages/oraculo-app.html?payment=success&session_id={CHECKOUT_SESSION_ID}",
            cancel_url=FRONTEND_URL + "/pages/checkout.html?payment=cancelled",
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/customer/create-portal-session")
def create_customer_portal_session(user_email: str, db: Session = Depends(get_db)):
    """Cria um link para o Customer Portal do Stripe"""
    try:
        # Buscar utilizador
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.stripe_customer_id:
            raise HTTPException(status_code=400, detail="No Stripe customer found")

        # Criar sessão do portal
        session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=FRONTEND_URL + "/pages/oraculo-app.html",
        )
        return {"portal_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- STATIC FILES ---
# Mount frontend files to serve them directly
import os

# Try to find the frontend directory relative to this file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(base_dir, "frontend")

if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    # Fallback for when running from root
    if os.path.exists("frontend"):
        app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
