"""
Main entry point for the AnyType Agent.
"""

import logging
from pathlib import Path

from anytype_agent.config import settings
from anytype_agent.mcp.server import start_mcp_server
from anytype_agent.agents import LearningAgent, NotesAgent, OrganizationAgent

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Start the AnyType Agent."""
    logger.info("Starting AnyType Agent v%s", __import__("anytype_agent").__version__)
    
    # Initialize agents
    learning_agent = LearningAgent()
    notes_agent = NotesAgent()
    organization_agent = OrganizationAgent()
    
    logger.info("Agents initialized: Learning, Notes, Organization")
    
    # Start MCP server for Anytype integration
    start_mcp_server()


if __name__ == "__main__":
    main()
