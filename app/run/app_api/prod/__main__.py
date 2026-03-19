from granian import Granian
from granian.constants import Interfaces, Loops, RuntimeModes
from granian.log import LogLevels

from app.core.config import env_config


if __name__ == "__main__":
    Granian(
        target="app.run.app_api.app:app",
        address="0.0.0.0",
        port=env_config.server_port,
        loop=Loops.uvloop,
        interface=Interfaces.ASGI,
        log_level=LogLevels.info,
        workers=env_config.server_workers,
        runtime_threads=env_config.server_worker_threads,
        runtime_mode=RuntimeModes.mt if env_config.server_worker_threads > 1 else RuntimeModes.st,
        respawn_failed_workers=True,
        respawn_interval=1,
    ).serve()
