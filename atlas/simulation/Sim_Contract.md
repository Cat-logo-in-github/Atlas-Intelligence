# Atlas Simulation Contract v1

## 1. Your Role

You are **not writing a standalone Python program.**

A simulation is exactly one Python file named `simulation*.py`. Atlas imports this file as a module. It is not an executable program.

Your file is **one stage in a larger pipeline.**

You are responsible only for creating scientific objects.

Atlas is responsible for everything else.

---

# 2. The Pipeline

Every simulation executes in the following order.

```
run.py
│
│ imports simulation001.py
│
▼

build(simulation)

│
│ creates scientific objects
│
▼

simulation.figure(...)
simulation.graph(...)
simulation.data(...)
simulation.animation(...)
simulation.model(...)

│
│ registers objects
│
▼

build() returns

│
│
▼

run.py imports the next simulation

...

After ALL simulations finish:

simulation.export()

│
▼

Atlas exporters

│
├── figure exporter
├── graph exporter
├── animation exporter
├── dataset exporter
└── model exporter

│
▼

Browser-ready assets written to outputs/
```

**Your code ends when `build()` returns.**

Everything afterwards belongs to Atlas.

---

# 3. Golden Rule

A simulation never creates Atlas output files. Interactive models are the exception: they may create local model source files inside parent directory if required by simulation.model().

A simulation never exports.

A simulation never publishes.

A simulation only creates objects and registers them.

Registration looks like

```python
simulation.figure(obj, name)
```

This DOES NOT write a file.

It simply stores

```python
{
    "object": obj,
    "name": name
}
```

inside Atlas.

Later, Atlas exporters decide how to serialize that object.

Think of the simulation API as adding items to a queue.

---

# 4. What You Produce

You produce Python objects.

You do NOT produce files.

For example

```
You create:

Plotly Figure

↓

Atlas creates:

figure.html
figure.png
figure.svg


You create:

Matplotlib Figure

↓

Atlas creates:

figure.png
figure.svg
```

Likewise

```
You create:

DataFrame

↓

Atlas creates

results.csv
results.json
results.html
```

Likewise

```
You create

NetworkX graph

↓

Atlas creates

graph.html
graph.png
graph.svg
graph.json
```

Your responsibility ends at the Python object.

---

# 5. Required Entry Point

Every simulation MUST define

```python
def build(simulation):
    """
    Create scientific objects.
    Register them.
    Return None.
    """
```

build() may register zero or more objects.
build() must not call simulation.export().
build() should not rely on execution order relative to other simulations.
build() should return normally (or simply fall off the end).

Atlas calls this function.

Do not call it yourself.

---

# 6. Never Write Executable Code

Do NOT include

```python
if __name__ == "__main__":
```

Do NOT create

```python
Simulation()
```

Do NOT call

```python
simulation.export()
```

Do NOT call

```python
build(...)
```

Atlas performs all execution.

Note:
Do not execute expensive computations at module import time.
All simulation construction must occur inside build().

---

# 7. Registering Objects

The provided object exposes

```python
simulation.figure(obj, name)

simulation.graph(obj, name)

simulation.data(obj, name)

simulation.animation(obj, name)

simulation.model(path, name)
```

Calling these functions only registers objects.

Nothing is exported immediately.

---

# 8. Figure Contract

Register with

```python
simulation.figure(
    figure,
    "loss_curve"
)
```

Supported objects

* matplotlib.figure.Figure
* plotly.graph_objects.Figure

Do NOT call

```python
write_html()

write_image()

to_json()
```

Atlas does this.

---

# 9. Graph Contract

Register

```python
simulation.graph(
    graph,
    "network"
)
```

Supported

NetworkX Graph objects
(including DiGraph, MultiGraph, MultiDiGraph)

or

```python
{
    "nodes":[...],
    "edges":[...]
}
```

Do not render layouts.

Do not export HTML.

Atlas converts graphs into Plotly visualizations. x,y co-ordinates as metadata are appreciated. So are more metadata properties:
Eg: 
```python
graph.add_node(
    "Visual Cortex",
    x=5,
    y=2,
    color="#ef4444",
    size=30,
    label="V1",
    type="occipital cortex"
)

graph.add_edge(
    "LGN",
    "Visual Cortex",
    label="optic radiation"
)
```
---

# 10. Data Contract

Register

```python
simulation.data(
    dataframe,
    "results"
)
```

Supported

* pandas DataFrame
* numpy ndarray
* dictionary
* list of dictionaries

Do not write CSV.

Do not write HTML tables.

Atlas converts datasets.

---

# 11. Animation Contract

Register

```python
simulation.animation(
    animation,
    "training"
)
```

Supported:

- Plotly Figure containing frames
- Atlas animation dictionary

A normal static Plotly Figure belongs in simulation.figure(), not simulation.animation().

Do not export animation HTML.

Atlas animation dictionaries must contain:

{
    "frames": [
        {
            "data": [
                Plotly trace dictionaries
            ]
        }
    ]
}

Atlas creates the browser player.

---

# 12. Interactive Model Contract

Register

```python
simulation.model(
    "gravity_sim",
    "gravity"
)
```

simulation.model(path, name) expects path to refer to a directory relative to the current simulation file unless it is an absolute path.

The supplied path must contain:

index.html

Additional files such as:

main.js
assets/

are allowed but not required.

Do not copy directories.

Atlas copies the model.

## Model Asset Generation

A simulation may create local model source files/directories required by simulation.model(). This is an exception to the normal flow as it requires path argument.

Rules:
- Files must be created inside the simulation directory.
- Files must not be created inside outputs/.
- The simulation must create the complete model directory before calling simulation.model().
- The registered directory must contain index.html.
- Single-file HTML models are encouraged.
- JavaScript may be embedded inside <script> tags.
- External CDN libraries are allowed.
- Additional local files (JS, CSS, assets) are allowed if generated by the simulation.
- Atlas does not run build systems. npm, webpack, vite, and compilation steps are not available unless explicitly supported.
- Atlas only copies the finished model directory.
---

# 13. Allowed Libraries

Libraries for creating objects (they exist in environment):

requests → fetch public APIs/data sources
pandas → clean/tabulate data
numpy → numerical processing
scipy → statistics, optimization, correlations, interpolation
sympy → symbolic math
matplotlib / plotly → create figures
networkx → graph structures
beautifulsoup4 → scrape HTML if appropriate
json / csv (Python standard library) → parse data

NOTE:
Directly supported output objects can only be:

- plotly.graph_objects.Figure → simulation.figure()
- matplotlib.figure.Figure → simulation.figure()
- networkx.Graph → simulation.graph()
- pandas.DataFrame → simulation.data()
- numpy.ndarray → simulation.data()

Only Atlas-supported objects may be registered.
plotly.graph_objects animation frames are supported.

---
# 13b. Exporters validate types

For example:

simulation.figure() expects an actual Plotly or Matplotlib figure object.
simulation.graph() expects a NetworkX graph or Atlas graph dictionary.
simulation.data() expects a DataFrame, ndarray, dict, or list.
simulation.animation() expects a Plotly animation or Atlas animation dictionary.
simulation.model() receives a filesystem path to a directory, not a model object. The path must exist when build() executes. The directory must contain index.html at least.

Not "something equivalent." The actual object.

Do not wrap the entire simulation in try/except just to suppress errors. If object construction fails, allow the exception to propagate so Atlas can report it.

The simulation no longer owns the object. Atlas may serialize it later. Do not mutate registered objects after registration.

---

# 13c. Do not create adapters

Only register objects supported by the contracts.

Do not convert objects into custom wrappers, HTML strings, dictionaries, or files unless the contract explicitly requires that format.

The exporter receives the object directly.
Eg:
simulation.figure(
    {
        "x": x,
        "y": y
    },
    "plot"
) is bad because figure() expects an actual Plotly/Matplotlib figure
---

# 14. Forbidden Operations

Never do any of the following.

Filesystem

Never create Atlas output assets for non model simulations.

Forbidden:

- writing to outputs/
- creating output folders
- copying model folders
- exporting HTML/PNG/SVG/JSON/CSV files
- Do not create a class named Simulations

Temporary files are allowed only when required for computation.

Rules:

- temporary files must live inside the simulation folder
- temporary files must be deleted before build() returns
- model asset files created for simulation.model() are not temporary and must remain.
- registered objects must be in-memory Atlas-supported objects


# 15. Naming Rules

Names must

* be unique
* contain only

```
letters

numbers

underscores
```

Good

```
loss_curve

temperature

network

experiment1
```

Bad

```
Loss_Curve

loss curve

loss-curve

graph(1)
```

Names become filenames.

Example:

simulation.figure(fig, "loss_curve")

creates files beginning with:

loss_curve

Therefore names must be valid filenames.

---

# 16. Mental Model

Always think of your code as doing this

```
Create object

↓

Register object

↓

Return

↓

STOP
```

Not this

```
Create object

↓

Export HTML

↓

Export PNG

↓

Write files

↓

Package outputs
```

The second pipeline belongs entirely to Atlas.

---
# 17. Choosing the Correct Output Type

Choose the Atlas API based on what the user wants to visualize, not the word they use.

## simulation.figure()

Use for scientific plots and mathematical visualizations.

Examples:
- mathematical functions
- statistical charts
- heatmaps
- trajectories
- phase diagrams
- scientific illustrations
- annotated images
- experimental results

A mathematical "graph" is a figure. A good background image is expected for heatmaps/overlays (public assets).

---

## simulation.graph()

Use for node-edge structures.

Examples:
- networks
- pathways
- knowledge graphs
- dependency graphs
- neural/social/transport networks
- molecular interaction diagrams
- state machines
- trees

Names must be readable and font size should accomodate. Overlapping node names are not good. Make sure x,y coordinates if specified do not cluster the graph.
---

## simulation.data()

Use for structured values.

Examples:
- tables
- measurements
- datasets
- time series
- lists

---

## simulation.animation()

Use when the output changes over time.

Examples:
- particle motion
- optimization steps
- evolving systems
- training progress
- physics engines
- agent simualtions
- signal propagation

---

## simulation.model()

Use for complete browser applications. All files need to be made in same script.

Examples:
- Three.js
- WebGL
- custom JavaScript simulations

---

Decision rule:

- Visual relationship → `figure`
- Connected entities → `graph`
- Values/tables → `data`
- Time evolution → `animation`
- Full interactive application → `model`

---
# 18. Simulation Reliability

A simulation must be deterministic and self-contained.

Avoid:
- infinite loops
- extremely large allocations
- long-running downloads
- interactive input()
- dependence on unavailable services

External data sources must:
- have reasonable timeouts
- handle missing data gracefully
- produce valid Atlas-supported objects

The simulation must always either:
- register valid objects and return
- raise a meaningful exception

---
# Import Behavior

This file is never executed directly.

It is imported by run.py.

run.py calls:

build(simulation)

Therefore:

- define build()
- create objects inside build()
- register objects
- return

Do not write executable startup code.

Before finishing, verify:

✓ build(simulation) exists

✓ no Simulation()

✓ no simulation.export()

✓ no write_html() unless it is registering a model

✓ no write_image()

✓ no savefig()

✓ no __main__

✓ every created object is registered

✓ all names are unique