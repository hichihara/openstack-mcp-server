# OpenStack MCP Server

A Model Context Protocol (MCP) server that provides AI models with direct access to OpenStack cloud infrastructure management capabilities.

## Features

- List servers (Nova Compute API)
- Support for OpenStack Identity API v3
- Support for Image service API v2
- Support for Compute API
- Support for Block Storage API v3
- Support for Networking API v2.0

## Installation

```bash
uv pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and configure your OpenStack credentials:

```bash
cp .env.example .env
```

## Usage

Start the MCP server:

```bash
python -m openstack_mcp_server
```

## Development

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .

# Lint code
ruff check .
```

## License

Apache License 2.0