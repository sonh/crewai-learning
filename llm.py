from crewai import LLM

gpt35tubo = LLM(
    model="gpt-3.5-turbo",
    temperature=0.5,
)