#!/usr/bin/env python3
"""Example script to test the list servers functionality."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openstack_mcp_server.config import Config
from openstack_mcp_server.tools import ListServersParams, OpenStackTools


async def main() -> None:
    """Test listing servers."""
    # Load configuration
    config = Config()
    tools = OpenStackTools(config)

    print("Testing OpenStack MCP Server - List Servers")
    print("=" * 50)

    # Test 1: List all servers with details
    print("\n1. Listing all servers with details:")
    params = ListServersParams(detailed=True)
    result = await tools.list_servers(params)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {result['count']} servers")
        for server in result["servers"]:
            print(f"\n  - Name: {server['name']}")
            print(f"    ID: {server['id']}")
            print(f"    Status: {server['status']}")
            if "addresses" in server:
                print("    Networks:")
                for network, addresses in server["addresses"].items():
                    for addr in addresses:
                        print(f"      {network}: {addr['addr']}")

    # Test 2: List active servers only
    print("\n2. Listing only ACTIVE servers:")
    params = ListServersParams(detailed=False, filters={"status": "ACTIVE"})
    result = await tools.list_servers(params)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {result['count']} active servers")
        for server in result["servers"]:
            print(f"  - {server['name']} ({server['id']})")

    # Test 3: List servers with limit
    print("\n3. Listing servers with limit=2:")
    params = ListServersParams(detailed=False, limit=2)
    result = await tools.list_servers(params)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {result['count']} servers (limited)")
        for server in result["servers"]:
            print(f"  - {server['name']} ({server['id']})")


if __name__ == "__main__":
    asyncio.run(main())
