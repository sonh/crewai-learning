import os

from crewai import Agent, Task, Crew, Process, LLM

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

teaching_assistant = Agent(
    role="Senior Teaching Assistant",
    goal="The first agent to receive the {question}, summarize, analyze to give insights. Prepare the first answer",
    backstory="10 years of experience in teaching and learning support"
              "Assist the students/learners/ by recording/noting their questions"
              "you used to be an tutor, know well about activities at schools and universities",
    llm="gpt-3.5-turbo",
    verbose=True,
    allow_delegation=False,
    max_rpm=30
)

math_teacher = Agent(
    role="Math Teacher",
    goal="Verify existing conclusion, try to resolve to the {question}, then give instruction to resolve it.",
    backstory="With over 10 years of experience in education, especially in math",
    llm="gpt-3.5-turbo",
    verbose=True,
    allow_delegation=False,
    max_rpm=30
)

teaching_support_task = Task(
    description="""
        Summarize the {question}, extract the essential information we have to resolve.
        Try to answer the {question} yourself first to get a answer.
    """,
    expected_output="""
        A recap of the question the answer for it
    """,
    agent=teaching_assistant
)

math_resolving_task = Task(
    description="""
        Try to resolve the {question} by yourself, then verify the first answer/conclusion.
        Give the A step by step instruction.
    """,
    expected_output="""
        A step by step instruction to follow the final answer to resolve the {question}, 
        Keep them short, concise, easy to understanding, less than 200 words, the lesser the better.
    """,
    agent=math_teacher,
    context=[teaching_support_task]
)