from pathlib import Path


def find_project_root() -> Path:
    current = Path.cwd()

    while current != current.parent:

        if (current / "pyproject.toml").exists():
            return current

        current = current.parent

    raise RuntimeError(
        "Could not find Atlas project root."
    )


PROJECT_ROOT = find_project_root()

MODULES_DIR = PROJECT_ROOT / "modules"

WEBSITE_DIR = PROJECT_ROOT / "website"

TEMPLATES_DIR = PROJECT_ROOT / "atlas" / "templates"

OUTPUTS_DIR = PROJECT_ROOT / "atlas" / "outputs"

GRAPH_FILE = PROJECT_ROOT / "graph.json"