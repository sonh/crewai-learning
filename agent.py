import os

from crewai import Agent, Task, Crew, Process, LLM
from llm import gpt35tubo
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

csv_source = CSVKnowledgeSource(
    file_paths=["cloze_math.csv", "mcq.csv"]
)

teaching_assistant = Agent(
    role="Senior Teaching Assistant",
    goal="The first agent to receive the {question}, summarize, analyze to give insights. Prepare the first answer",
    backstory="10 years of experience in teaching and learning support"
              "Assist the students/learners/ by recording/noting their questions"
              "you used to be an tutor, know well about activities at schools and universities",
    llm=gpt35tubo,
    knowledge_sources=[csv_source],
    verbose=True,
    allow_delegation=False,
    max_rpm=30
)

math_teacher = Agent(
    role="Math Teacher",
    goal="Verify existing conclusion, try to resolve to the {question}, then give explanation to resolve it.",
    backstory="With over 10 years of experience in education, especially in math",
    llm=gpt35tubo,
    knowledge_sources=[csv_source],
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
        A recap of the question the answer for it.
        The first result of the question, no need to explain.
    """,
    agent=teaching_assistant
)

math_resolving_task = Task(
    description="""
        Try to resolve the {question} by yourself, then verify with the first result.
        Give the A step by step explanation.
    """,
    expected_output="""
        Show the result
        Must have a step by step explanation show how to resolve it.
        Keep them short, concise, easy to understanding, the lesser the better.
    """,
    agent=math_teacher,
    context=[teaching_support_task]
)
