from dataclasses import dataclass, field

from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR
from atlas.validators.hash import update_module_hash
from atlas.validators.metadata import validate_metadata


@dataclass
class ModuleStatus:

    slug: str

    changed: bool = False

    ready: bool = True

    metadata_errors: list[str] = field(
        default_factory=list
    )

    missing: list[str] = field(
        default_factory=list
    )


@dataclass
class AtlasStatus:

    total_modules: int = 0

    synced: int = 0

    changed: list[ModuleStatus] = field(
        default_factory=list
    )

    incomplete: list[ModuleStatus] = field(
        default_factory=list
    )


def check_module_state(module):

    status = ModuleStatus(
        slug=module.slug
    )


    # Detect content changes
    status.changed = update_module_hash(
        module
    )


    # Metadata validation
    errors = validate_metadata(
        module
    )

    if errors:

        status.ready = False

        status.metadata_errors.extend(
            errors
        )


    # Basic content checks
    if not module.knowledge.exists():

        status.ready = False

        status.missing.append(
            "knowledge.md"
        )


    if not module.generated.exists():

        status.ready = False

        status.missing.append(
            "generated"
        )


    return status



def sync():

    result = AtlasStatus()


    modules = Module.load_all(
        MODULES_DIR
    )


    result.total_modules = len(
        modules
    )


    for module in modules:

        status = check_module_state(
            module
        )


        if status.changed:

            result.changed.append(
                status
            )


        if not status.ready:

            result.incomplete.append(
                status
            )


        if (
            not status.changed
            and status.ready
        ):

            result.synced += 1



    return result