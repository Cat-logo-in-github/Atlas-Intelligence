import numpy as np
import plotly.graph_objects as go


def build(simulation):
    x = np.linspace(-5, 5, 300)

    # Uneven loss landscape (height represents loss)
    y = (
        0.08 * (x + 1.5) ** 2
        + 0.35 * np.sin(1.8 * x)
        + 0.12 * np.sin(4.5 * x)
    )

    # Start ball in a right-side crevace
    positions = np.linspace(3.7, 0.2, 35)

    frames = []

    for i, px in enumerate(positions):
        py = np.interp(px, x, y) + 0.22

        # Gradient direction approximation
        dx = 0.25
        slope_right = np.interp(px + dx, x, y)
        slope_left = np.interp(px - dx, x, y)
        gradient = (slope_right - slope_left) / (2 * dx)

        arrow_length = -0.8 * np.sign(gradient)
        if abs(gradient) < 0.02:
            arrow_length = -0.25

        arrow_x = [px, px + arrow_length]
        arrow_y = [py + 0.7, py + 0.7]

        frame_data = [
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line=dict(color="royalblue", width=4),
                name="Loss landscape",
            ),
            go.Scatter(
                x=[px],
                y=[py],
                mode="markers",
                marker=dict(size=22, color="crimson"),
                name="Ball",
            ),
            go.Scatter(
                x=arrow_x,
                y=arrow_y,
                mode="lines+markers",
                line=dict(color="darkorange", width=5),
                marker=dict(size=8, symbol="arrow"),
                name="Force nudge",
            ),
        ]

        frames.append(
            go.Frame(
                data=frame_data,
                name=f"step_{i}",
            )
        )

    fig = go.Figure(
        data=frames[0].data,
        frames=frames,
    )

    fig.update_layout(
        title="Gradient Descent: Ball Rolling Down the Loss Landscape",
        xaxis_title="Parameter",
        yaxis_title="Loss (Height)",
        showlegend=True,
        template="plotly_white",
        xaxis=dict(range=[-5, 5]),
        yaxis=dict(range=[min(y) - 0.5, max(y) + 1.2]),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Start Gradient Descent",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 120, "redraw": True},
                                "transition": {"duration": 0},
                            },
                        ],
                    }
                ],
            }
        ],
    )

    simulation.animation(fig, "gradient_descent_loss")