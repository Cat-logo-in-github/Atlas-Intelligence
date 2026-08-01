import json

from atlas.utils.paths import GRAPH_FILE
from atlas.utils.filesystem import write_if_changed


def build_graph(modules):

    graph = {
        "nodes": [],
        "edges": []
    }


    for module in modules:

        graph["nodes"].append(
            {
                "id": module.slug,
                "title": module.title
            }
        )


        for related in module.metadata.related:

            graph["edges"].append(
                {
                    "from": module.slug,
                    "to": related
                }
            )


    output = json.dumps(
        graph,
        indent=2
    )


    if write_if_changed(
        GRAPH_FILE,
        output
    ):
        print(
            " ✓ graph.json updated"
        )