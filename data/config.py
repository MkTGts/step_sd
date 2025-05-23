from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    bot_token: str
    token_inn: str



@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            bot_token=env("BOT_STEP_SD"),
            token_inn=env("TOKEN_INN")
        )
    )

