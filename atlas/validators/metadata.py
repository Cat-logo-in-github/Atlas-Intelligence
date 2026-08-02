def validate_metadata(module):

    warnings = []

    metadata = module.metadata

    if not metadata.title:
        warnings.append(
            "Missing title"
        )

    if not metadata.slug:
        warnings.append(
            "Missing slug"
        )

    if not metadata.status:
        warnings.append(
            "Missing status"
        )

    return warnings