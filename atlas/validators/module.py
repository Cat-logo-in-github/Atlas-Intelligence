from datetime import datetime
import yaml


def module_needs_build(module):

    return module.metadata.updated


def mark_module_updated(module):

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


    path.write_text(
        yaml.dump(
            data,
            sort_keys=False
        ),
        encoding="utf-8"
    )

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