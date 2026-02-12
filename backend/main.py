from fastapi import FastAPI
from backend.app.api.routes.analytics import router as analytics_router

from backend.app.database.connection import Base, engine
from backend.app.auth.routes import router as auth_router
from backend.app.api.routes.recommendations import router as reco_router
from fastapi.middleware.cors import CORSMiddleware
from backend.app.chat.routes import router as chat_router
#from backend.app.chat.websocket import router as ws_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"],          
)

app.include_router(analytics_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(reco_router)

@app.get("/")
def health():
    return {"status": "running"}
