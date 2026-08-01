from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR, TEMPLATES_DIR
import typer

RUN_TEMPLATE = (
    TEMPLATES_DIR /
    "run.py"
).read_text(
    encoding="utf-8"
)


def generate_simulation(
    slug: str
):

    module_path = MODULES_DIR / slug

    if not module_path.exists():
        raise typer.Exit(
            f"Unknown module: {slug}"
        )

    module = Module(module_path)

    path = (
        module.simulation /
        "run.py"
    )

    path.write_text(
        RUN_TEMPLATE,
        encoding="utf-8"
    )

    print(
        f"✓ Generated {path}"
    )