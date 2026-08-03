from pathlib import Path
import json
import shutil
import webbrowser


def validate_model(path: Path):

    if not path.exists():

        raise FileNotFoundError(
            f"Model not found: {path}"
        )


    if not path.is_dir():

        raise TypeError(
            "Model must be a directory"
        )


    index = path / "index.html"


    if not index.exists():

        raise FileNotFoundError(
            "Interactive models require index.html"
        )



def copy_directory(
    source,
    destination
):

    if destination.exists():

        shutil.rmtree(
            destination
        )


    shutil.copytree(
        source,
        destination
    )


def export_models(
    simulation,
    export: bool = True,
):

    for item in simulation.models:

        model = Path(
            item["object"]
        )

        name = item["name"]


        validate_model(
            model
        )


        if not export:

            index = (
                model /
                "index.html"
            )


            webbrowser.open(
                index.resolve().as_uri()
            )

            continue


        output = simulation.output


        model_output = (
            output /
            name
        )


        copy_directory(
            model,
            model_output
        )


        metadata = {
            "type":
                "interactive_model",

            "name":
                name,

            "entry":
                "index.html"
        }


        (
            model_output /
            "atlas_metadata.json"
        ).write_text(

            json.dumps(
                metadata,
                indent=2
            ),

            encoding="utf-8"
        )


        print(
            f"✓ Exported model: {name}"
        )