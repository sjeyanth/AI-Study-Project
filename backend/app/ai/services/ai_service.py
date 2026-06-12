



def summarize_note(content: str) -> str:
    return f"Mock Summary: {content[:100]}"

def generate_mail(purpose: str) -> str:
    return (
        f"Subject: regarding {purpose}\n\n"
        f"Dear Recipient \n\n"
        f"this is a mock email"
        f" {purpose} \n\n"
        f"Best regards\n Sender"
    )

def task_breakdown(
        goal: str
) -> list[str]:
    
    return[
        f"Research {goal}",
        f"Create plan for {goal}",
        f"practice {goal}",
        f"Review progress on {goal}"
    ]


def budget_insights(
    budget_summary: str
) -> str:

    return (
        "Mock Insight: "
        "Monitor your spending and "
        "reduce unnecessary expenses."
    )


