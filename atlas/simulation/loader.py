import importlib.util
from pathlib import Path


def load_simulation(
    path: Path,
    simulation
):
    """
    Load a single Atlas simulation file and execute its
    build(simulation) function.
    """

    spec = importlib.util.spec_from_file_location(
        path.stem,
        path
    )

    if spec is None or spec.loader is None:

        raise RuntimeError(
            f"Could not load {path}"
        )


    module = importlib.util.module_from_spec(
        spec
    )


    spec.loader.exec_module(
        module
    )


    if not hasattr(
        module,
        "build"
    ):

        raise RuntimeError(
            f"{path.name} has no build(simulation) function."
        )


    simulation.set_context(
        path
    )


    module.build(
        simulation
    )