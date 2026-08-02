from pathlib import Path
import subprocess
import sys
from atlas.validators.module import mark_output_built

def run_simulation(module):

    simulation = module.simulation

    if not simulation.exists():
        return


    run_file = simulation / "run.py"

    if not run_file.exists():
        return


    print(
        f" ▶ Running simulation: {module.slug}"
    )


    try:
        subprocess.run(
            [
                sys.executable,
                str(run_file)
            ],
            cwd=simulation,
            check=True
        )
        mark_output_built(
                module,
                "simulation"
        )

    except subprocess.CalledProcessError:
        print(
            f" ✗ Simulation failed: {module.slug}"
        )