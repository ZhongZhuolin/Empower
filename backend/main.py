from fastapi import FastAPI
from routes.company import router as company_router

app = FastAPI()

app.include_router(company_router)
