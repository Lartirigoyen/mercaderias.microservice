from fastapi import FastAPI, Request
from routers.router import router
from dotenv import dotenv_values

config = dotenv_values(".env")

current_version = "v1"
documentacion = f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}/docs"
redoc_documentacion = f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}/redocs"

app = FastAPI(    
    title=config['APP_TITLE'],
    description=config['APP_DESCRIPTION'],
    version=config['APP_VERSION'],
    docs_url=documentacion, 
    redoc_url=redoc_documentacion
	)

# Importo rutas desde modulo
app.include_router(router)
