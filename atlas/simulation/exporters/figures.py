from pathlib import Path

import matplotlib.figure
import plotly.graph_objects as go


def export_figures(
    simulation,
    export: bool = True,
):

    for item in simulation.figures:

        figure = item["object"]
        name = item["name"]

        if isinstance(
            figure,
            matplotlib.figure.Figure
        ):

            export_matplotlib(
                figure,
                name,
                simulation.output,
                export=export,
            )

        elif isinstance(
            figure,
            go.Figure
        ):

            export_plotly(
                figure,
                name,
                simulation.output,
                export=export,
            )

        else:

            print(
                f"⚠ Unknown figure type: {type(figure)}"
            )


def export_matplotlib(
    figure,
    name: str,
    output: Path,
    export: bool = True,
):

    if not export:

        figure.show()

        return


    png_path = (
        output /
        f"{name}.png"
    )

    svg_path = (
        output /
        f"{name}.svg"
    )


    figure.savefig(
        png_path,
        dpi=300,
        bbox_inches="tight"
    )


    figure.savefig(
        svg_path,
        format="svg",
        bbox_inches="tight"
    )


    print(
        f"✓ Exported matplotlib figure: {name}"
    )


def export_plotly(
    figure,
    name: str,
    output: Path,
    export: bool = True,
):

    if not export:

        figure.show()

        return


    html_path = (
        output /
        f"{name}.html"
    )


    png_path = (
        output /
        f"{name}.png"
    )


    svg_path = (
        output /
        f"{name}.svg"
    )


    figure.write_html(
        html_path
    )


    try:

        figure.write_image(
            png_path
        )

        figure.write_image(
            svg_path
        )

    except Exception as e:

        print(
            f"⚠ Plotly static export failed for {name}: {e}"
        )


    print(
        f"✓ Exported plotly figure: {name}"
    )