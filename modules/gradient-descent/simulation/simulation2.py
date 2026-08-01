def build(simulation):

    simulation.graph(
        {
            "nodes": [
                {"id": "A"},
                {"id": "B"},
                {"id": "C"}
            ],

            "edges": [
                {
                    "source": "A",
                    "target": "B"
                },
                {
                    "source": "B",
                    "target": "C"
                }
            ]
        },
        name="test_graph"
    )