from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import teams, challenges, admin

app = FastAPI(
    title="BreachPoint CTF Backend",
    description="API for the BreachPoint CTF platform.",
    version="1.0.0"
)

# --- CORRECT CORS Configuration ---
# This list only contains the URLs of the frontends that need access.
origins = [
    "http://localhost:8081",  # Your local frontend dev server
    "http://localhost:5173",
    "http://127.0.0.1:8081",
    "https://breachpoint-backend-api.onrender.com",
    "https://breachpoint-2k25-ctf.pages.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(teams.router)
app.include_router(challenges.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BreachPoint CTF API!"}