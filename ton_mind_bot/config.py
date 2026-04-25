from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str
    database_url: str
    redis_url: str
    toncenter_api_key: str
    toncenter_base_url: str = "https://toncenter.com/api/v2"
    bot_wallet_address: str
    premium_cost_ton: float = 5
    premium_days: int = 30
    whale_threshold_ton: float = 10_000
    algo_holding_threshold: float = 1_000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
