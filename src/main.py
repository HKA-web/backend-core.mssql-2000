from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="SQL Server 2000 Microservice")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)
