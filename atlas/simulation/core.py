from pathlib import Path

import matplotlib.figure
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from atlas.simulation.exporters import (
    export_figures,
    export_graphs,
    export_animations,
    export_datasets,
    export_models,
)

from pathlib import Path
from typing import Optional

class Simulation:

    def __init__(
        self,
        output: Optional[Path] = None
    ):
        self.output = output

        self.current_file = None

        self.figures = []
        self.graphs = []
        self.animations = []
        self.datasets = []
        self.models = []


    def set_context(
        self,
        file: Path
    ):

        self.current_file = file


    def resolve_path(
        self,
        path
    ):

        path = Path(path)

        if path.is_absolute():
            return path

        if self.current_file:
            return self.current_file.parent / path

        return path


    def validate_name(
        self,
        name: str
    ):

        if not isinstance(name, str):

            raise TypeError(
                "Name must be a string"
            )


        if not name:

            raise ValueError(
                "Name cannot be empty"
            )


        if not name.replace("_", "").isalnum():

            raise ValueError(
                f"Invalid name '{name}'. "
                "Only letters, numbers, and underscores allowed."
            )


    def name_exists(
        self,
        name: str
    ):

        collections = (
            self.figures,
            self.graphs,
            self.animations,
            self.datasets,
            self.models,
        )


        return any(
            item["name"] == name
            for collection in collections
            for item in collection
        )


    def validate_unique_name(
        self,
        name: str
    ):

        if self.name_exists(name):

            raise ValueError(
                f"Duplicate simulation name: '{name}'"
            )


    def validate_registration_name(
        self,
        name: str
    ):

        self.validate_name(name)

        self.validate_unique_name(name)


    def figure(
        self,
        figure,
        name: str
    ):

        self.validate_registration_name(name)


        if not isinstance(
            figure,
            (
                matplotlib.figure.Figure,
                go.Figure
            )
        ):

            raise TypeError(
                "simulation.figure expects "
                "matplotlib.figure.Figure or "
                "plotly.graph_objects.Figure"
            )


        self.figures.append(
            {
                "object": figure,
                "name": name
            }
        )


    def graph(
        self,
        graph,
        name: str
    ):

        self.validate_registration_name(name)


        if not isinstance(
            graph,
            (
                nx.Graph,
                dict
            )
        ):

            raise TypeError(
                "simulation.graph expects "
                "NetworkX graph or dictionary"
            )


        self.graphs.append(
            {
                "object": graph,
                "name": name
            }
        )


    def animation(
        self,
        animation,
        name: str
    ):

        self.validate_registration_name(name)


        if not isinstance(
            animation,
            (
                go.Figure,
                dict
            )
        ):

            raise TypeError(
                "simulation.animation expects "
                "Plotly Figure or Atlas animation dictionary"
            )


        self.animations.append(
            {
                "object": animation,
                "name": name
            }
        )


    def data(
        self,
        data,
        name: str
    ):

        self.validate_registration_name(name)


        if not isinstance(
            data,
            (
                pd.DataFrame,
                np.ndarray,
                dict,
                list
            )
        ):

            raise TypeError(
                "simulation.data expects "
                "DataFrame, ndarray, dictionary, or list"
            )


        self.datasets.append(
            {
                "object": data,
                "name": name
            }
        )


    def model(
        self,
        model,
        name: str
    ):

        self.validate_registration_name(name)


        model = self.resolve_path(model)


        if not isinstance(
            model,
            Path
        ):

            raise TypeError(
                "simulation.model expects a filesystem path"
            )


        if not model.exists():

            raise FileNotFoundError(
                f"Model directory does not exist: {model}"
            )


        if not model.is_dir():

            raise TypeError(
                "Model path must be a directory"
            )


        if not (model / "index.html").exists():

            raise FileNotFoundError(
                f"Model requires index.html: {model}"
            )


        self.models.append(
            {
                "object": model,
                "name": name
            }
        )

    def preview(self):

        export_figures(
            self,
            export=False
        )

        export_graphs(
            self,
            export=False
        )

        export_animations(
            self,
            export=False
        )

        export_datasets(
            self,
            export=False
        )

        export_models(
            self,
            export=False
        )


    def export(self):

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        export_figures(self)

        export_graphs(self)

        export_animations(self)

        export_datasets(self)

        export_models(self)