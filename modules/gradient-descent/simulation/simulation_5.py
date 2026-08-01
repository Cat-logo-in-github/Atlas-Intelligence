import numpy as np
import plotly.graph_objects as go


def build(simulation):
    x = np.linspace(-5, 5, 400)
    y = x**2 + 5

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="f(x)=x^2+5",
            line=dict(color="blue")
        )
    )

    start_x = -4.5
    steps = [start_x]
    learning_rate = 0.08

    current = start_x
    for _ in range(25):
        current = current - learning_rate * (2 * current)
        steps.append(current)

    frames = []
    for i, point in enumerate(steps):
        path_x = steps[: i + 1]
        path_y = [v**2 + 5 for v in path_x]

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=[point],
                        y=[point**2 + 5],
                        mode="markers",
                        marker=dict(size=12, color="red"),
                        name="current point"
                    ),
                    go.Scatter(
                        x=path_x,
                        y=path_y,
                        mode="lines+markers",
                        line=dict(color="orange"),
                        name="gradient descent path"
                    ),
                ],
                name=str(i)
            )
        )

    fig.frames = frames

    fig.add_trace(
        go.Scatter(
            x=[start_x],
            y=[start_x**2 + 5],
            mode="markers",
            marker=dict(size=12, color="red"),
            name="start"
        )
    )

    fig.update_layout(
        title="Function Graph with Gradient Descent",
        xaxis_title="x",
        yaxis_title="f(x)",
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Run Gradient Descent",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 250, "redraw": True},
                                "fromcurrent": True
                            }
                        ],
                    }
                ],
            }
        ],
    )

    gradient = 2 * x

    gradient_fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=gradient,
                mode="lines",
                name="f'(x)=2x",
                line=dict(color="green")
            )
        ]
    )

    gradient_fig.update_layout(
        title="Gradient Function",
        xaxis_title="x",
        yaxis_title="gradient"
    )

    simulation.figure(fig, "function_gradient_descent")
    simulation.figure(gradient_fig, "gradient_function")