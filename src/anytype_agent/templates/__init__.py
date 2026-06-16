"""
Note templates for the AnyType Agent.
"""

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent


def get_template(template_name: str) -> str:
    """Load a template by name."""
    template_path = TEMPLATES_DIR / f"{template_name}.md"
    if not template_path.exists():
        raise ValueError(f"Template '{template_name}' not found")
    return template_path.read_text(encoding="utf-8")


def list_templates() -> list:
    """List all available templates."""
    return [
        f.stem for f in TEMPLATES_DIR.glob("*.md") if f.is_file()
    ]
