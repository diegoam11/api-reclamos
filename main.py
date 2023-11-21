from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import reclamo_routes, queja_routes, solicitud_routes

app = FastAPI()

origins = ["*"]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(reclamo_routes.router)
app.include_router(queja_routes.router)
app.include_router(solicitud_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)