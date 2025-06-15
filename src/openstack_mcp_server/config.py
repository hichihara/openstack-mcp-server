"""Configuration management for OpenStack MCP Server."""


from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenStackConfig(BaseSettings):
    """OpenStack authentication configuration."""

    auth_url: str
    project_name: str
    project_domain_name: str = "default"
    username: str | None = None
    password: str | None = None
    user_domain_name: str = "default"
    region_name: str = "RegionOne"

    application_credential_id: str | None = None
    application_credential_secret: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="OS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def has_password_auth(self) -> bool:
        """Check if password authentication is configured."""
        return bool(self.username and self.password)

    def has_app_credential_auth(self) -> bool:
        """Check if application credential authentication is configured."""
        return bool(
            self.application_credential_id and self.application_credential_secret
        )


class MCPConfig(BaseSettings):
    """MCP server configuration."""

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


class Config:
    """Application configuration."""

    def __init__(self) -> None:
        self.openstack = OpenStackConfig()
        self.mcp = MCPConfig()
