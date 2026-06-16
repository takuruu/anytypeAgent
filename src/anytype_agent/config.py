"""
Configuration settings for the AnyType Agent.
Loads from environment variables and .env file.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""
    
    # AnyType API Configuration
    ANYTYPE_API_KEY: Optional[str] = Field(
        default=None,
        description="AnyType API key for authentication",
    )
    ANYTYPE_SPACE_ID: Optional[str] = Field(
        default=None,
        description="AnyType Space ID (workspace)",
    )
    ANYTYPE_API_URL: str = Field(
        default="https://api.anytype.io",
        description="AnyType API base URL",
    )
    
    # MCP Server Configuration
    MCP_HOST: str = Field(
        default="localhost",
        description="MCP server host",
    )
    MCP_PORT: int = Field(
        default=8080,
        description="MCP server port",
    )
    MCP_LOG_LEVEL: str = Field(
        default="INFO",
        description="MCP server log level",
    )
    
    # Application Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Application log level",
    )
    DATA_DIR: Path = Field(
        default=Path("data"),
        description="Directory for local data storage",
    )
    TEMPLATES_DIR: Path = Field(
        default=Path("src/anytype_agent/templates"),
        description="Directory for note templates",
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Initialize settings
settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
