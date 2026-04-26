from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str
    database_url: str
    redis_url: str
    toncenter_api_key: str
    toncenter_base_url: str = "https://toncenter.com/api/v2"
    tonapi_base_url: str = "https://tonapi.io/v2"
    bot_wallet_address: str
    tracked_wallet_address: str = "EQCYKUdisY5yEv9Z5f9J5KZQAaOe3ouSAZXSusXUpzFb3r1i"
    tracked_jetton_address: str = "EQCYKUdisY5yEv9Z5f9J5KZQAaOe3ouSAZXSusXUpzFb3r1i"
    premium_cost_ton: float = 5
    premium_days: int = 30
    whale_threshold_ton: float = 10_000
    algo_holding_threshold: float = 1_000
    token_growth_threshold_pct: float = 1000
    token_market_cap_threshold: float = 1_000_000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
