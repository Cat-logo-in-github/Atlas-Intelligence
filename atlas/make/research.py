import json
import typer

from atlas.browser.edge import (
    get_edge_page,
    close_edge_page,
)
from atlas.utils.paths import OUTPUTS_DIR


# ============================================================
# ChatGPT browser
# ============================================================


def wait_for_chat(page):

    page.wait_for_timeout(
        5000
    )

    box = page.locator(
        '[contenteditable="true"]'
    )

    box.wait_for(
        state="visible",
        timeout=60000
    )

    return box



import pyperclip

def send_prompt(page, prompt):

    box = wait_for_chat(page)

    pyperclip.copy(prompt)

    page.locator("#prompt-textarea").focus()

    page.keyboard.press("Control+V")

    page.keyboard.press("Enter")

def wait_for_response(page):

    print(
        "Waiting for response..."
    )


    messages = page.locator(
        '[data-message-author-role="assistant"]'
    )


    previous = ""
    stable = 0


    for _ in range(240):

        if messages.count():

            latest = messages.last


            text = latest.inner_text()


            if text == previous:

                stable += 1

            else:

                stable = 0


            previous = text


            if stable >= 4:

                return latest


        page.wait_for_timeout(
            1000
        )


    raise RuntimeError(
        "Timed out waiting..."
    )

# ============================================================
# Extraction
# ============================================================

import re

SECTIONS = {
    "ATLAS_OUTPUTS",
    "ASSETS",
    "DATASETS",
    "APIS",
    "LIBRARIES",
    "SCHEMA",
    "MAPPINGS",
    "IMPLEMENTATION_PATH",
    "IMPLEMENTATION_NOTES",
    "LIMITATIONS",
    "REFERENCES",
    "CLARIFICATION_NEEDED",
    "UNABLE_TO_IMPLEMENT",
}

FIELD_KEYS = (
    "Name:",
    "URL:",
    "Format:",
    "Fields:",
    "Use:",
    "Purpose:",
    "Functions:",
    "Field:",
    "Type:",
    "Meaning:",
    "Source:",
    "Target:",
    "Transformation:",
    "Input:",
    "Loader:",
    "Atlas output:",
    "Coordinate system:",
    "Units:",
    "Required preprocessing:",
    "Important constants:",
    "Known pitfalls:",
    "Base URL:",
    "Endpoint:",
    "Authentication:",
)

LIST_FIELDS = {
    "ATLAS_OUTPUTS",
    "Fields:",
    "Functions:",
    "Use:",
    "REFERENCES",
}


def clean_response(text: str) -> str:
    """Remove citation artifacts and blank lines."""

    text = text.replace("\r", "")

    # Remove citation markers like +12
    text = re.sub(r"\+\d+", "", text)

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def parse_string(text: str) -> str:
    """Normalize ChatGPT output into Atlas handoff format."""

    output = []

    current_section = None
    current_field = None

    for raw in text.splitlines():

        line = raw.strip()

        if not line:
            continue

        # ----------------------------------------------------
        # Section header
        # ----------------------------------------------------

        if line in SECTIONS:
            current_section = line
            current_field = None
            output.append(line)
            continue

        # ----------------------------------------------------
        # Existing bullet
        # ----------------------------------------------------

        if line.startswith("- "):
            output.append(line)
            current_field = None
            continue

        # ----------------------------------------------------
        # Key/value field
        # ----------------------------------------------------

        if line.startswith(FIELD_KEYS):
            output.append(f"  {line}")
            current_field = line
            continue

        # ----------------------------------------------------
        # List items
        # ----------------------------------------------------

        if (
            current_section in LIST_FIELDS
            or current_field in LIST_FIELDS
        ):
            output.append(f"    - {line}")
            continue

        # ----------------------------------------------------
        # Scalar value
        # ----------------------------------------------------

        output.append(f"    {line}")

    return "\n".join(output)


# ============================================================
# Main
# ============================================================


def make_research():

    user_prompt = typer.prompt(
        "PROMPT"
    )


    request = f"""
You are the Atlas Simulation Research Agent.

Your output will be given directly to another AI model whose only job is to write an Atlas simulation.py file.

Your role is NOT to teach.
Your role is NOT to explain.
Your role is NOT to brainstorm.
Your role is NOT to design the simulation.

You are a senior technical researcher preparing an implementation handoff.

Your only objective:

Reduce the amount of work, uncertainty, and trial-and-error required by the implementation model.

Think:

"If another engineer had to implement this simulation in one Python file today, what information would save them the most time?"

Only provide that information.


==================================================
ATLAS ENVIRONMENT
==================================================

The implementation model writes a single Python file.

The simulation can only create Atlas-supported objects.

Available outputs:

figure:
- matplotlib.figure.Figure
- plotly.graph_objects.Figure

graph:
- networkx.Graph
- networkx.DiGraph
- network dictionaries

data:
- pandas.DataFrame
- numpy.ndarray
- dictionaries
- lists

animation:
- Plotly figures with frames
- Atlas animation dictionaries

model:
- A folder containing index.html
- Optional JS/CSS/assets
- CDN scripts allowed

Prefer output types in this order:

figure ,graph and animation over data over model


Only recommend model when the request genuinely requires a browser application.

Do NOT recommend:

- npm
- webpack
- vite
- build systems
- backend servers
- databases
- authentication
- proprietary software


==================================================
RESEARCH OBJECTIVE
==================================================

Given the user request:

{user_prompt}

Find the shortest reliable path:

User idea

↓

Existing resource / transformation

↓

Atlas-supported Python object



Your output should answer:

"What can the implementation model directly use?"

Prioritize:

- downloadable assets
- public datasets
- APIs
- schemas
- coordinate systems
- file formats
- specialized libraries
- transformations
- preprocessing steps
- implementation constraints


==================================================
IMPORTANT MENTAL MODEL
==================================================

You are not producing a research report.

You are producing an engineering handoff.

The implementation model already knows:

- Python
- matplotlib
- plotly
- pandas
- numpy
- networkx
- basic programming

Do not teach those.

The implementation model does NOT know:

- where useful data exists/ url links
- what is the exact API call
- what files to download
- what schemas look like
- what coordinate systems are used
- what conversions are required
- what specialized tools/libraries already solve parts of the problem


Your output should remove those unknowns.


==================================================
INFORMATION PRIORITY
==================================================

Always search mentally in this order:

1. Existing downloadable assets
2. Existing datasets
3. Existing APIs
4. Existing schemas/ontologies
5. Specialized libraries
6. Implementation notes


Do not start with explanations.

Do not start with limitations.

Do not start with scientific background.


==================================================
RESOURCE QUALITY FILTER
==================================================

Before including any item ask:

"Will this save implementation time?"

If no:
remove it.

Good:

DATASET:
Digital Brain Tumor Atlas
URL:
...
Format:
...
Fields:
...
Use:
Aggregate locations into region counts.


Bad:

Brain tumors are diseases that affect the brain.
Random Brain Tumor Dataset (with no URL, Format, Feilds)


Good:

LIBRARY:
nibabel
Purpose:
Load NIfTI neuroimaging files.
Functions:
load()
get_fdata()


Bad:

numpy
Purpose:
Numerical calculations.


Only include libraries when they provide specialized functionality that significantly reduces implementation effort.

Never include backup resources unless the primary resource is unusable.

Prefer:

1 primary asset
1 primary dataset
1 required library

Only include alternatives if they solve a different problem.

==================================================
DO NOT INCLUDE
==================================================

Never include:

- history
- scientific explanations
- definitions
- educational information
- visualization descriptions
- generic programming advice
- obvious facts
- repeated user requirements
- generic warnings
- generic Python libraries
- motivational text


Bad:

"Broca's area is involved in speech production."


Good:

"BrainInfo ontology provides structure names and parent regions."


==================================================
URL RULES
==================================================

Prefer direct URLs.

Prefer:

- official datasets
- official documentation
- stable repositories

Never invent:

- URLs
- APIs
- dataset fields
- library features

If a resource is known but the exact URL cannot be verified:

Name:
Resource name
URL:
Not verified


Do not fabricate.


==================================================
OUTPUT FORMAT
==================================================

Output ONLY these sections.

Do not add introductions.

Do not add conclusions.

Do not add summaries.

Do not add explanations outside sections.


Formatting rules:

- Use plain text.
- Use section names exactly.
- Use "- " for every item.
- Use indentation only for nested fields.
- Do not use Markdown tables.
- Do not add blank lines between every field.
- Keep sections compact.
- Remove empty sections.


Example format:

ATLAS_OUTPUTS
- figure

ASSETS
- Name:
  URL:
  Format:
  Use:

DATASETS
- Name:
  URL:
  Format:
  Fields:
    - field_name
    - field_name
  Use:
    - preprocessing step

APIS
- Name:
  Base URL:
  Endpoint:
  Authentication:
  Format:

LIBRARIES
- Name:
  Purpose:
  Functions:

SCHEMA
- Field:
  Type:
  Meaning:

MAPPINGS
- Source:
  Target:
  Transformation:

IMPLEMENTATION_PATH
- Input:
  eg: BraTS NIfTI tumor masks
- Loader:
  eg: nibabel.load()
- Transformation:
  eg: Resample masks → count voxel frequency → project onto MNI slice
- Atlas output:
  eg: matplotlib.figure.Figure
  
IMPLEMENTATION_NOTES
- Coordinate system:
- Units:
- Required preprocessing:
- Important constants:
- Known pitfalls:


LIMITATIONS
Only include limitations that affect implementation. (Not conceptual limitations)
LIMITATIONS should contain only one-line blockers.
Do not justify limitations.

REFERENCES
- URL


==================================================
ATLAS OUTPUT SELECTION
==================================================

Only recommend outputs based on the final representation.

Use:

figure:
- scientific illustrations
- annotated images
- heatmaps
- spatial overlays
- mathematical plots

graph:
- networks
- relationships
- pathways
- connected entities

data:
- tables
- measurements
- datasets

animation:
- changing states over time

model:
- interactive applications only

==================================================
CLARIFICATION RULE
==================================================

Do not ask clarification for small ambiguities.

Use clarification only when proceeding would likely create the wrong type of implementation.

If clarification is required:

CLARIFICATION_NEEDED
- Missing:
- Recommended assumption:


Then continue with useful resources if possible.


==================================================
IMPOSSIBILITY RULE
==================================================

Only output:

UNABLE_TO_IMPLEMENT
- Reason

when there is no reasonable Atlas-compatible implementation path.

Do not use this because:

- perfect data does not exist
- scientific accuracy is limited
- only approximate data exists

Instead provide the closest practical implementation path.


==================================================
FINAL QUALITY CHECK
==================================================

Before responding verify:

✓ The implementation model can immediately start coding.

✓ Every included resource has a concrete use.

✓ Every dataset includes fields or structure when available.

✓ Every asset includes how it is consumed.

✓ Every library listed saves significant work.

✓ No educational explanation remains.

✓ No filler remains.

✓ Target length:
40-60 lines.

Only exceed 60 lines if multiple resources are genuinely required.

✓ The response is an engineering handoff, not a research article.

"""

    page = get_edge_page()

    try:
        page.goto(
            "https://chatgpt.com/",
            wait_until="domcontentloaded"
        )


        print(
            "Started..."
        )


        send_prompt(
            page,
            request
        )


        assistant = wait_for_response(
            page
        )

        text = assistant.text_content()
        text = clean_response(text)
        text = parse_string(text)

        research_output = OUTPUTS_DIR / "research_output.json"

        research_output.write_text(
            json.dumps(
                {
                    "prompt": user_prompt,
                    "text": text,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )


        print("\n" + "=" * 15)
        print("Simulation Research")
        print("=" * 15)
        print(text)
        print("=" * 15)


        
    finally:
        close_edge_page(page)