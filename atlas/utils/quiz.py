def append_quiz(module):

    quiz = module.generated / "quiz.md"

    if not quiz.exists():
        return


    knowledge = module.knowledge


    quiz_text = quiz.read_text(
        encoding="utf-8"
    ).strip()


    knowledge_text = knowledge.read_text(
        encoding="utf-8"
    ).rstrip()


    # Prevent accidental duplicate appends
    if "## Quiz" in knowledge_text:
        return


    with knowledge.open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write("\n\n")
        f.write("## Quiz\n\n")
        f.write(quiz_text)
        f.write("\n")