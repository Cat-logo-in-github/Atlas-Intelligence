> A simulation author creates a scientific object. Atlas guarantees a browser-ready artifact with a predictable quality standard.

So we should lock the contracts now.

I would define the `Simulation` API like this:

---

# Atlas Simulation Contracts v0.1

## 1. Figure Contract

Purpose:

* Scientific plots
* Mathematical visualizations
* Experimental results

Input:

```python
simulation.figure(
    figure,
    name="loss_curve"
)
```

Accepted objects:

* `matplotlib.figure.Figure`
* `plotly.graph_objects.Figure`

Export:

```
outputs/
│
├── loss_curve.png
├── loss_curve.svg
├── loss_curve.html
└── loss_curve.json
```

Rules:

### PNG

Static high-resolution render.

### SVG

Vector output where supported.

### HTML

Interactive version.

For Plotly:

* native interactive HTML
* hover
* zoom
* sliders
* dropdowns

For matplotlib:

* static HTML wrapper or conversion layer

The exporter should preserve interactive controls where the library supports them.

---

# 2. Graph Contract

Purpose:

* Networks
* Trees
* State diagrams
* Knowledge graphs

Input:

```python
simulation.graph(
    graph,
    name="neural_network"
)
```

Accepted:

* NetworkX graphs
* graph dictionaries
* edge/node structures

Example:

```python
{
    "nodes": [
        {"id": "A"},
        {"id": "B"}
    ],
    "edges": [
        {"source":"A","target":"B"}
    ]
}
```

Export:

```
outputs/

neural_network.png
neural_network.svg
neural_network.json
neural_network.html
```
Static image export depends on Plotly image export support.

HTML:

* zoom
* pan
* hover nodes
* inspect edges

Possible backends:

* Plotly
* Cytoscape.js
* D3.js

---

# 3. Data Contract

Purpose:

* Tables
* Measurements
* Simulation output
* Time series

Input:

```python
simulation.data(
    data,
    name="temperature"
)
```

Accepted:

* pandas DataFrame
* numpy arrays
* dictionaries
* list of records

Example:

```python
{
    "time":[0,1,2],
    "temperature":[20,21,23]
}
```

Export:

```
outputs/

temperature.json
temperature.html
temperature.csv
```

HTML:

* sortable table
* searchable
* pagination

Possible backend:

* DataTables
* native HTML tables

---

# 4. Animation Contract

Purpose:

* Time-dependent systems
* Physics
* Training curves
* Evolution processes

Input:

```python
simulation.animation(
    animation,
    name="particle_motion"
)
```

Accepted:

* matplotlib Animation
* Plotly frames
* custom frame sequence

Export:

```
outputs/

particle_motion.html
particle_motion.json
```

HTML requirements:

Must support:

* play/pause
* timeline slider
* frame stepping

Example:

```
[◀] [▶] --------●-----
Frame 45/200
```

---

# 5. Interactive Model Contract

This is the important one.

Atlas does **not** understand arbitrary physics.

Instead:

```python
simulation.model(
    model,
    name="gravity_sim"
)
```

means:

"This object provides a browser runtime."

Contract:

```
model/

├── index.html
├── main.js
├── assets/
└── metadata.json
```

Example:

Three.js:

```
gravity_sim/

index.html
main.js
three.min.js
textures/
```

Atlas packages:

```
outputs/

gravity_sim.html
gravity_sim/
    main.js
    assets/
```

The browser runs the simulation.

Atlas is the publisher, not the physics engine.

---

# The Simulation API becomes:

```python
class Simulation:

    def figure(self, obj, name):
        ...

    def graph(self, obj, name):
        ...

    def data(self, obj, name):
        ...

    def animation(self, obj, name):
        ...

    def model(self, obj, name):
        ...
```

The exporter layer owns:

```
simulation.py
        |
        |
        v

registered objects

        |
        |
        v

exporters/

figure.py
graph.py
data.py
animation.py
model.py
```

---

This gives you a clean mental model:

A researcher writes:

```python
def build(simulation):

    simulation.figure(
        make_gradient_plot(),
        "gradient_descent"
    )

    simulation.animation(
        make_training_animation(),
        "training"
    )
```

They never think about:

* HTML
* SVG
* PNG
* browser embedding
* output folders
* file naming
* website integration

Atlas handles the publication pipeline.