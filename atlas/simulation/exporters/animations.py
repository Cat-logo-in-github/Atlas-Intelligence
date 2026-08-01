import json

import numpy as np
import plotly.graph_objects as go


def make_json_safe(value):
    """
    Recursively convert objects into JSON serializable forms.
    """

    if isinstance(value, np.ndarray):
        return [
            make_json_safe(item)
            for item in value.tolist()
        ]


    if isinstance(
        value,
        (
            np.integer,
            np.floating,
            np.bool_
        )
    ):
        return value.item()


    if isinstance(value, dict):

        return {
            key: make_json_safe(val)
            for key, val in value.items()
        }


    if isinstance(value, (list, tuple)):

        return [
            make_json_safe(item)
            for item in value
        ]


    return value



def normalize_trace(trace):

    trace = dict(trace)

    if "type" not in trace:
        trace["type"] = "scatter"

    if "mode" not in trace:
        trace["mode"] = "markers"

    return make_json_safe(trace)



def normalize_frame(frame):

    return {

        "data": [
            normalize_trace(trace)
            for trace in frame.get(
                "data",
                []
            )
        ],

        "name": frame.get(
            "name"
        )

    }



def normalize_animation(animation):

    """
    Convert supported animations into:

    {
        type,
        data,
        layout,
        frames
    }
    """


    if isinstance(animation, dict):

        if "frames" not in animation:
            raise ValueError(
                "Animation dictionary requires frames"
            )


        return {

            "type": "atlas",

            "data": make_json_safe(
                animation.get(
                    "data",
                    []
                )
            ),

            "layout": make_json_safe(
                animation.get(
                    "layout",
                    {}
                )
            ),

            "frames": [

                normalize_frame(frame)

                for frame in animation["frames"]

            ]

        }



    if isinstance(
        animation,
        go.Figure
    ):


        return {

            "type": "plotly",


            "data": [

                normalize_trace(
                    trace.to_plotly_json()
                )

                for trace in animation.data

            ],


            "layout": make_json_safe(
                animation.layout.to_plotly_json()
            ),


            "frames": [

                normalize_frame(
                    {
                        "data": [
                            trace.to_plotly_json()
                            for trace in frame.data
                        ],

                        "name": frame.name

                    }
                )

                for frame in animation.frames

            ]

        }


    raise TypeError(
        f"Unsupported animation type: {type(animation)}"
    )



def build_plotly_animation(data):

    fig = go.Figure(

        data=[
            normalize_trace(trace)
            for trace in data.get(
                "data",
                []
            )
        ],

        layout=data.get(
            "layout",
            {}
        )

    )


    fig.frames = [

        go.Frame(

            data=[
                normalize_trace(trace)
                for trace in frame.get(
                    "data",
                    []
                )
            ],

            name=frame.get(
                "name",
                str(i)
            )

        )

        for i, frame in enumerate(
            data.get(
                "frames",
                []
            )
        )

    ]


    return fig



def export_animations(simulation):

    for item in simulation.animations:

        animation = item["object"]
        name = item["name"]

        data = normalize_animation(
            animation
        )


        output = simulation.output


        (
            output / f"{name}.json"
        ).write_text(

            json.dumps(
                data,
                indent=2
            ),

            encoding="utf-8"

        )


        fig = build_plotly_animation(
            data
        )


        fig.write_html(
            output / f"{name}.html"
        )


        try:

            fig.write_image(
                output / f"{name}.png"
            )

            fig.write_image(
                output / f"{name}.svg"
            )


        except Exception as e:

            print(
                f"⚠ Could not export animation image: {e}"
            )


        print(
            f"✓ Exported animation: {name}"
        )