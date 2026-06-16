"""
Base class for all agents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from anytype_agent.mcp.client import AnyTypeClient

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    Provides common functionality:
    - AnyType client access
    - Template management
    - Object CRUD operations
    """
    
    def __init__(self):
        self.client = AnyTypeClient()
        self.name = self.__class__.__name__
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a query/request. Must be implemented by subclasses."""
        pass
    
    async def create_note(
        self,
        title: str,
        content: str,
        template: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new note in AnyType."""
        return await self.client.create_object(
            type="note",
            title=title,
            content=content,
            template=template,
            properties=properties or {},
        )
    
    async def search_notes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for notes."""
        result = await self.client.search_objects(query, type="note", limit=limit)
        return result.get("results", [])
    
    async def get_note(self, note_id: str) -> Dict[str, Any]:
        """Get a note by ID."""
        return await self.client.get_object(note_id)
    
    async def update_note(
        self,
        note_id: str,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update a note."""
        return await self.client.update_object(note_id, updates)
    
    async def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Delete a note."""
        return await self.client.delete_object(note_id)
