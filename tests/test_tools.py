"""Tests for OpenStack tools."""

from unittest.mock import MagicMock, patch

import pytest

from openstack_mcp_server.tools import ListServersParams, OpenStackTools


@pytest.fixture
def mock_config() -> MagicMock:
    """Create mock configuration."""
    config = MagicMock()
    config.openstack = MagicMock()
    config.openstack.auth_url = "https://example.com:5000/v3"
    config.openstack.project_name = "test-project"
    config.openstack.project_domain_name = "default"
    config.openstack.username = "test-user"
    config.openstack.password = "test-pass"
    config.openstack.user_domain_name = "default"
    config.openstack.region_name = "RegionOne"
    config.openstack.has_password_auth.return_value = True
    config.openstack.has_app_credential_auth.return_value = False
    return config


@pytest.fixture
def tools(mock_config: MagicMock) -> OpenStackTools:
    """Create OpenStackTools instance with mock config."""
    return OpenStackTools(mock_config)


def test_get_tools(tools: OpenStackTools) -> None:
    """Test getting available tools."""
    available_tools = tools.get_tools()

    assert len(available_tools) == 1
    assert available_tools[0].name == "list_servers"
    assert "List servers" in available_tools[0].description


@pytest.mark.asyncio
async def test_list_servers(tools: OpenStackTools) -> None:
    """Test listing servers."""
    # Mock server objects
    mock_server1 = MagicMock()
    mock_server1.to_dict.return_value = {
        "id": "server-1",
        "name": "test-server-1",
        "status": "ACTIVE",
        "addresses": {"private": [{"addr": "10.0.0.1", "OS-EXT-IPS:type": "fixed"}]},
    }

    mock_server2 = MagicMock()
    mock_server2.to_dict.return_value = {
        "id": "server-2",
        "name": "test-server-2",
        "status": "SHUTOFF",
        "addresses": {"private": [{"addr": "10.0.0.2", "OS-EXT-IPS:type": "fixed"}]},
    }

    # Mock connection
    with patch.object(tools, "_conn", MagicMock()):
        tools._conn.compute.servers.return_value = [mock_server1, mock_server2]

        params = ListServersParams(detailed=True)
        result = await tools.list_servers(params)

    assert result["count"] == 2
    assert len(result["servers"]) == 2
    assert result["servers"][0]["name"] == "test-server-1"
    assert result["servers"][1]["name"] == "test-server-2"


@pytest.mark.asyncio
async def test_list_servers_with_filters(tools: OpenStackTools) -> None:
    """Test listing servers with filters."""
    mock_server = MagicMock()
    mock_server.to_dict.return_value = {
        "id": "server-1",
        "name": "test-server-1",
        "status": "ACTIVE",
    }

    with patch.object(tools, "_conn", MagicMock()):
        tools._conn.compute.servers.return_value = [mock_server]

        params = ListServersParams(
            detailed=False, filters={"status": "ACTIVE"}, limit=10
        )
        result = await tools.list_servers(params)

        # Verify the call was made with correct parameters
        tools._conn.compute.servers.assert_called_once_with(
            detailed=False, all_projects=False, status="ACTIVE", limit=10
        )

    assert result["count"] == 1
    assert result["servers"][0]["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_list_servers_error_handling(tools: OpenStackTools) -> None:
    """Test error handling when listing servers fails."""
    with patch.object(tools, "_conn", MagicMock()):
        tools._conn.compute.servers.side_effect = Exception("Connection failed")

        params = ListServersParams()
        result = await tools.list_servers(params)

    assert "error" in result
    assert "Unexpected error" in result["error"]
    assert result["count"] == 0
    assert result["servers"] == []
