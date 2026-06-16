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
        """Get headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
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
    
    async def close(self):
        """Close the client connection."""
        await self.client.aclose()
