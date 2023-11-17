from fastapi import FastAPI
from routes import reclamo_routes, queja_routes, solicitud_routes

app = FastAPI()

app.include_router(reclamo_routes.router)
app.include_router(queja_routes.router)
app.include_router(solicitud_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
