import json
from pathlib import Path


def notebook_has_content(
    path: Path
) -> bool:

    if not path.exists():
        return False


    notebook = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


    for cell in notebook.get(
        "cells",
        []
    ):

        source = cell.get(
            "source",
            []
        )


        if isinstance(
            source,
            list
        ):
            text = "".join(source)

        else:
            text = str(source)


        if text.strip():
            return True


    return False



def validate_notebook(
    module
) -> list[str]:

    warnings = []


    if not module.notebook.exists():

        warnings.append(
            "Notebook missing"
        )

        return warnings


    if not notebook_has_content(
        module.notebook
    ):

        warnings.append(
            "Notebook empty"
        )


    return warnings