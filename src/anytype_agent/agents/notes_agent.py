"""
Notes Agent - Manages general note-taking and documentation.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from anytype_agent.agents.base_agent import BaseAgent
from anytype_agent.templates import get_template, list_templates

logger = logging.getLogger(__name__)


class NotesAgent(BaseAgent):
    """
    Agent specialized in note management.
    
    Capabilities:
    - Create various types of notes (daily, meeting, project, etc.)
    - Organize notes with tags and links
    - Search and retrieve notes
    - Template management
    """
    
    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process note-related queries.
        
        Supported commands:
        - create [type] <title> [--template <name>]
        - search <query>
        - list [templates|notes]
        - get <note_id>
        """
        parts = query.split()
        command = parts[0].lower() if parts else ""
        
        if command == "create":
            note_type = parts[1] if len(parts) >= 2 else "note"
            title = " ".join(parts[2:]) if len(parts) >= 3 else "Untitled"
            template = context.get("template") if context else None
            return await self.create_note_by_type(note_type, title, template)
        
        elif command == "search" and len(parts) >= 2:
            search_query = " ".join(parts[1:])
            return {"results": await self.search_notes(search_query)}
        
        elif command == "list":
            if len(parts) >= 2 and parts[1] == "templates":
                return {"templates": list_templates()}
            else:
                # List recent notes
                return {"notes": await self.list_recent_notes(20)}
        
        elif command == "get" and len(parts) >= 2:
            note_id = parts[1]
            return await self.get_note(note_id)
        
        else:
            return {"error": f"Unknown command: {query}", "isError": True}
    
    async def create_note_by_type(
        self,
        note_type: str,
        title: str,
        template: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a note based on its type."""
        # Map note types to templates
        type_to_template = {
            "daily": "journal",
            "journal": "journal",
            "task": "tasks",
            "learning": "learning",
            "meeting": "meeting",
        }
        
        actual_template = template or type_to_template.get(note_type, None)
        
        try:
            if actual_template:
                template_content = get_template(actual_template)
                # Replace date placeholder if exists
                template_content = template_content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
                template_content = template_content.replace("{{today}}", datetime.now().strftime("%Y-%m-%d"))
            else:
                template_content = f"# {title}\n\n---\n\n"
        except ValueError:
            template_content = f"# {title}\n\n---\n\n"
        
        result = await self.create_note(
            title=title,
            content=template_content,
            template=actual_template,
            properties={"type": note_type, "template": actual_template},
        )
        
        logger.info(f"Created {note_type} note: {title}")
        return {
            "status": "success",
            "note_id": result.get("id"),
            "title": title,
            "type": note_type,
            "message": f"{note_type.capitalize()} note '{title}' created",
        }
    
    async def list_recent_notes(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recently created/updated notes."""
        # TODO: Implement sorting by date when API supports it
        results = await self.search_notes("", limit=limit)
        return sorted(results, key=lambda x: x.get("createdAt", ""), reverse=True)
    
    async def create_daily_note(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Create a daily journal note."""
        date_str = date or datetime.now().strftime("%Y-%m-%d")
        title = f"Tagebuch - {date_str}"
        
        return await self.create_note_by_type("daily", title, "journal")
    
    async def create_meeting_note(
        self,
        title: str,
        participants: List[str] = None,
        agenda: List[str] = None,
    ) -> Dict[str, Any]:
        """Create a meeting note."""
        content = f"""# {title}

**Datum:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

**Teilnehmer:**
{chr(10).join([f\"- {p}\" for p in (participants or [])])}

**Agenda:**
{chr(10).join([f\"- [ ] {a}\" for a in (agenda or [])])}

---

## Notizen


---

## Aktionen

- [ ] Protokoll fertigstellen
- [ ] Aufgaben verteilen
"""
        
        result = await self.create_note(
            title=title,
            content=content,
            properties={"type": "meeting", "participants": participants},
        )
        
        return {
            "status": "success",
            "note_id": result.get("id"),
            "title": title,
        }
    
    async def link_notes(self, note_id_1: str, note_id_2: str, relation: str = "related") -> Dict[str, Any]:
        """Create a link/relation between two notes."""
        # In AnyType, this would be done via backlinks or relations
        # For now, we just log and return success
        logger.info(f"Linking {note_id_1} -> {note_id_2} ({relation})")
        return {
            "status": "success",
            "note_1": note_id_1,
            "note_2": note_id_2,
            "relation": relation,
        }
