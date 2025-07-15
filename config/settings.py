from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = 'postgresql://postgres.padqznyuozjgdcbpjasx:9JBbhHQob88o2B8P@aws-0-us-east-2.pooler.supabase.com:6543/postgres'
settings = Settings()

