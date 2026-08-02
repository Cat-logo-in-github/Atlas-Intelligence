from atlas.utils.hash import hash_module
import yaml


def update_module_hash(module):

    current_hash = hash_module(
        module
    )


    metadata_path = (
        module.path /
        "metadata.yaml"
    )


    data = yaml.safe_load(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )


    old_hash = data.get(
        "content_hash",
        ""
    )


    if old_hash == current_hash:
        return False


    data["content_hash"] = current_hash
    data["updated"] = True


    metadata_path.write_text(
        yaml.dump(
            data,
            sort_keys=False
        ),
        encoding="utf-8"
    )


    return True