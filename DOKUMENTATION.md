# AnyType Agent - Projekt-Dokumentation

> **Stand:** 16. Juni 2026  
> **Status:** Projektstruktur fertig, MCP-Server & Agenten implementiert (API-Integration als Stub)  
> **Nächster Schritt:** AnyType API-Integration vervollständigen

---

## 📋 Inhaltsverzeichnis

1. [Überblick](#-überblick)
2. [Projektstruktur](#-projektstruktur)
3. [Architektur](#-architektur)
4. [Komponenten](#-komponenten)
5. [Einrichtung](#-einrichtung)
6. [Verwendete Technologien](#-verwendete-technologien)
7. [Fortschritt & Nächste Schritte](#-fortschritt--nächste-schritte)
8. [Changelog](#-changelog)

---

## 🎯 Überblick

**AnyType Agent** ist ein persönlicher KI-Assistent, der dir hilft:
- 📚 **Zu lernen** – Strukturierte Notizen, Lernfortschritt tracken, Flashcards
- ✍️ **Notizen zu erstellen** – Tagesnotizen, Meeting-Protokolle, Wissensdatenbank
- 🎯 **Dein Leben zu organisieren** – Aufgaben, Projekte, Ziele, Gewohnheiten

Das System nutzt **[AnyType](https://anytype.io)** als zentrale Datenbasis und kommuniziert darüber via **Model Context Protocol (MCP)**.

---

## 📁 Projektstruktur

```
anytypeAgent/
├── DOKUMENTATION.md          # Diese Datei
├── .env.example              # Umgebungsvariablen-Vorlage
├── .python-version           # Python 3.11
├── pyproject.toml            # Projektkonfiguration & Abhängigkeiten
├── README.md
├── data/                     # Lokale Datenspeicherung
├── src/
│   └── anytype_agent/
│       ├── __init__.py       # Paket-Init (Version 0.1.0)
│       ├── __main__.py       # Modul-Einstiegspunkt
│       ├── main.py           # Hauptprogramm
│       ├── config.py         # Einstellungen (Pydantic)
│       ├── mcp/
│       │   ├── __init__.py
│       │   ├── server.py      # MCP-Server für AnyType
│       │   └── client.py      # AnyType API Client (httpx)
│       ├── templates/
│       │   ├── __init__.py    # Template-Lader
│       │   ├── learning.md    # Lernvorlage
│       │   ├── tasks.md       # Aufgabenvorlage
│       │   └── journal.md     # Tagebuchvorlage
│       └── agents/
│           ├── __init__.py
│           ├── base_agent.py  # Basis-Klasse für alle Agenten
│           ├── learning_agent.py   # Lern-Agent
│           ├── notes_agent.py      # Notizen-Agent
│           └── organization_agent.py # Organisations-Agent
└── tests/
    └── __init__.py
```

---

## 🏗️ Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                        AnyType Agent                           │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐ │
│  │  Learning     │    │   Notes      │    │  Organization   │ │
│  │  Agent        │    │   Agent      │    │    Agent        │ │
│  └──────┬────────┘    └──────┬────────┘    └────────┬─────────┘ │
│         │                     │                    │          │
│         └─────────────────────┼────────────────────┘          │
│                           │ │                                  │
│                           ▼ ▼                                  │
│                    ┌─────────────────┐                           │
│                    │   Base Agent    │                           │
│                    │  (Abstrakte Klasse)│                         │
│                    └────────┬────────┘                           │
│                             │                                      │
│                             ▼                                      │
│                    ┌─────────────────┐                           │
│                    │  AnyType Client  │                           │
│                    │   (HTTP/REST)    │                           │
│                    └────────┬────────┘                           │
│                             │                                      │
│                             ▼                                      │
│                    ┌─────────────────┐                           │
│                    │   MCP Server     │                           │
│                    │  (Model Context  │                           │
│                    │   Protocol)      │                           │
│                    └────────┬────────┘                           │
│                             │                                      │
│                             ▼                                      │
│                    ┌─────────────────┐                           │
│                    │     AnyType     │                           │
│                    │   API (Cloud)   │                           │
│                    └─────────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Komponenten

### 1. MCP-Server (`src/anytype_agent/mcp/`)

Der **Model Context Protocol** Server stellt Tools bereit, um mit AnyType zu interagieren.

#### ✅ Implementierte Tools

| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `create_object` | Erstellt ein neues Objekt (Notiz, Aufgabe, etc.) | `type`, `title`, `content?`, `template?`, `properties?` |
| `get_object` | Holt ein Objekt per ID | `object_id` |
| `search_objects` | Sucht nach Objekten | `query`, `type?`, `limit?` |
| `update_object` | Aktualisiert ein Objekt | `object_id`, `updates` |
| `delete_object` | Löscht ein Objekt | `object_id` |

#### 📝 Status
- ✅ Server-Struktur implementiert
- ✅ Tool-Definitionen erstellt
- ✅ Handler-Methoden als Stub (_return Mock-Daten)
- ⚠️ **TODO:** Echte AnyType API-Aufrufe integrieren

#### 🔗 AnyType API Client (`client.py`)

Bereit für echte HTTP-Anfragen an die AnyType API:
- `create_object()` – Objekt anlegen
- `get_object()` – Objekt abrufen
- `update_object()` – Objekt aktualisieren
- `delete_object()` – Objekt löschen
- `search_objects()` – Objekte suchen
- `list_templates()` – Vorlagen auflisten

**Benötigt:** `ANYTYPE_API_KEY` und `ANYTYPE_SPACE_ID` in `.env`

---

### 2. Agenten (`src/anytype_agent/agents/`)

Jeder Agent erbt von `BaseAgent` und bietet spezialisierte Funktionen.

#### 🎓 LearningAgent

**Zweck:** Wissensmanagement und Lernunterstützung

**Funktionen:**
- `create_learning_note(title, template)` – Erstellt strukturierte Lernnotizen
- `summarize_note(note_id)` – Generiert Zusammenfassungen
- `create_flashcard(question, answer, topic)` – Erstellt Karteikarten
- `track_progress(topic, progress, notes)` – Trackt Lernfortschritt

**Verwendete Vorlage:** `templates/learning.md`

**Beispiel-Befehle:**
```python
create note "Python Grundlagen"
search "Algorithmen"
summarize <note_id>
```

#### ✍️ NotesAgent

**Zweck:** Allgemeine Notizenverwaltung

**Funktionen:**
- `create_note_by_type(note_type, title, template)` – Erstellt Notizen nach Typ
- `create_daily_note(date)` – Tagesnotiz erstellen
- `create_meeting_note(title, participants, agenda)` – Meeting-Protokoll
- `link_notes(note_id_1, note_id_2, relation)` – Verknüpft Notizen
- `list_recent_notes(limit)` – Zeigt letzte Notizen

**Unterstützte Notiz-Typen:**
- `daily` / `journal` → `templates/journal.md`
- `task` → `templates/tasks.md`
- `learning` → `templates/learning.md`
- `meeting` → Generische Meeting-Vorlage

**Beispiel-Befehle:**
```python
create daily "Tagebuch 16.06.2026"
create meeting "Team Sync" --participants ["Max", "Anna"]
list templates
get <note_id>
```

#### 🎯 OrganizationAgent

**Zweck:** Aufgaben-, Projekt- und Zeitmanagement

**Funktionen:**
- `create_task(title, context)` – Erstellt Aufgaben mit Projekt, Priorität, Fälligkeit
- `create_project(name)` – Erstellt ein neues Projekt
- `create_goal(description)` – Erstellt ein Ziel
- `create_habit(name)` – Erstellt eine Gewohnheits-Tracker
- `list_objects(obj_type)` – Listet Objekte nach Typ
- `complete_task(task_id)` – Markiert Aufgabe als erledigt
- `get_weekly_review()` – Generiert wöchentliche Review

**Beispiel-Befehle:**
```python
create task "AnyType API integrieren" --project "AnyType Agent" --priority "🔴 Hoch"
create project "AnyType Agent"
create goal "Python Meister werden"
create habit "Täglich 30min lernen"
list tasks
complete <task_id>
```

---

### 3. Vorlagen-System (`src/anytype_agent/templates/`)

Markdown-basierte Vorlagen mit Platzhaltern im Format `{{variable}}`.

#### 📄 Verfügbare Vorlagen

| Vorlage | Typ | Beschreibung |
|---------|-----|--------------|
| `learning.md` | Lernnotiz | Struktur für Wissensaufbau mit Zielen, Konzepten, Fragen |
| `tasks.md` | Aufgabe | Aufgabenmanagement mit Priorität, Fälligkeit, Unteraufgaben |
| `journal.md` | Tagebuch | Tagesstruktur mit Stimmung, Zielen, Reflexion |

#### 🔧 Platzhalter-Ersetzung

Automatisch ersetzte Variablen:
- `{{date}}` → Aktuelles Datum (YYYY-MM-DD)
- `{{today}}` → Aktuelles Datum (YYYY-MM-DD)

Manuell zu füllende Platzhalter (per Agent oder Benutzer):
- `{{title}}`, `{{category}}`, `{{topic}}`, `{{project}}`, `{{priority}}`, etc.

---

### 4. Konfiguration (`src/anytype_agent/config.py`)

Verwendet **Pydantic** für typsichere Einstellungen.

#### 📝 Umweltvariablen (`.env`)

```bash
# AnyType API
ANYTYPE_API_KEY=your_api_key_here
ANYTYPE_SPACE_ID=your_space_id_here
ANYTYPE_API_URL=https://api.anytype.io

# MCP Server
MCP_HOST=localhost
MCP_PORT=8080
MCP_LOG_LEVEL=INFO

# Application
LOG_LEVEL=INFO
DATA_DIR=./data
```

**Hinweis:** `.env.example` ist bereits vorhanden – kopiere sie zu `.env` und trage deine Werte ein.

---

## ⚙️ Einrichtung

### 1. Git-Repository (✅ erledigt)

```bash
# Bereits geplant:
git init
git add -A
git commit -m "feat: Initial project structure"
```

### 2. Virtuelle Umgebung mit uv (✅ erledigt)

```bash
# Bereits vorhanden:
uv init
```

### 3. Abhängigkeiten installieren

```bash
# Standard-Abhängigkeiten
uv sync

# Entwicklungs-Abhängigkeiten (optional)
uv sync --all-extras
```

#### 📦 Abhängigkeiten (pyproject.toml)

**Haupt-Abhängigkeiten:**
- `pydantic>=2.0.0` – Konfiguration & Datenvalidierung
- `httpx>=0.25.0` – HTTP-Client für AnyType API
- `python-dotenv>=1.0.0` – .env Datei Support

**Entwicklungs-Abhängigkeiten:**
- `pytest>=7.0.0` – Testing
- `pytest-asyncio>=0.21.0` – Async Test Support
- `black>=23.0.0` – Code Formatierung
- `ruff>=0.1.0` – Linting
- `mypy>=1.0.0` – Typprüfung

### 4. Projekt ausführen

```bash
# Als Modul
python -m anytype_agent

# Über Einstiegspunkt (nach Installation)
anytype-agent
```

---

## 🛠 Verwendete Technologien

| Komponente | Technologie | Zweck |
|-----------|-------------|-------|
| **Sprache** | Python 3.11+ | Haupt-Programmiersprache |
| **Paketmanager** | uv | Schnelle Abhängigkeitsverwaltung |
| **HTTP-Client** | httpx | Async HTTP-Anfragen an AnyType API |
| **Konfiguration** | Pydantic | Typsichere Einstellungen |
| **Umgebungsvariablen** | python-dotenv | .env Datei Support |
| **Protokoll** | MCP (Model Context Protocol) | Standardisierte Tool-Schnittstelle |
| **Datenbasis** | AnyType | Cloud-basiertes Notiz- und Wissenssystem |
| **Testing** | pytest | Unit-Tests |
| **Formatierung** | black | Code-Stil |
| **Linting** | ruff | Code-Qualität |
| **Typprüfung** | mypy | Statische Typanalyse |

---

## 📊 Fortschritt & Nächste Schritte

### ✅ Erledigt

- [x] Git-Repository initialisiert
- [x] Virtuelle Umgebung mit uv eingerichtet
- [x] Projektstrukturcreated (`src/`, `tests/`, `data/`)
- [x] pyproject.toml mit Abhängigkeiten und Konfiguration
- [x] AnyTypeClient (API-Client) implementiert
- [x] MCP-Server mit 5 Tools definiert
- [x] BaseAgent als abstrakte Basis-Klasse
- [x] LearningAgent mit Lernfunktionen
- [x] NotesAgent mit Notizenverwaltung
- [x] OrganizationAgent mit Aufgabenmanagement
- [x] 3 Vorlagen (learning, tasks, journal)
- [x] Konfigurationssystem mit Pydantic
- [x] .env.example für Umgebungsvariablen
- [x] Erste Commit erstellt

### 🔄 In Arbeit

- [ ] AnyType API-Integration vervollständigen (echte Anfragen in client.py)
- [ ] MCP-Server mit echten AnyType-Aufrufen verbinden
- [ ] Tests für Agenten und MCP-Server schreiben
- [ ] CLI-Schnittstelle für Benutzerinteraktion
- [ ] Docker-Container für einfache Bereitstellung

### 📋 Geplant (später)

- [ ] Web-Interface (optional)
- [ ] Integration mit anderen Tools (Calendar, E-Mail)
- [ ] KI-basierte Notizen-Generierung (LLM)
- [ ] Synchronisation mit lokalen Dateien
- [ ] Backup & Restore Funktionalität
- [ ] Plugin-System für Erweiterungen
- [ ] Multi-User Support

---

## 📜 Changelog

### v0.1.0 (16. Juni 2026)

**Erste Version – Projekt-Grundgerüst**

- Projektstruktur mit `src/` und `tests/` Verzeichnissen
- uv-basiertes Python-Projekt mit pyproject.toml
- 3 Agenten: Learning, Notes, Organization
- MCP-Server für AnyType-Integration (Stub-Implementierung)
- 3 Notiz-Vorlagen: Lernen, Aufgaben, Tagebuch
- Konfigurationssystem mit Pydantic und .env Support
- Abhängigkeiten: pydantic, httpx, python-dotenv

**Commit:** `d0022be` – "feat: Initial project structure with agents, MCP server, and templates"

---

## 💡 Tipps & Hinweise

### AnyType API Zugang

1. Registriere dich unter [https://anytype.io](https://anytype.io)
2. Erstelle einen API-Key in den Einstellungen
3. Finde deine Space-ID (Workspace-ID) in der URL oder Einstellungen
4. Trage beide in `.env` ein:
   ```bash
   ANYTYPE_API_KEY=dein_api_key
   ANYTYPE_SPACE_ID=deine_space_id
   ```

### MCP-Server testen

Der MCP-Server kann unabhängig getestet werden:

```python
from anytype_agent.mcp.server import AnyTypeMCPServer, start_mcp_server

server = AnyTypeMCPServer()
print(f"Verfügbare Tools: {list(server.tools.keys())}")

# Beispiel: Tool-Aufruf testen
import asyncio
result = asyncio.run(server.handle_tool_call("create_object", {"type": "note", "title": "Test"}))
print(result)
```

### Agenten direkt nutzen

```python
import asyncio
from anytype_agent.agents import LearningAgent, NotesAgent, OrganizationAgent

async def test_agents():
    # Learning Agent
    learning = LearningAgent()
    result = await learning.create_learning_note("Python Grundlagen")
    print(f"Lernnotiz erstellt: {result['note_id']}")
    
    # Notes Agent
    notes = NotesAgent()
    result = await notes.create_daily_note()
    print(f"Tagesnotiz erstellt: {result['note_id']}")
    
    # Organization Agent
    org = OrganizationAgent()
    result = await org.create_task("API integrieren")
    print(f"Aufgabe erstellt: {result['task_id']}")

asyncio.run(test_agents())
```

**Hinweis:** Ohne echte AnyType API-Integration geben die Methoden Mock-Daten zurück.

---

## 📞 Support & Ressourcen

- **AnyType API Dokumentation:** [https://developers.anytype.io](https://developers.anytype.io)
- **MCP Spezifikation:** [https://github.com/modelcontextprotocol/spec](https://github.com/modelcontextprotocol/spec)
- **Python uv:** [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

---

*Dokumentation zuletzt aktualisiert: 16. Juni 2026*
