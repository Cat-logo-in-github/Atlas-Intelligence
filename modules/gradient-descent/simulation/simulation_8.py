import plotly.graph_objects as go
import networkx as nx
import numpy as np


def build(simulation):
    brain = nx.DiGraph()

    nodes = [
        ("Eye", 0, 0),
        ("Optic Nerve", 1.5, 0),
        ("Optic Chiasm", 3, 0),
        ("Optic Tract", 4.5, 0),
        ("Lateral Geniculate Nucleus", 6, 0.7),
        ("Optic Radiation", 7.5, 0.7),
        ("Primary Visual Cortex", 9, 0.7),
        ("Visual Association Cortex", 10.5, 0.7),
        ("Superior Colliculus", 6, -1),
        ("Cerebellum", 8, -1.3),
    ]

    for name, x, y in nodes:
        brain.add_node(name, x=x, y=y)

    edges = [
        ("Eye", "Optic Nerve"),
        ("Optic Nerve", "Optic Chiasm"),
        ("Optic Chiasm", "Optic Tract"),
        ("Optic Tract", "Lateral Geniculate Nucleus"),
        ("Lateral Geniculate Nucleus", "Optic Radiation"),
        ("Optic Radiation", "Primary Visual Cortex"),
        ("Primary Visual Cortex", "Visual Association Cortex"),
        ("Optic Tract", "Superior Colliculus"),
        ("Superior Colliculus", "Cerebellum"),
    ]

    brain.add_edges_from(edges)

    simulation.graph(brain, "visual_pathway_network")

    frames = []

    node_x = [data["x"] for _, data in brain.nodes(data=True)]
    node_y = [data["y"] for _, data in brain.nodes(data=True)]
    node_labels = list(brain.nodes())

    base_edge_x = []
    base_edge_y = []
    for a, b in edges:
        base_edge_x.extend([
            brain.nodes[a]["x"],
            brain.nodes[b]["x"],
            None
        ])
        base_edge_y.extend([
            brain.nodes[a]["y"],
            brain.nodes[b]["y"],
            None
        ])

    base_edges = go.Scatter(
        x=base_edge_x,
        y=base_edge_y,
        mode="lines",
        line=dict(color="rgba(80,120,120,0.35)", width=3),
        hoverinfo="none"
    )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        marker=dict(
            size=28,
            color="rgb(30,80,90)",
            line=dict(color="rgb(120,230,220)", width=2)
        ),
        hoverinfo="text"
    )

    signal_edges = []
    for index in range(len(edges)):
        active = edges[:index + 1]

        sx = []
        sy = []

        for a, b in active:
            sx.extend([
                brain.nodes[a]["x"],
                brain.nodes[b]["x"],
                None
            ])
            sy.extend([
                brain.nodes[a]["y"],
                brain.nodes[b]["y"],
                None
            ])

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=sx,
                        y=sy,
                        mode="lines",
                        line=dict(
                            color="rgb(0,255,200)",
                            width=6
                        ),
                        hoverinfo="none"
                    )
                ],
                name=f"signal_{index}"
            )
        )

    animation = go.Figure(
        data=[
            base_edges,
            node_trace,
            go.Scatter(
                x=[],
                y=[],
                mode="lines",
                line=dict(color="rgb(0,255,200)", width=6)
            )
        ],
        layout=go.Layout(
            title="Visual Information Flow Through the Brain",
            xaxis=dict(
                visible=False,
                range=[-1, 12]
            ),
            yaxis=dict(
                visible=False,
                range=[-2, 2]
            ),
            template="plotly_dark",
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play Signal",
                            method="animate",
                            args=[
                                None,
                                {
                                    "frame": {
                                        "duration": 900,
                                        "redraw": True
                                    },
                                    "fromcurrent": True
                                }
                            ]
                        )
                    ]
                )
            ]
        ),
        frames=frames
    )

    simulation.animation(animation, "visual_signal_animation")