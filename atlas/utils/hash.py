import hashlib


IGNORED_FILES = {
    "metadata.yaml",
    ".DS_Store",
}


IGNORED_DIRS = {
    "__pycache__",
    "generated",
}


def hash_module(module):

    sha = hashlib.sha256()


    for file in sorted(
        module.path.rglob("*")
    ):

        if not file.is_file():
            continue


        if file.name in IGNORED_FILES:
            continue


        if any(
            directory in file.parts
            for directory in IGNORED_DIRS
        ):
            continue


        # Include path so renaming/moving files changes the hash
        relative_path = file.relative_to(
            module.path
        )


        sha.update(
            str(relative_path)
            .encode("utf-8")
        )


        # Include file contents
        sha.update(
            file.read_bytes()
        )


    return sha.hexdigest()