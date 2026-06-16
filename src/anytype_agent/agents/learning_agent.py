"""
Learning Agent - Helps with creating and organizing learning materials.
"""

import logging
from typing import Any, Dict, List, Optional

from anytype_agent.agents.base_agent import BaseAgent
from anytype_agent.templates import get_template

logger = logging.getLogger(__name__)


class LearningAgent(BaseAgent):
    """
    Agent specialized in learning and knowledge management.
    
    Capabilities:
    - Create structured learning notes
    - Organize knowledge by topics and categories
    - Track learning progress
    - Generate summaries and flashcards
    """
    
    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process learning-related queries.
        
        Supported commands:
        - create note <title> [--template <name>]
        - search <query>
        - summarize <note_id>
        """
        parts = query.split()
        command = parts[0].lower() if parts else ""
        
        if command == "create" and len(parts) >= 3:
            title = " ".join(parts[2:])
            template = context.get("template") if context else None
            return await self.create_learning_note(title, template)
        
        elif command == "search" and len(parts) >= 2:
            search_query = " ".join(parts[1:])
            return {"results": await self.search_notes(search_query)}
        
        elif command == "summarize" and len(parts) >= 2:
            note_id = parts[1]
            return await self.summarize_note(note_id)
        
        else:
            return {"error": f"Unknown command: {query}", "isError": True}
    
    async def create_learning_note(
        self,
        title: str,
        template: Optional[str] = "learning",
    ) -> Dict[str, Any]:
        """Create a new learning note with template."""
        try:
            template_content = get_template(template or "learning")
        except ValueError:
            template_content = f"# {title}\n\n---\n\n**Inhalt:** \n\n"
        
        result = await self.create_note(
            title=title,
            content=template_content,
            template=template,
            properties={"type": "learning", "template": template},
        )
        
        logger.info(f"Created learning note: {title}")
        return {
            "status": "success",
            "note_id": result.get("id"),
            "title": title,
            "message": f"Learning note '{title}' created",
        }
    
    async def summarize_note(self, note_id: str) -> Dict[str, Any]:
        """Generate a summary of a learning note."""
        note = await self.get_note(note_id)
        content = note.get("content", "")
        
        # Simple summary extraction (enhance with LLM later)
        lines = content.split("\n")
        summary_lines = [l for l in lines if l.strip() and not l.startswith("#") and not l.startswith("---")]
        summary = " ".join(summary_lines[:5]) + "..." if len(summary_lines) > 5 else content
        
        return {
            "note_id": note_id,
            "title": note.get("title", "Unknown"),
            "summary": summary,
        }
    
    async def create_flashcard(
        self,
        question: str,
        answer: str,
        topic: str = "General",
    ) -> Dict[str, Any]:
        """Create a flashcard for learning."""
        content = f"""# Flashcard

**Frage:** {question}

---

**Antwort:** {answer}

---

**Thema:** {topic}
**Typ:** Flashcard
"""
        
        result = await self.create_note(
            title=f"Flashcard: {question[:30]}...",
            content=content,
            properties={"type": "flashcard", "topic": topic},
        )
        
        return {
            "status": "success",
            "flashcard_id": result.get("id"),
            "question": question,
        }
    
    async def track_progress(
        self,
        topic: str,
        progress: int,  # 0-100
        notes: str = "",
    ) -> Dict[str, Any]:
        """Track learning progress for a topic."""
        content = f"""# Lernfortschritt: {topic}

**Fortschritt:** {progress}%

**Notizen:**
{notes}

**Aktionen:**
- [ ] Weiter lernen
- [ ] Übungen machen
- [ ] Wissen anwenden
"""
        
        result = await self.create_note(
            title=f"Fortschritt: {topic}",
            content=content,
            properties={"type": "progress", "topic": topic, "progress": progress},
        )
        
        return {
            "status": "success",
            "progress_id": result.get("id"),
            "topic": topic,
            "progress": progress,
        }
