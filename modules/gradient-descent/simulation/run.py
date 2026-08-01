from pathlib import Path
import importlib.util

from atlas.simulation import Simulation


BASE_DIR = Path(__file__).parent

OUTPUT_DIR = BASE_DIR / "outputs"


simulation = Simulation(
    output=OUTPUT_DIR
)


def load_simulation(path: Path):

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
        print(
            f"⚠ Skipping {path.name}: no build(simulation)"
        )
        return


    simulation.set_context(path)

    module.build(simulation)


def main():

    simulation_files = sorted(
        BASE_DIR.glob(
            "simulation*.py"
        )
    )


    if not simulation_files:
        print(
            "No simulation files found."
        )
        return


    for file in simulation_files:

        try:

            print(
                f"Loading {file.name}"
            )

            load_simulation(
                file
            )

        except Exception as e:

            print(
                f"✗ Failed {file.name}: {e}"
            )


    print(
        "Exporting simulation outputs..."
    )

    simulation.export()


    print(
        "✓ Simulation complete"
    )


if __name__ == "__main__":
    main()