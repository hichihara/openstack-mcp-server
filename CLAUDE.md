# OpenStack MCP Server

## Project Overview

**OpenStack MCP Server** - A Model Context Protocol (MCP) server that provides AI models with direct access to OpenStack cloud infrastructure management capabilities.

### Purpose
Enable AI assistants to interact with OpenStack clouds through a standardized protocol, supporting infrastructure automation, monitoring, and management tasks across compute, storage, networking, and identity services.

### Key Capabilities
- **Multi-Service Support**: Integrates with Nova (Compute), Glance (Image), Cinder (Block Storage), Neutron (Networking), and Keystone (Identity)
- **Comprehensive Filtering**: Advanced query capabilities for all list operations
- **Resource Creation**: Create and manage servers, volumes, and network resources
- **Enterprise Ready**: Supports multi-tenant environments with proper authentication and authorization

## Architecture

```
┌─────────────────┐     MCP Protocol      ┌──────────────────┐
│   AI Assistant  │◄─────────────────────►│  OpenStack MCP   │
│    (Claude)     │                       │     Server       │
└─────────────────┘                       └────────┬─────────┘
                                                   │
                                          OpenStack│SDK
                                                   │
                                          ┌────────▼─────────┐
                                          │   OpenStack      │
                                          │   Cloud APIs     │
                                          ├──────────────────┤
                                          │ • Keystone (v3)  │
                                          │ • Nova           │
                                          │ • Glance (v2)    │
                                          │ • Cinder (v3)    │
                                          │ • Neutron (v2.0) │
                                          └──────────────────┘
```

## Best Practices

### 1. Efficient Querying
- **Use specific filters** to reduce API calls and data transfer
- **Set reasonable limits** on list operations (default: no limit)
- **Use `detailed=False`** when full server details aren't needed
- **Leverage tags** for logical grouping of resources

### 2. Error Handling
```python
try:
    server = await create_server(...)
except OpenStackCloudException as e:
    # Handle specific OpenStack errors
    logger.error(f"Failed to create server: {e}")
except Exception as e:
    # Handle general errors
    logger.error(f"Unexpected error: {e}")
```

### 3. Security Considerations
- **Never hardcode credentials** - use environment variables or secure vaults
- **Use project-scoped tokens** for better isolation
- **Implement rate limiting** to prevent API abuse
- **Audit all operations** for compliance
- **Rotate credentials regularly**

### 4. Performance Optimization
- **Cache static data** like flavors and images
- **Use pagination** for large result sets
- **Batch operations** when possible
- **Monitor API quotas** and rate limits

## Development style

### Base
- Language: `Python`
- Pckage Manager: `uv`
- Type Hints: Required for all functions
- Line Length: 88 characters maximum
- Virtual Environments: Always use venv or uv

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document all public functions
- Include docstring examples
- Dependencies: Pin versions in requirements

### Testing
- Use pytest with fixtures
- Write unit tests for new features
- Include integration tests for API operations
- Test with multiple OpenStack versions
- Verify error handling

## Security and Quality Standards

### NEVER Rules (Non-negotiable)

- NEVER: Delete production data without explicit confirmation
- NEVER: Hardcode API keys, passwords, token, or secrets
- NEVER: Commit code with failing tests or linting errors
- NEVER: Push directly to main/master branch
- NEVER: Skip security reviews for authentication/authorization code
- NEVER: Use pip install - always use uv

## Resources

- [OpenStack SDK Documentation](https://docs.openstack.org/openstacksdk/latest/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [OpenStack API Reference](https://docs.openstack.org/api-ref/)
- [Project Repository](https://github.com/hichihara/openstack-mcp-server)

## License

[Specify your license]

---

*This MCP server enables AI assistants to effectively manage OpenStack infrastructure while maintaining security and following best practices for cloud operations.*