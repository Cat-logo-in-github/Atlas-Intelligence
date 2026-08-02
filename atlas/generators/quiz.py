import typer

from atlas.models.module import Module
from atlas.utils.paths import MODULES_DIR
from atlas.llm.ollama import generate
from atlas.validators.module import mark_output_published


def generate_quiz(
    slug: str,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing quiz.md",
    ),
):

    module_path = MODULES_DIR / slug


    if not module_path.exists():

        raise typer.Exit(
            f"Unknown module: {slug}"
        )


    module = Module(module_path)


    destination = (
        module.generated
        /
        "quiz.md"
    )


    if destination.exists() and not force:

        print(
            f" O {module.title}/quiz.md exists"
        )

        return



    knowledge = ""


    if module.knowledge.exists():

        knowledge = module.knowledge.read_text(
            encoding="utf-8"
        )


    if not knowledge.strip():

        print(
            f" ! No knowledge.md found for {module.title}"
        )

        return



    print(
        f" ▶ Generating quiz: {module.title}"
    )



    prompt = f"""
You are creating an educational quiz.

Create a short quiz from the knowledge notes below.

Topic:
{module.title}


Knowledge:
-----------
{knowledge}


Requirements:

- Create 5 to 7 questions.
- Test understanding, not memorization.
- Mix conceptual and technical questions.
- Start easy and gradually increase difficulty.
- Include the answer after each question.
- Keep explanations short.
- Use Markdown formatting.


Format:

# Quiz: <topic>


## Question 1

Question text

**Answer:**

Answer text

**Explanation:**

Short explanation

Rules:
- 1 question 1 answer. 
- No multiple choice questions/Fill in the blanks. 
- Short 1 line answers
- Conscise explanations referencing 'Knowledge'

Repeat for all questions.
"""



    result = generate(
        prompt
    )


    content = f"""# {module.title}

{result}
"""


    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    destination.write_text(
        content,
        encoding="utf-8"
    )


    print(
        f" ✓ Generated {destination}"
    )

    mark_output_published(
        module,
        "quiz"
    )