from datetime import datetime
import yaml


def module_needs_build(module):

    return module.metadata.updated


def mark_module_built(module):

    path = (
        module.path /
        "metadata.yaml"
    )


    data = yaml.safe_load(
        path.read_text(
            encoding="utf-8"
        )
    )


    data["updated"] = False

    data["last_build"] = (
        datetime.now()
        .isoformat()
    )


    path.write_text(
        yaml.dump(
            data,
            sort_keys=False
        ),
        encoding="utf-8"
    )

    print(f"✓ Module '{module.metadata.title}' marked as built")

def mark_output_published(
    module,
    output,
    url=None
):

    path = (
        module.path /
        "metadata.yaml"
    )


    data = yaml.safe_load(
        path.read_text(
            encoding="utf-8"
        )
    )


    if "outputs" not in data:
        data["outputs"] = {}


    if output not in data["outputs"]:
        data["outputs"][output] = {}


    data["outputs"][output]["published"] = True


    if url is not None:
        data["outputs"][output]["url"] = url


    path.write_text(
        yaml.dump(
            data,
            sort_keys=False
        ),
        encoding="utf-8"
    )

def mark_output_built(
    module,
    output
):

    path = (
        module.path /
        "metadata.yaml"
    )


    data = yaml.safe_load(
        path.read_text(
            encoding="utf-8"
        )
    )


    if "outputs" not in data:
        data["outputs"] = {}


    if output not in data["outputs"]:
        data["outputs"][output] = {}


    data["outputs"][output]["build"] = False


    path.write_text(
        yaml.dump(
            data,
            sort_keys=False
        ),
        encoding="utf-8"
    )