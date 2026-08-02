from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class OutputConfig:

    published: bool = False
    url: str = ""
    build: bool = False



@dataclass
class Outputs:

    quiz: OutputConfig = field(
        default_factory=OutputConfig
    )

    website: OutputConfig = field(
        default_factory=OutputConfig
    )

    youtube: OutputConfig = field(
        default_factory=OutputConfig
    )

    instagram: OutputConfig = field(
        default_factory=OutputConfig
    )

    blog: OutputConfig = field(
        default_factory=OutputConfig
    )

    notebook: OutputConfig = field(
        default_factory=OutputConfig
    )

    simulation: OutputConfig = field(
        default_factory=OutputConfig
    )



@dataclass
class Metadata:

    title: str
    slug: str

    module: str = ""

    created: str = ""

    last_build: str = ""

    updated: bool = True

    content_hash: str = ""

    status: str = "seed"

    difficulty: str = "beginner"

    tags: list[str] = field(
        default_factory=list
    )

    related: list[str] = field(
        default_factory=list
    )

    outputs: Outputs = field(
        default_factory=Outputs
    )


    @classmethod
    def from_file(
        cls,
        path: Path
    ):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = yaml.safe_load(f) or {}


        raw_outputs = data.get(
            "outputs",
            {}
        )


        outputs = Outputs(

            quiz=OutputConfig(
                **raw_outputs.get(
                    "quiz",
                    {}
                )
            ),

            website=OutputConfig(
                **raw_outputs.get(
                    "website",
                    {}
                )
            ),

            youtube=OutputConfig(
                **raw_outputs.get(
                    "youtube",
                    {}
                )
            ),

            instagram=OutputConfig(
                **raw_outputs.get(
                    "instagram",
                    {}
                )
            ),

            blog=OutputConfig(
                **raw_outputs.get(
                    "blog",
                    {}
                )
            ),

            notebook=OutputConfig(
                **raw_outputs.get(
                    "notebook",
                    {}
                )
            ),

            simulation=OutputConfig(
                **raw_outputs.get(
                    "simulation",
                    {}
                )
            ),
        )


        return cls(

            title=data.get(
                "title",
                ""
            ),

            slug=data.get(
                "slug",
                ""
            ),

            module=data.get(
                "module",
                ""
            ),

            created=data.get(
                "created",
                ""
            ),

            last_build=data.get(
                "last_build",
                ""
            ),

            updated=data.get(
                "updated",
                True
            ),

            content_hash=data.get(
                "content_hash",
                ""
            ),

            status=data.get(
                "status",
                "seed"
            ),

            difficulty=data.get(
                "difficulty",
                "beginner"
            ),

            tags=data.get(
                "tags",
                []
            ),

            related=data.get(
                "related",
                []
            ),

            outputs=outputs
        )