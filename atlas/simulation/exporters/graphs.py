from pathlib import Path
import json

import plotly.graph_objects as go


def normalize_graph(graph):

    # Dictionary contract
    if isinstance(graph, dict):

        return {
            "nodes": graph.get("nodes", []),
            "edges": graph.get("edges", [])
        }

    try:

        import networkx as nx

        if isinstance(graph, nx.Graph):

            nodes = []

            for node, attrs in graph.nodes(data=True):

                nodes.append(
                    {
                        "id": str(node),
                        **attrs
                    }
                )

            edges = []

            for source, target, attrs in graph.edges(data=True):

                edges.append(
                    {
                        "source": str(source),
                        "target": str(target),
                        **attrs
                    }
                )

            return {
                "nodes": nodes,
                "edges": edges
            }

    except ImportError:
        pass

    raise TypeError(
        "Unsupported graph type"
    )


def build_positions(data):

    node_lookup = {
        node["id"]: node
        for node in data["nodes"]
    }

    # Use supplied coordinates if every node has them.

    if all(
        "x" in node and "y" in node
        for node in data["nodes"]
    ):

        return {
            node["id"]: (
                node["x"],
                node["y"]
            )
            for node in data["nodes"]
        }

    # Otherwise use spring layout.

    try:

        import networkx as nx

        g = nx.DiGraph()

        for node in data["nodes"]:
            g.add_node(node["id"])

        for edge in data["edges"]:
            g.add_edge(
                edge["source"],
                edge["target"]
            )

        return nx.spring_layout(
            g,
            seed=42
        )

    except Exception:

        import math

        positions = {}

        total = max(
            len(data["nodes"]),
            1
        )

        for i, node in enumerate(data["nodes"]):

            angle = (
                2 *
                math.pi *
                i /
                total
            )

            positions[node["id"]] = (
                math.cos(angle),
                math.sin(angle)
            )

        return positions


def build_plotly_graph(data):

    positions = build_positions(data)

    edge_x = []
    edge_y = []

    edge_hover_x = []
    edge_hover_y = []
    edge_hover = []

    for edge in data["edges"]:

        x0, y0 = positions[
            edge["source"]
        ]

        x1, y1 = positions[
            edge["target"]
        ]

        edge_x.extend(
            [
                x0,
                x1,
                None
            ]
        )

        edge_y.extend(
            [
                y0,
                y1,
                None
            ]
        )

        label = (
            edge.get("label")
            or edge.get("weight")
            or ""
        )

        if label:

            edge_hover_x.append(
                (x0 + x1) / 2
            )

            edge_hover_y.append(
                (y0 + y1) / 2
            )

            edge_hover.append(
                str(label)
            )

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            width=1,
            color="#888"
        ),
        hoverinfo="none"
    )

    edge_label_trace = go.Scatter(
        x=edge_hover_x,
        y=edge_hover_y,
        mode="markers",
        marker=dict(
            size=8,
            opacity=0
        ),
        text=edge_hover,
        hoverinfo="text",
        showlegend=False
    )

    node_x = []
    node_y = []

    node_text = []
    hover_text = []

    node_sizes = []
    node_colors = []

    for node in data["nodes"]:

        x, y = positions[
            node["id"]
        ]

        node_x.append(x)
        node_y.append(y)

        node_text.append(
            node.get(
                "label",
                node["id"]
            )
        )

        hover = []

        for key, value in node.items():

            if key in {
                "id",
                "label",
                "x",
                "y",
                "color",
                "size"
            }:
                continue

            hover.append(
                f"{key}: {value}"
            )

        hover_text.append(
            "<br>".join(hover)
        )

        node_sizes.append(
            node.get(
                "size",
                20
            )
        )

        node_colors.append(
            node.get(
                "color",
                "#2563eb"
            )
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hovertext=hover_text,
        hoverinfo="text",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(
                color="white",
                width=1
            )
        )
    )

    fig = go.Figure(
        data=[
            edge_trace,
            edge_label_trace,
            node_trace
        ]
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor="white"
    )

    return fig


def export_graphs(simulation):

    for item in simulation.graphs:

        graph = item["object"]
        name = item["name"]

        data = normalize_graph(graph)

        (simulation.output / f"{name}.json").write_text(
            json.dumps(
                data,
                indent=2
            ),
            encoding="utf-8"
        )

        fig = build_plotly_graph(data)

        fig.write_html(
            simulation.output / f"{name}.html"
        )

        try:

            fig.write_image(
                simulation.output / f"{name}.png"
            )

            fig.write_image(
                simulation.output / f"{name}.svg"
            )

        except Exception as e:

            print(
                f"⚠ Could not render static graph images: {e}"
            )

        print(
            f"✓ Exported graph: {name}"
        )