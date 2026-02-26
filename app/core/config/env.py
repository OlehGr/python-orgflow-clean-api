from dynaconf import Dynaconf


env_config = Dynaconf(
    settings_files=["dynaconf.toml"],
    envvar_prefix="STT",
    environments=True,
    load_dotenv=True,
)
