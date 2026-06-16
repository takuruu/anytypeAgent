"""
Organization Agent - Helps with task management and life organization.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from anytype_agent.agents.base_agent import BaseAgent
from anytype_agent.templates import get_template

logger = logging.getLogger(__name__)


class OrganizationAgent(BaseAgent):
    """
    Agent specialized in organization and productivity.
    
    Capabilities:
    - Create and manage tasks
    - Set up projects and goals
    - Track habits
    - Manage schedules
    """
    
    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process organization-related queries.
        
        Supported commands:
        - create task <title> [--project <name>] [--priority <level>] [--due <date>]
        - create project <name>
        - create goal <description>
        - list [tasks|projects|goals]
        - complete <task_id>
        """
        parts = query.split()
        command = parts[0].lower() if parts else ""
        
        if command == "create":
            if len(parts) >= 3:
                obj_type = parts[1]
                name = " ".join(parts[2:])
                
                if obj_type == "task":
                    return await self.create_task(name, context)
                elif obj_type == "project":
                    return await self.create_project(name)
                elif obj_type == "goal":
                    return await self.create_goal(name)
                elif obj_type == "habit":
                    return await self.create_habit(name)
        
        elif command == "list":
            obj_type = parts[1] if len(parts) >= 2 else "tasks"
            return await self.list_objects(obj_type)
        
        elif command == "complete" and len(parts) >= 2:
            obj_id = parts[1]
            return await self.complete_task(obj_id)
        
        else:
            return {"error": f"Unknown command: {query}", "isError": True}
    
    async def create_task(
        self,
        title: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new task."""
        project = (context or {}).get("project", "Persönlich")
        priority = (context or {}).get("priority", "🟡 Mittel")
        due_date = (context or {}).get("due", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        
        try:
            template_content = get_template("tasks")
            template_content = template_content.replace("{{title}}", title)
            template_content = template_content.replace("{{project}}", project)
            template_content = template_content.replace("{{priority}}", priority)
            template_content = template_content.replace("{{due_date}}", due_date)
        except ValueError:
            template_content = f"# {title}\n\n**Projekt:** {project}\n\n**Priorität:** {priority}\n\n**Fällig:** {due_date}\n\n"
        
        result = await self.create_note(
            title=title,
            content=template_content,
            template="tasks",
            properties={
                "type": "task",
                "project": project,
                "priority": priority,
                "due_date": due_date,
                "status": "⏳ Todo",
            },
        )
        
        logger.info(f"Created task: {title} (Project: {project})")
        return {
            "status": "success",
            "task_id": result.get("id"),
            "title": title,
            "project": project,
            "priority": priority,
            "due_date": due_date,
        }
    
    async def create_project(self, name: str) -> Dict[str, Any]:
        """Create a new project."""
        content = f"""# Projekt: {name}

**Status:** 🟢 Aktiv
**Erstellt:** {datetime.now().strftime("%Y-%m-%d")}

---

## Beschreibung


---

## Aufgaben

- [ ] Aufgabe 1 hinzufügen
- [ ] Aufgabe 2 hinzufügen

---

## Meilensteine

- [ ] Meilenstein 1
- [ ] Meilenstein 2

---

## Notizen

"""
        
        result = await self.create_note(
            title=f"Projekt: {name}",
            content=content,
            properties={"type": "project", "status": "Aktiv"},
        )
        
        logger.info(f"Created project: {name}")
        return {
            "status": "success",
            "project_id": result.get("id"),
            "name": name,
        }
    
    async def create_goal(self, description: str) -> Dict[str, Any]:
        """Create a new goal."""
        content = f"""# Ziel: {description}

**Status:** 🎯 Im Fortschritt
**Erstellt:** {datetime.now().strftime("%Y-%m-%d")}

---

## Maßnahmen

- [ ] Maßnahme 1
- [ ] Maßnahme 2

---

## Fortschritt

0%

---

## Reflexion

"""
        
        result = await self.create_note(
            title=f"Ziel: {description}",
            content=content,
            properties={"type": "goal", "status": "Im Fortschritt", "progress": 0},
        )
        
        logger.info(f"Created goal: {description}")
        return {
            "status": "success",
            "goal_id": result.get("id"),
            "description": description,
        }
    
    async def create_habit(self, name: str) -> Dict[str, Any]:
        """Create a new habit tracker."""
        content = f"""# Gewohnheit: {name}

**Beschreibung:** 

---

## Tracking

| Datum | Erledigt |
|-------|----------|
| {datetime.now().strftime("%Y-%m-%d")} | [ ] |
| {(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")} | [ ] |
| {(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")} | [ ] |

---

## Statistik

- **Aktuelle Serie:** 0 Tage
- **Beste Serie:** 0 Tage
- **Gesamt:** 0/0 Tage

---

## Motivation

Warum ist diese Gewohnheit wichtig?

"""
        
        result = await self.create_note(
            title=f"Gewohnheit: {name}",
            content=content,
            properties={"type": "habit", "streak": 0},
        )
        
        logger.info(f"Created habit: {name}")
        return {
            "status": "success",
            "habit_id": result.get("id"),
            "name": name,
        }
    
    async def list_objects(self, obj_type: str) -> Dict[str, Any]:
        """List objects of a specific type."""
        results = await self.search_notes(f"type:{obj_type}", limit=50)
        return {
            "type": obj_type,
            "count": len(results),
            "items": results,
        }
    
    async def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as completed."""
        note = await self.get_note(task_id)
        
        # Update status
        properties = note.get("properties", {})
        properties["status"] = "✅ Erledigt"
        properties["completedAt"] = datetime.now().isoformat()
        
        result = await self.update_note(task_id, {"properties": properties})
        
        logger.info(f"Completed task: {task_id}")
        return {
            "status": "success",
            "task_id": task_id,
            "completed_at": datetime.now().isoformat(),
        }
    
    async def get_weekly_review(self) -> Dict[str, Any]:
        """Generate a weekly review."""
        # Search for this week's tasks
        start_of_week = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        tasks = await self.search_notes(f"type:task createdAt:>={start_of_week}")
        
        completed = [t for t in tasks if t.get("properties", {}).get("status") == "✅ Erledigt"]
        pending = [t for t in tasks if t.get("properties", {}).get("status") != "✅ Erledigt"]
        
        content = f"""# Wöchentliche Überprüfung

**Woche:** {start_of_week} - {(datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime("%Y-%m-%d")}

---

## Statistik

- **Gesamt Aufgaben:** {len(tasks)}
- **Erledigt:** {len(completed)}
- **Offen:** {len(pending)}

---

## Erledigte Aufgaben

{chr(10).join([f\"- [x] {t.get('title', 'Unbekannt')}\" for t in completed])}

---

## Offene Aufgaben

{chr(10).join([f\"- [ ] {t.get('title', 'Unbekannt')}\" for t in pending])}

---

## Reflexion

**Was lief gut?** 

**Was kann verbessert werden?** 

**Ziele für nächste Woche:** 
"""
        
        result = await self.create_note(
            title=f"Wöchentliche Überprüfung - {start_of_week}",
            content=content,
            properties={"type": "weekly-review"},
        )
        
        return {
            "status": "success",
            "review_id": result.get("id"),
            "week": start_of_week,
            "completed": len(completed),
            "pending": len(pending),
        }
