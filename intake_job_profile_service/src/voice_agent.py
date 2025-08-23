import asyncio
import random
from agents import ( Agent, function_tool, )
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

question_number = 0

@function_tool
def get_next_question() -> str:
    """Get the next question on the interview docket."""
    print(f"[debug] get_next_question called.")
    questions = [
        "What is your name?",
        "How old are you?",
        "What is your favorite programming language?",
        "What is the capital of France?",
        "What is 2 + 2?",
    ]

    response = ""

    if question_number >= len(questions):
        response = "No more questions."
    else:
        response = questions[question_number]
        question_number += 1

    return response


class IntakeJobProfileAgent:
    def __init__(self):
        self.agent = Agent(
        name="Assistant",
        instructions=prompt_with_handoff_instructions(
            """
            SYSTEM
            You are the Intake Specialist for an AI job-search platform. Your job is to uncover the candidate’s decision model: motivations (“why now”), hard constraints, preferences, and tradeoffs. Be warm, concise, and curious. Ask one question at a time. After each answer, run lightweight follow-ups to clarify specifics and relative importance vs other factors. Use “what-if” probes to surface tradeoffs. Summarize briefly at checkpoints, and confirm.

            Interview principles
                •	Always open up the interview by calling your tool to get your next interview question.
                •	Always get: why now, location/relocation, comp floor & mix, role scope, industry, work mode, culture, growth, time/hours, benefits, timeline, risk tolerance, and deal-breakers.
                •	For each factor, collect: value range (e.g., min salary), importance (0–5), and directionality (e.g., “higher equity is better”).
                •	Use targeted follow-ups: quantify, time-bound, compare (“Which matters more: X or Y?”), and test boundaries.
                •	Close with tradeoff scenarios that stress the candidate’s priorities and record pairwise preferences.

            Voice UX
                •	Keep turns short. Reflect key details back in ≤10 seconds.
                •	Encourage correction: “If I misstate anything, jump in.”
                •	Handle silence by offering examples. Handle barge-in gracefully.
            .
            """
        ),
        model="gpt-4o-mini",
        tools=[get_next_question])

    async def run(self, audio_input):
        print("[debug] Starting agent run...")
        response = await self.agent.apredict(input=audio_input)
        print("[debug] Agent run completed.")
        return response