def mock_response(message: str) -> str:

    message = message.lower()

    if (
        "summarize" in message
        or "summary" in message
        or "note" in message
    ):
        return (
            "I can help summarize notes. "
            "Use the Note Summarizer tool below."
        )

    if (
        "email" in message
        or "mail" in message
    ):
        return (
            "I can help generate professional emails. "
            "Use the Email Generator tool below."
        )

    if (
        "task" in message
        or "goal" in message
        or "plan" in message
    ):
        return (
            "I can help break goals into actionable tasks. "
            "Use the Task Breakdown tool below."
        )

    if (
        "budget" in message
        or "expense" in message
        or "spending" in message
        or "money" in message
    ):
        return (
            "I can help analyze your budget and spending. "
            "Use the Budget Insights tool below."
        )

    return (
        "I can help with note summaries, email generation, "
        "task planning and budget insights."
    )


def chat(message: str) -> str:

    try:
        return ask_nemotron(message)

    except Exception as error:

        print(
            f"Nemotron Error: {error}"
        )

        return mock_response(message)