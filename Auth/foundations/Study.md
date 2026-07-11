# Phase 1: Deep Dive Theory & Implementation Guide

---

## 1. Authentication (AuthN) vs. Authorization (AuthZ)

### The Concept
* **Authentication (AuthN)** is the process of verifying **who** an identity is. It establishes the baseline truth that a client is who they claim to be.
* **Authorization (AuthZ)** happens *after* successful authentication. It is the process of verifying **what** that authenticated identity is allowed to do based on policies, roles, or attributes.



### Architectural Pattern
In professional backend architecture, these are decoupled into sequential middleware layers within your request pipeline. AuthN always processes first to build the security context (`request.user`). AuthZ evaluates next, utilizing that security context against the targeted resource constraints. If AuthN fails, the system returns a `401 Unauthorized`. If AuthZ fails, it returns a `403 Forbidden`.

---

## 2. Stateful Session Management

### The Concept
Stateful session management relies on the server maintaining a persistent record of every authenticated user session in a centralized data store (e.g., RAM, or an enterprise Redis cluster). 

When a user authenticates, a highly random string (Session ID) is generated. This ID points to the user's session state on the server. The client stores only this ID, typically inside a browser cookie.

### Hardening Cookies Against Exploits
To prevent session hijacking, cookies must be restricted using explicit cryptographic and architectural boundary flags:
* `HttpOnly`: Instructs the browser that client-side JavaScript (e.g., `document.cookie`) cannot access the cookie payload. This neutralizes token theft via Cross-Site Scripting (XSS).
* `Secure`: Directs the browser to only transmit the cookie over encrypted TLS/HTTPS connections.
* `SameSite=Strict`: Tells the browser never to include the cookie on cross-site requests (e.g., clicking a link on an external malicious site pointing to your backend API), functioning as a primary defense against Cross-Site Request Forgery (CSRF).

---

## 3. Stateless Token Management (JWT)

### The Concept
Stateless token management shifts the burden of maintaining session state from the server to the client. The server generates a signed data token containing identity claims and handles verification purely via cryptography.

[Image diagram showing anatomy of a JSON Web Token with Header Payload and Signature sections decoded]

### Anatomy of a JSON Web Token (JWT)
A JWT consists of three distinct parts separated by periods (`.`):
1.  **Header:** Specifies the token type (`JWT`) and the digital signing algorithm used (e.g., `HS256`, `RS256`).
2.  **Payload:** Contains the claims—key-value assertions about the identity (e.g., `sub` for user ID, `exp` for expiration timestamp) and application-specific metadata (e.g., `roles`).
3.  **Signature:** A cryptographic hash computed by combining the encoded header, encoded payload, and a server-held secret or private key. 

$$\text{Signature} = \text{HMAC-SHA256}(\text{Header}_{\text{b64}} + "." + \text{Payload}_{\text{b64}}, \text{secret\_key})$$

### Symmetric vs. Asymmetric Signing
* **Symmetric (`HS256`):** The same secret key is shared between the service issuing the token and the service validating it. Ideal for single, monolithic backends.
* **Asymmetric (`RS256`/`ES256`):** The identity provider uses a private key to sign tokens, while downstream resource microservices verify the token using a public key. Downstream services cannot forge tokens, isolating compromise risks.

---

## 4. Complete Implementation Code

The production-ready Python suite below combines both concepts into a single, cohesive codebase using **FastAPI** and **PyJWT**.

```python
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, Depends, HTTPException, Response, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI(title="Identity Foundations Lab")

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# -----------------------------------------------------------------------------
# In production, these must be sourced from a secure environment or KMS secret store
JWT_SECRET_KEY = "enterprise-grade-signing-key-rotation-enabled"
JWT_ALGORITHM = "HS256"
SESSION_TTL_MINUTES = 30
TOKEN_TTL_MINUTES = 15

# Dummy User Database for demonstration purposes
USER_DB = {
    "engineer_one": {
        "user_id": "usr_9921",
        "password_raw": "secure_pass_123",  # Phase 2 will implement Argon2id hashing
        "roles": ["developer", "approver"]
    }
}

# -----------------------------------------------------------------------------
# STATEFUL SESSION STORAGE Engine
# -----------------------------------------------------------------------------
class SessionStore:
    """
    In-memory stateful session engine.
    Production translation: Replace self._storage with a redis-py client pool.
    """
    def __init__(self):
        # Storage schema: { session_id: { "user_id": str, "expires_at": datetime } }
        self._storage: Dict[str, Dict[str, Any]] = {}

    def create_session(self, user_id: str) -> str:
        # Cryptographically secure high-entropy string generation
        session_id = secrets.token_urlsafe(32)
        expiry = datetime.now(timezone.utc) + timedelta(minutes=SESSION_TTL_MINUTES)
        
        self._storage[session_id] = {
            "user_id": user_id,
            "expires_at": expiry
        }
        return session_id

    def get_session_data(self, session_id: str) -> Optional[str]:
        session = self._storage.get(session_id)
        if not session:
            return None
            
        # Lazy Eviction Check
        if datetime.now(timezone.utc) > session["expires_at"]:
            self.revoke_session(session_id)
            return None
            
        return session["user_id"]

    def revoke_session(self, session_id: str) -> None:
        self._storage.pop(session_id, None)

session_manager = SessionStore()

# -----------------------------------------------------------------------------
# STATELESS TOKEN (JWT) Engine
# -----------------------------------------------------------------------------
def generate_access_token(user_id: str, roles: List[str]) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_TTL_MINUTES),
        "roles": roles
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_access_token(token: str) -> Dict[str, Any]:
    try:
        # PyJWT checks token validity, structure, signature, and expiration natively.
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token signature has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid security token structure"
        )

# -----------------------------------------------------------------------------
# PIPELINE MIDDLEWARES & DEPENDENCIES (AuthN & AuthZ)
# -----------------------------------------------------------------------------
# Cookie Extractor for Stateful routes
def get_session_identity(request: Request) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Session cookie missing")
        
    user_id = session_manager.get_session_data(session_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Session invalid or expired")
    return user_id

# Header Token Extractor for Stateless routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-token")

def get_token_claims(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    return verify_access_token(token)

# Role Verification Dependency (AuthZ Layer)
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, claims: Dict[str, Any] = Depends(get_token_claims)):
        user_roles = claims.get("roles", [])
        if not any(role in user_roles for role in self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Access denied: Insufficient scope permissions"
            )

# -----------------------------------------------------------------------------
# ROUTE GATEWAYS
# -----------------------------------------------------------------------------

# --- FLOW A: COOKIE-BASED STATEFUL ROUTING ---
@app.post("/login-session")
def login_session(username: str, password_raw: str, response: Response):
    user = USER_DB.get(username)
    if not user or user["password_raw"] != password_raw:
        raise HTTPException(status_code=401, detail="Invalid identity credentials")
        
    session_id = session_manager.create_session(user["user_id"])
    
    # Securely append cookie context to header boundaries
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # Set to True in production environment (forces HTTPS)
        samesite="strict",
        path="/"
    )
    return {"message": "Stateful session established successfully"}

@app.get("/dashboard-session")
def dashboard_session(user_id: str = Depends(get_session_identity)):
    return {"message": f"Welcome to secure server space. Authenticated Identity: {user_id}"}

@app.post("/logout-session")
def logout_session(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id:
        session_manager.revoke_session(session_id)
    response.delete_cookie("session_id")
    return {"message": "Session terminated and server state cleared"}


# --- FLOW B: TOKEN-BASED STATELESS ROUTING ---
@app.post("/login-token")
def login_token(username: str, password_raw: str):
    user = USER_DB.get(username)
    if not user or user["password_raw"] != password_raw:
        raise HTTPException(status_code=401, detail="Invalid identity credentials")
        
    token = generate_access_token(user["user_id"], user["roles"])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/v1/resource-developer", dependencies=[Depends(RoleChecker(["developer"]))])
def get_developer_resource(claims: Dict[str, Any] = Depends(get_token_claims)):
    return {
        "data": "Stateless system data payload", 
        "authorized_subject": claims["sub"]
    }

@app.get("/api/v1/resource-admin", dependencies=[Depends(RoleChecker(["admin"]))])
def get_admin_resource():
    return {"data": "Highly privileged administrative sector"}