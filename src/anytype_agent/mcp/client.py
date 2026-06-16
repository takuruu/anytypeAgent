"""
AnyType API Client for MCP Server.
Handles authentication and API requests to AnyType.
"""

import httpx
import logging
from typing import Any, Dict, List, Optional

from anytype_agent.config import settings

logger = logging.getLogger(__name__)


class AnyTypeClient:
    """
    Client for interacting with the AnyType API.
    
    Reference: https://developers.anytype.io
    """
    
    def __init__(self):
        self.base_url = settings.ANYTYPE_API_URL
        self.api_key = settings.ANYTYPE_API_KEY
        self.space_id = settings.ANYTYPE_SPACE_ID
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._get_headers(),
            timeout=30.0,
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.
        
        AnyType requires:
        - Anytype-Version header (current: 2025-11-08)
        - Authorization: Bearer <api_key> (from Desktop Client Settings)
        - X-Space-ID: <space_id> (optional, for multi-space setups)
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Anytype-Version": "2025-11-08",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if self.space_id:
            headers["X-Space-ID"] = self.space_id
        return headers
    
    async def create_object(
        self,
        type: str,
        title: str,
        content: Optional[str] = None,
        template: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new object in AnyType."""
        payload = {
            "type": type,
            "title": title,
        }
        if content:
            payload["content"] = content
        if template:
            payload["template"] = template
        if properties:
            payload["properties"] = properties
        
        response = await self.client.post("/api/objects", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def get_object(self, object_id: str) -> Dict[str, Any]:
        """Get an object by ID."""
        response = await self.client.get(f"/api/objects/{object_id}")
        response.raise_for_status()
        return response.json()
    
    async def update_object(
        self,
        object_id: str,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update an existing object."""
        response = await self.client.patch(
            f"/api/objects/{object_id}",
            json=updates,
        )
        response.raise_for_status()
        return response.json()
    
    async def delete_object(self, object_id: str) -> Dict[str, Any]:
        """Delete an object."""
        response = await self.client.delete(f"/api/objects/{object_id}")
        response.raise_for_status()
        return response.json()
    
    async def search_objects(
        self,
        query: str,
        type: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Search for objects."""
        params: Dict[str, Any] = {"query": query, "limit": limit}
        if type:
            params["type"] = type
        
        response = await self.client.get("/api/search", params=params)
        response.raise_for_status()
        return response.json()
    
    async def list_templates(self) -> List[Dict[str, Any]]:
        """List available templates."""
        response = await self.client.get("/api/templates")
        response.raise_for_status()
        return response.json()

    async def test_connection(self) -> Dict[str, Any]:
        """Test the connection to AnyType API and return account info."""
        try:
            response = await self.client.get("/api/account")
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except httpx.HTTPStatusError as e:
            logger.error(f"Connection test failed: {e.response.status_code} - {e.response.text}")
            return {
                "status": "error",
                "error": f"HTTP {e.response.status_code}",
                "message": e.response.text[:200],
            }
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            return {
                "status": "error",
                "error": "connection_failed",
                "message": f"Could not connect to {self.base_url}. Is the AnyType service running?",
            }

    async def close(self):
        """Close the client connection."""
        await self.client.aclose()
