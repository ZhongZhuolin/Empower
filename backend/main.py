from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.company import router as company_router

app = FastAPI()
# added CORS so react in port 5173 can interact with local host 8000 where uvicorn lives
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_router)
