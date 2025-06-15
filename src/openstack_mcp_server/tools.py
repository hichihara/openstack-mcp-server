"""MCP tools for OpenStack operations."""

import logging
from typing import Any

from mcp.types import Tool
from openstack import connection
from openstack.exceptions import OpenStackCloudException
from pydantic import BaseModel, Field

from .config import Config

logger = logging.getLogger(__name__)


class ListServersParams(BaseModel):
    """Parameters for listing servers."""

    detailed: bool = Field(
        default=True,
        description="Whether to return detailed server information",
    )
    all_projects: bool = Field(
        default=False,
        description="List servers from all projects (admin only)",
    )
    filters: dict[str, Any] | None = Field(
        default=None,
        description="Filters to apply when listing servers",
    )
    limit: int | None = Field(
        default=None,
        description="Maximum number of servers to return",
    )
    marker: str | None = Field(
        default=None,
        description="ID of the last item in the previous page (for pagination)",
    )


class OpenStackTools:
    """OpenStack MCP tools implementation."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._conn: connection.Connection | None = None

    @property
    def conn(self) -> connection.Connection:
        """Get or create OpenStack connection."""
        if self._conn is None:
            auth_args = {
                "auth_url": self.config.openstack.auth_url,
                "project_name": self.config.openstack.project_name,
                "project_domain_name": self.config.openstack.project_domain_name,
                "region_name": self.config.openstack.region_name,
            }

            if self.config.openstack.has_password_auth():
                auth_args.update(
                    {
                        "username": self.config.openstack.username,
                        "password": self.config.openstack.password,
                        "user_domain_name": self.config.openstack.user_domain_name,
                    }
                )
            elif self.config.openstack.has_app_credential_auth():
                auth_args.update(
                    {
                        "application_credential_id": (
                            self.config.openstack.application_credential_id
                        ),
                        "application_credential_secret": (
                            self.config.openstack.application_credential_secret
                        ),
                    }
                )
            else:
                raise ValueError(
                    "No valid authentication method configured. "
                    "Please provide valid authentication credentials."
                )

            self._conn = connection.Connection(**auth_args)
            logger.info("OpenStack connection established")

        return self._conn

    async def list_servers(self, params: ListServersParams) -> dict[str, Any]:
        """List servers from OpenStack Nova."""
        try:
            kwargs: dict[str, Any] = {
                "detailed": params.detailed,
                "all_projects": params.all_projects,
            }

            if params.filters:
                kwargs.update(params.filters)

            if params.limit:
                kwargs["limit"] = params.limit

            if params.marker:
                kwargs["marker"] = params.marker

            servers = list(self.conn.compute.servers(**kwargs))

            return {
                "servers": [server.to_dict() for server in servers],
                "count": len(servers),
            }

        except OpenStackCloudException as e:
            logger.error(f"Failed to list servers: {e}")
            return {
                "error": f"Failed to list servers: {str(e)}",
                "servers": [],
                "count": 0,
            }
        except Exception as e:
            logger.exception("Unexpected error listing servers")
            return {
                "error": f"Unexpected error: {str(e)}",
                "servers": [],
                "count": 0,
            }

    def get_tools(self) -> list[Tool]:
        """Get list of available tools."""
        return [
            Tool(
                name="list_servers",
                description="List servers from OpenStack Nova compute service",
                inputSchema=ListServersParams.model_json_schema(),
            ),
        ]
