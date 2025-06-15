"""MCP Server implementation for OpenStack."""

import logging
from typing import Any

from mcp.server import Server
from mcp.types import TextContent

from .config import Config
from .tools import ListServersParams, OpenStackTools

logger = logging.getLogger(__name__)


def create_server() -> tuple[Server, OpenStackTools]:
    """Create and configure the MCP server."""
    server = Server("openstack-mcp-server")
    config = Config()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.mcp.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    tools = OpenStackTools(config)

    @server.list_tools()
    async def list_tools() -> list[Any]:
        """List available tools."""
        return tools.get_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle tool calls."""
        logger.info(f"Tool called: {name} with arguments: {arguments}")

        if name == "list_servers":
            params = ListServersParams(**arguments)
            result = await tools.list_servers(params)

            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]

            servers_info = f"Found {result['count']} servers\n\n"

            for server in result["servers"]:
                server_info = (
                    f"ID: {server['id']}\n"
                    f"Name: {server['name']}\n"
                    f"Status: {server['status']}\n"
                )

                if "addresses" in server:
                    server_info += "Addresses:\n"
                    for network, addresses in server["addresses"].items():
                        for addr in addresses:
                            addr_type = addr['OS-EXT-IPS:type']
                            server_info += (
                                f"  - {network}: {addr['addr']} ({addr_type})\n"
                            )

                if "flavor" in server and isinstance(server["flavor"], dict):
                    server_info += (
                        f"Flavor: {server['flavor'].get('original_name', 'Unknown')}\n"
                    )

                if (
                    "image" in server
                    and server["image"]
                    and isinstance(server["image"], dict)
                ):
                    server_info += f"Image: {server['image'].get('id', 'Unknown')}\n"

                server_info += "\n"
                servers_info += server_info

            return [TextContent(type="text", text=servers_info)]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    return server, tools
