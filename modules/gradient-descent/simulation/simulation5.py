from pathlib import Path


def build(simulation):

    simulation.model(
        Path("test_model"),
        "hello_world"
    )