import stripe
import os
import logging
import sys
import hashlib
import bcrypt
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, text

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("api_debug.log")],
)
logger = logging.getLogger(__name__)

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

logger.info(f"🚀 Application starting...")
logger.info(f"📍 Environment: {ENVIRONMENT}")
logger.info(f"📊 Database URL: {os.getenv('DATABASE_URL', 'sqlite:///./escola.db')}")
logger.info(f"🔑 Stripe API configured: {STRIPE_SECRET_KEY[:20]}...")
stripe.api_key = STRIPE_SECRET_KEY
# Use environment variable for frontend URL in production
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

app = FastAPI(title="Escola do Oraculo API", version="1.0.1")

# Version info for debugging deployment
API_VERSION = "1.0.6-email-validation"
DEPLOY_TIMESTAMP = "2026-01-14T18:30:00Z"


@app.get("/version")
def get_version():
    """Returns the current API version and deployment info"""
    return {
        "api_version": API_VERSION,
        "deploy_timestamp": DEPLOY_TIMESTAMP,
        "environment": ENVIRONMENT,
        "python_hashlib": "enabled",
    }


@app.get("/debug/hash-test")
def debug_hash_test():
    """Test the password hashing to debug bcrypt issue"""
    import sys

    test_password = "Test123!"
    try:
        # Step 1: SHA256
        sha256_hash = hashlib.sha256(test_password.encode("utf-8")).hexdigest()
        logger.info(f"SHA256 hash: {sha256_hash} (len={len(sha256_hash)})")

        # Step 2: bcrypt (directly, not via passlib)
        salt = bcrypt.gensalt(rounds=12)
        bcrypt_hash = bcrypt.hashpw(sha256_hash.encode("utf-8"), salt)
        logger.info(f"Bcrypt hash: {bcrypt_hash[:30]}...")

        # Step 3: Verify
        verified = bcrypt.checkpw(sha256_hash.encode("utf-8"), bcrypt_hash)

        return {
            "success": True,
            "sha256_length": len(sha256_hash),
            "sha256_bytes": len(sha256_hash.encode("utf-8")),
            "bcrypt_length": len(bcrypt_hash),
            "verified": verified,
            "python_version": sys.version,
            "bcrypt_version": (
                bcrypt.__version__ if hasattr(bcrypt, "__version__") else "unknown"
            ),
            "message": "Hash test passed using bcrypt directly!",
        }
    except Exception as e:
        import traceback

        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "python_version": sys.version,
        }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    logger.info("🏥 Health check requested")
    try:
        # Tenta executar uma query simples para verificar a conexão
        logger.debug("Checking database connection...")
        db.execute(text("SELECT 1"))
        logger.info(f"✅ Health check OK - Environment: {ENVIRONMENT}")
        return {"status": "ok", "database": "connected", "environment": ENVIRONMENT}
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )


# CORS setup - allow frontend to talk to backend
allowed_origins = ["*"]
if ENVIRONMENT == "production":
    # In production, restrict to your domain
    # allowed_origins = [
    #     "https://escola-do-oraculo.com",
    #     "https://www.escola-do-oraculo.com",
    #     FRONTEND_URL,
    # ]
    # TEMPORARY: Allow all origins to enable local testing against prod backend
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STATIC FILES ---
# Mount the frontend folder to serve static files (CSS, JS, images)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    logger.info(f"✅ Mounting frontend from: {frontend_path}")
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
else:
    logger.warning(f"⚠️ Frontend path not found: {frontend_path}")

# --- SECURITY ---
# Using bcrypt directly instead of passlib to avoid compatibility issues
# with newer bcrypt versions and passlib's wrap bug detection


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using SHA256 pre-hash + bcrypt."""
    # Pre-hash with SHA256 to avoid bcrypt 72-byte limit
    sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    try:
        return bcrypt.checkpw(
            sha256_hash.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using SHA256 pre-hash + bcrypt."""
    # Pre-hash with SHA256 to ensure we never exceed bcrypt's 72-byte limit
    # SHA256 produces 64 hex chars, well within the limit
    logger.debug(f"get_password_hash called, password length: {len(password)}")
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    logger.debug(f"SHA256 pre-hash applied, length: {len(sha256_hash)}")

    try:
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(sha256_hash.encode("utf-8"), salt)
        result = hashed.decode("utf-8")
        logger.debug(f"Password hashed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in bcrypt.hashpw: {type(e).__name__}: {str(e)}")
        raise


# --- Pydantic MODELS ---
class UserLogin(BaseModel):
    email: EmailStr  # Validates email format automatically
    password: str


class UserCreate(BaseModel):
    email: EmailStr  # Validates email format automatically
    password: str
    full_name: Optional[str] = None


class UserDisplay(BaseModel):
    email: str
    full_name: Optional[str]
    subscription_status: str

    class Config:
        from_attributes = True


# --- ENDPOINTS ---


@app.get("/")
def read_root():
    """Serve the main HTML page"""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path, media_type="text/html")
    else:
        return {"message": "Welcome to Escola do Oraculo API (Connected to SQLite)"}


@app.post("/auth/register", status_code=201, response_model=UserDisplay)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"📝 Registration attempt for email: {user.email}")
    try:
        # Step 1: Check if user exists
        logger.debug(f"Step 1: Checking if user {user.email} already exists")
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            logger.warning(f"⚠️ Email {user.email} already registered")
            raise HTTPException(status_code=400, detail="Email already registered")
        logger.debug(f"✅ Email {user.email} is available")

        # Step 2: Hash password
        logger.debug(f"Step 2: Hashing password for {user.email}")
        hashed_pwd = get_password_hash(user.password)
        logger.debug(f"✅ Password hashed successfully")

        # Step 3: Create new user object
        logger.debug(f"Step 3: Creating User object for {user.email}")
        new_user = User(
            email=user.email,
            hashed_password=hashed_pwd,
            full_name=user.full_name,
            subscription_status="free",
        )
        logger.debug(f"✅ User object created: {new_user}")

        # Step 4: Add to database session
        logger.debug(f"Step 4: Adding user to database session")
        db.add(new_user)
        logger.debug(f"✅ User added to session")

        # Step 5: Commit to database
        logger.debug(f"Step 5: Committing to database")
        db.commit()
        logger.debug(f"✅ Committed successfully")

        # Step 6: Refresh from database
        logger.debug(f"Step 6: Refreshing user object from database")
        db.refresh(new_user)
        logger.info(
            f"✅ User registered successfully: {new_user.email} (ID: {new_user.id})"
        )

        return new_user
    except HTTPException:
        logger.error(f"❌ HTTPException during registration: {str(HTTPException)}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error during registration for {user.email}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Exception message: {str(e)}")
        logger.exception(f"Full traceback: ")

        try:
            db.rollback()
            logger.debug(f"✅ Database rollback successful")
        except Exception as rollback_error:
            logger.error(f"❌ Error during rollback: {str(rollback_error)}")

        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check if user was created via checkout without password
    if db_user.hashed_password.startswith("NO_PASSWORD:"):
        raise HTTPException(
            status_code=401,
            detail="This account was created via checkout. Please reset your password first.",
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # In a real app, generate a JWT token here. For now, we return a simulated token containing the user ID.
    return {
        "access_token": f"user_id:{db_user.id}",
        "token_type": "bearer",
        "user_email": db_user.email,
        "subscription": db_user.subscription_status,
    }


# --- FORGOT PASSWORD ---
class ForgotPasswordRequest(BaseModel):
    email: str


@app.post("/auth/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Initiate password reset. In production, this would send an email.
    For now, we just log and return success (to prevent email enumeration).
    """
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        # In production: generate reset token, save to DB, send email
        # For now, just log
        print(f"🔐 Password reset requested for: {request.email}")
        # TODO: Implement email sending with reset token
        # reset_token = secrets.token_urlsafe(32)
        # send_email(user.email, reset_link=f"{FRONTEND_URL}/pages/reset-password.html?token={reset_token}")

    # Always return success to prevent email enumeration attacks
    return {"message": "If this email exists, a reset link has been sent."}


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


@app.get("/auth/me")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Get current user from Authorization header.
    Supports both Bearer token and query parameter.
    """
    logger.debug("📍 /auth/me endpoint called")

    # Try to get token from Authorization header first
    auth_header = request.headers.get("Authorization")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
        logger.debug(f"Token from Authorization header: {token[:20]}...")
    else:
        # Fallback to query parameter
        token = request.query_params.get("token")
        if token:
            logger.debug(f"Token from query params: {token[:20]}...")

    if not token:
        logger.warning("No token provided")
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        if not token.startswith("user_id:"):
            raise ValueError("Invalid token format")

        user_id = int(token.split(":")[1])
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User not found for ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"✅ User authenticated: {user.email}")
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "subscription_status": user.subscription_status,
            "subscription_tier": user.subscription_plan or user.subscription_status,
            "stripe_customer_id": user.stripe_customer_id,
            "is_active": user.is_active,
        }
    except ValueError:
        logger.warning("Invalid token format")
        raise HTTPException(status_code=401, detail="Invalid token format")
    except Exception as e:
        logger.error(f"Error in /auth/me: {str(e)}")
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
            # Auto-register user if they don't exist during checkout
            # User will set password later when they first login
            # Use a special marker instead of bcrypt to avoid 72-byte limit issues
            # Format: "NO_PASSWORD:" indicates account created via checkout without password
            user = User(
                email=request.user_email,
                full_name=request.user_email.split("@")[0],
                hashed_password="NO_PASSWORD:checkout_auto_created",  # Marker, not a real hash
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


# --- STRIPE WEBHOOK ---
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Price IDs for products
STRIPE_PRICE_IDS = {
    "pro": os.getenv("STRIPE_PRICE_PRO", "price_1RUXxf2KN7yNwNd99t9Y3uyT"),
    "elite": os.getenv("STRIPE_PRICE_ELITE", "price_1RUY2C2KN7yNwNd9L4fPiVkw"),
    "radiestesia": os.getenv(
        "STRIPE_PRICE_RADIESTESIA", "price_1RUY502KN7yNwNd9wMcW0m8E"
    ),
    "modulo1": os.getenv("STRIPE_PRICE_MODULO1", "price_1RUY8z2KN7yNwNd9pQE2YYxO"),
    "modulo2": os.getenv("STRIPE_PRICE_MODULO2", "price_1RUYAu2KN7yNwNd9oFFqFp2D"),
    "modulo3": os.getenv("STRIPE_PRICE_MODULO3", "price_1RUYCg2KN7yNwNd93xJwPwXv"),
    "kundalini": os.getenv("STRIPE_PRICE_KUNDALINI", "price_1RUYFR2KN7yNwNd9RK2nwWvx"),
    "terapia": os.getenv("STRIPE_PRICE_TERAPIA", "price_1RUYGf2KN7yNwNd9Hs2z7K5L"),
}


# --- STRIPE CUSTOMER PORTAL ---
class PortalSessionRequest(BaseModel):
    return_url: str


@app.post("/stripe/create-portal-session")
def create_portal_session(
    request: PortalSessionRequest, token: str = None, db: Session = Depends(get_db)
):
    """
    Creates a Stripe Customer Portal session for the authenticated user.
    Allows users to manage their subscription, update payment methods, etc.
    """
    logger.info(f"🔄 Creating customer portal session")

    # Get user from token
    if not token:
        logger.warning("No token provided for portal session")
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        if not token.startswith("user_id:"):
            raise ValueError("Invalid token format")

        user_id = int(token.split(":")[1])
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User not found for ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        if not user.stripe_customer_id:
            logger.info(f"User {user.email} has no Stripe customer ID")
            raise HTTPException(
                status_code=404,
                detail="No subscription found. Please subscribe to a plan first.",
            )

        # Create the portal session
        portal_session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=request.return_url or FRONTEND_URL + "/pages/oraculo-app.html",
        )

        logger.info(f"✅ Portal session created for user {user.email}")
        return {"url": portal_session.url}

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating portal session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating portal session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stripe/prices")
def get_stripe_prices():
    """Retorna os IDs de preços do Stripe para os produtos"""
    return STRIPE_PRICE_IDS


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Recebe eventos do Stripe para atualizar subscrições"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        else:
            # Para testes sem webhook secret
            import json

            event = json.loads(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Processar eventos
    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        # Pagamento concluído com sucesso
        customer_id = data.get("customer")
        # subscription_id = data.get("subscription")  # Available if needed

        if customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_status = "active"
                db.commit()
                print(f"✅ User {user.email} subscription activated!")

    elif event_type == "customer.subscription.updated":
        customer_id = data.get("customer")
        sub_status = data.get("status")  # active, past_due, canceled, etc.

        if customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_status = sub_status
                db.commit()
                print(f"📝 User {user.email} subscription updated to: {sub_status}")

    elif event_type == "customer.subscription.deleted":
        customer_id = data.get("customer")

        if customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_status = "free"
                db.commit()
                print(f"❌ User {user.email} subscription cancelled")

    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer")

        if customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_status = "past_due"
                db.commit()
                print(f"⚠️ User {user.email} payment failed")

    return {"status": "received"}


# --- STATIC FILES ---
# Mount frontend files to serve them directly
import os

# Try to find the frontend directory relative to this file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(base_dir, "frontend")

# Debug: Print paths
print(f"Base directory: {base_dir}")
print(f"Frontend directory: {frontend_dir}")
print(f"Frontend exists: {os.path.exists(frontend_dir)}")

if os.path.exists(frontend_dir):
    print(f"✅ Mounting frontend from: {frontend_dir}")
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    print(f"❌ Frontend directory not found at: {frontend_dir}")
    # Fallback for when running from root
    if os.path.exists("frontend"):
        print("✅ Mounting frontend from: frontend (fallback)")
        app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
    else:
        print("❌ Could not find frontend directory in any location")
