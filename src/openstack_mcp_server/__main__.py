"""Main entry point for the OpenStack MCP Server."""

import asyncio
import logging

from .server import create_server

logger = logging.getLogger(__name__)


async def main() -> None:
    """Run the MCP server."""
    server, tools = create_server()

    logger.info("Starting OpenStack MCP Server...")

    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
