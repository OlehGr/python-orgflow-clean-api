import uvicorn

from app.core.config import env_config


if __name__ == "__main__":
    uvicorn.run(
        "app.run.app_api.app:app",
        host="0.0.0.0",
        port=env_config.server_port,
        log_level="info",
    )
