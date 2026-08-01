import matplotlib.pyplot as plt


def build(simulation):

    fig, ax = plt.subplots()

    ax.plot(
        [0, 1, 2],
        [0, 1, 4]
    )

    simulation.figure(
        fig,
        name="parabola"
    )