import json
from datetime import date, timedelta
from typing import Any, Dict, List

from app.ai.schemas.ai import StudyPlannerRequest
from app.ai.services.nemotron_service import ask_nemotron_simple


def build_study_planner_prompt(
    request: StudyPlannerRequest
) -> str:

    payload = request.dict()

    return f"""
Act as an experienced academic study coach.

Create a realistic personalized study planner using the student's inputs.

Planning requirements:
- Balance workload across days.
- Avoid overloading any single day.
- Consider assignment deadlines.
- Prioritize difficult subjects and earlier exams.
- Include revision sessions before exams.
- Include break sessions.
- Respect available study hours per day.
- Use preferred session length where possible.
- Produce only valid JSON. Do not include markdown, commentary, or raw text outside JSON.

Student input JSON:
{json.dumps(payload, default=str)}

Return JSON with this exact shape:
{{
  "weekly_schedule": [
    {{
      "day": "Monday",
      "total_minutes": 180,
      "sessions": [
        {{
          "subject": "Database Systems",
          "duration_minutes": 90,
          "activity": "Study indexing and normalization",
          "type": "study"
        }}
      ]
    }}
  ],
  "daily_plan": [
    {{
      "date": "2026-06-29",
      "focus": "Database Systems fundamentals",
      "sessions": [
        {{
          "subject": "Database Systems",
          "duration_minutes": 90,
          "activity": "Practice ER diagrams",
          "type": "study"
        }}
      ]
    }}
  ],
  "priority_order": [
    {{
      "subject": "Database Systems",
      "reason": "Exam is earlier and difficulty is high",
      "rank": 1
    }}
  ],
  "recommended_study_duration": [
    {{
      "subject": "Database Systems",
      "minutes_per_week": 360,
      "reason": "Hard subject with an early exam"
    }}
  ],
  "revision_schedule": [
    {{
      "subject": "Database Systems",
      "date": "2026-07-02",
      "focus": "Revise weak topics and past questions"
    }}
  ],
  "break_suggestions": [
    "Take a 10 minute break after each long session"
  ],
  "study_tips": [
    "Start each session with one clear outcome"
  ],
  "explanation": "Database Systems is scheduled first because the exam is earlier."
}}
"""


def generate_study_plan_with_ai(
    request: StudyPlannerRequest
) -> Dict[str, Any]:

    prompt = build_study_planner_prompt(
        request
    )
    response = ask_nemotron_simple(
        prompt,
        max_tokens=1800
    )

    return _parse_json_response(
        response
    )


def build_fallback_study_plan(
    request: StudyPlannerRequest
) -> Dict[str, Any]:

    subjects = sorted(
        request.subjects,
        key=lambda subject: (
            subject.exam_date,
            _difficulty_weight(subject.difficulty) * -1
        )
    )
    session_minutes = int(
        request.preferred_session_length
    )
    daily_limit = int(
        request.available_hours_per_day * 60
    )
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]
    today = date.today()
    weekly_schedule: List[Dict[str, Any]] = []
    daily_plan: List[Dict[str, Any]] = []

    for index, day in enumerate(days):
        subject = subjects[
            index % len(subjects)
        ]
        study_minutes = min(
            session_minutes,
            daily_limit
        )
        sessions = [
            {
                "subject": subject.name,
                "duration_minutes": study_minutes,
                "activity": f"Study core topics for {subject.name}",
                "type": "study"
            }
        ]

        if daily_limit >= study_minutes + 30:
            sessions.append(
                {
                    "subject": "Break",
                    "duration_minutes": 10,
                    "activity": "Reset before the next study block",
                    "type": "break"
                }
            )
            sessions.append(
                {
                    "subject": subject.name,
                    "duration_minutes": min(30, daily_limit - study_minutes),
                    "activity": f"Revise recent notes for {subject.name}",
                    "type": "revision"
                }
            )

        total_minutes = sum(
            session["duration_minutes"]
            for session in sessions
        )
        plan_date = today + timedelta(
            days=index
        )

        weekly_schedule.append(
            {
                "day": day,
                "total_minutes": total_minutes,
                "sessions": sessions
            }
        )
        daily_plan.append(
            {
                "date": plan_date.isoformat(),
                "focus": f"{subject.name} priority study",
                "sessions": sessions
            }
        )

    return {
        "weekly_schedule": weekly_schedule,
        "daily_plan": daily_plan,
        "priority_order": [
            {
                "subject": subject.name,
                "reason": (
                    "Prioritized by exam date and difficulty level."
                ),
                "rank": index + 1
            }
            for index, subject in enumerate(subjects)
        ],
        "recommended_study_duration": [
            {
                "subject": subject.name,
                "minutes_per_week": (
                    session_minutes * _difficulty_weight(subject.difficulty)
                ),
                "reason": (
                    f"{subject.difficulty} difficulty and exam on "
                    f"{subject.exam_date.isoformat()}."
                )
            }
            for subject in subjects
        ],
        "revision_schedule": [
            {
                "subject": subject.name,
                "date": max(
                    today,
                    subject.exam_date - timedelta(days=2)
                ).isoformat(),
                "focus": "Review summaries, weak areas, and practice questions."
            }
            for subject in subjects
        ],
        "break_suggestions": [
            "Take a 5 to 10 minute break between study sessions.",
            "Use one longer break after two focused sessions."
        ],
        "study_tips": [
            "Begin each session with one measurable goal.",
            "End each day by marking topics that need revision.",
            "Use active recall before rereading notes."
        ],
        "explanation": (
            "Subjects are ordered by earlier exam dates and higher difficulty. "
            "Sessions are kept within the available daily study time and include "
            "revision blocks so the plan stays realistic."
        )
    }


def _parse_json_response(
    response: str
) -> Dict[str, Any]:

    text = response.strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("AI response did not contain JSON.")

    return json.loads(
        text[start:end + 1]
    )


def _difficulty_weight(
    difficulty: str
) -> int:

    return {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }.get(
        difficulty,
        1
    )
