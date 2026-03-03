from dynaconf import Dynaconf, Validator


env_config = Dynaconf(
    envvar_prefix=False,
    environments=True,
    load_dotenv=True,
    validators=[
        Validator("DEBUG", default=False, cast=lambda v: bool(int(v))),
        Validator("LOCAL_DEV", default=False, cast=lambda v: bool(int(v))),
        Validator("DB_POOL_SIZE", default=5, cast=int),
        Validator("DB_MAX_OVERFLOW", default=5, cast=int),
        Validator("ACCESS_TOKEN_MINUTES", default=15, cast=int),
        Validator("REFRESH_TOKEN_DAYS", default=60, cast=int),
        Validator("SERVER_WORKERS", default=1, cast=int),
        Validator("SERVER_WORKER_THREADS", default=1, cast=int),
        Validator("SERVER_PORT", default=8000, cast=int),
    ],
)
