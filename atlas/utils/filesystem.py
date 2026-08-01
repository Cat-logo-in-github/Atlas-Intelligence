from pathlib import Path
import shutil


def write_if_changed(
    path: Path,
    content: str
) -> bool:

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if path.exists():

        old = path.read_text(
            encoding="utf-8"
        )

        if old == content:
            return False

    path.write_text(
        content,
        encoding="utf-8"
    )

    return True



def write_if_missing(
    path: Path,
    content: str
) -> bool:

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if path.exists():
        return False

    path.write_text(
        content,
        encoding="utf-8"
    )

    return True



def copy_if_changed(
    source: Path,
    destination: Path
) -> bool:

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if destination.exists():

        if (
            source.read_bytes()
            ==
            destination.read_bytes()
        ):
            return False

    shutil.copy2(
        source,
        destination
    )

    return True