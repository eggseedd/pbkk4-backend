from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import files, jobs, results

def create_app() -> FastAPI:
    app = FastAPI(title="AI Backend")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # adjust later
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(files.router, prefix="/files", tags=["files"])
    app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
    app.include_router(results.router, prefix="/results", tags=["results"])

    @app.get("/")
    def root():
        return {"msg" : "Asolole"}

    return app

app = create_app()
