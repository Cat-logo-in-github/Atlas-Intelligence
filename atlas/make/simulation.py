from pathlib import Path
import ast
import json
import typer

from atlas.browser.edge import (
    get_edge_page,
    close_edge_page,
)
from atlas.utils.paths import MODULES_DIR
from atlas.utils.paths import OUTPUTS_DIR

# ============================================================
# Contract
# ============================================================

CONTRACT_PATH = (
    Path(__file__).parent.parent
    / "simulation"
    / "Sim_Contract.md"
)


def load_contract():

    if not CONTRACT_PATH.exists():

        raise FileNotFoundError(
            CONTRACT_PATH
        )


    return CONTRACT_PATH.read_text(
        encoding="utf-8"
    )

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

    print("wait")
    box = wait_for_chat(page)

    pyperclip.copy(prompt)

    page.locator("#prompt-textarea").focus()

    page.keyboard.press("Control+V")

    page.keyboard.press("Enter")

    
def wait_for_response(page):

    print(
        "Waiting for Simulation..."
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


def extract_python_blocks(
    assistant
):

    blocks = assistant.locator(
        "pre code"
    )


    results = []


    for i in range(blocks.count()):

        code = blocks.nth(i).inner_text()


        results.append(
            code
        )


    return results



def validate_python(
    code
):

    try:

        ast.parse(
            code
        )

    except SyntaxError as e:

        print(
            "Syntax error:"
        )

        print(e)

        return False


    if "def build(" not in code:

        print(
            "Missing build(simulation)"
        )

        return False


    return True



# ============================================================
# Files
# ============================================================


def next_filename(
    folder: Path
):

    existing = list(
        folder.glob(
            "simulation*.py"
        )
    )


    if not existing:

        return (
            folder /
            "simulation.py"
        )


    return (
        folder /
        f"simulation_{len(existing)}.py"
    )



# ============================================================
# Main
# ============================================================


def make_simulation(
    module_name: str,
    research: bool = False,
):

    user_prompt = typer.prompt(
        "PROMPT"
    )


    contract = load_contract()


    request = f"""
You are generating an Atlas simulation.

Read and follow the complete contract below.

CONTRACT:
----------------

{contract}

----------------
"""
    if research:
        data = json.loads(
            (OUTPUTS_DIR / "research_output.json").read_text(
                encoding="utf-8"
            )
        )

        request += f"""

Research Handoff:
----------------

{data["text"]}

Use the research handoff above as the implementation plan.
Do not replace it with new research.
Do not question the selected resources unless they are impossible to use.
Translate the handoff into Atlas-compatible Python code.
----------------
"""
        request += f"""

User request:

{user_prompt}

Output requirements:

- Output ONLY one python code block.
- No explanation.
- No markdown outside the code block.
- The code must implement the contract.
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


        blocks = extract_python_blocks(
            assistant
        )


        print(
            f"Found {len(blocks)} code blocks."
        )


        if len(blocks) != 1:

            input(
                "Unexpected number of code blocks. Review ChatGPT response, then ENTER..."
            )

            return



        code = blocks[0].strip()


        if not validate_python(
            code
        ):

            input(
                "Validation failed. Review response, then ENTER..."
            )

            return



        simulations = (
            MODULES_DIR
            /
            module_name
            /
            "simulation"
        )


        simulations.mkdir(
            exist_ok=True
        )


        output = next_filename(
            simulations
        )


        output.write_text(
            code,
            encoding="utf-8"
        )


        print(
            "\nSaved simulation:"
        )

        print(
            output
        )
    finally:
        close_edge_page(page)