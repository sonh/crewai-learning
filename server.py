from crewai import Crew, Process
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent import teaching_assistant, math_teacher, teaching_support_task, math_resolving_task

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for security)
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    text: str


@app.post("/api/process")
async def process_text(data: InputData):
    question_answer_crew = Crew(
        agents=[teaching_assistant, math_teacher],
        tasks=[teaching_support_task, math_resolving_task],
        process=Process.sequential,
        verbose=True
    )

    result = question_answer_crew.kickoff(inputs={
        'question': data.text,
    })
    return {"response": result.raw}


@app.get("/", response_class=HTMLResponse)
async def serve_page():
    """Serve a simple HTML page with an input box, button, preview, and response box."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Text Processor</title>
        <style>
            body {
                padding-left: 48px;
            }
        </style>
        <script>
            async function sendData() {
                let inputText = document.getElementById("textInput").value;
                let responseBox = document.getElementById("responseBox");

                // Show "Loading..." text before API call
                responseBox.innerText = "Loading...";

                try {
                    let response = await fetch("/api/process", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ text: inputText })
                    });

                    let data = await response.json();
                    responseBox.innerText = data.response;
                } catch (error) {
                    responseBox.innerText = "Error processing request.";
                }
            }
        </script>
    </head>
    <body>
        <h2>Input question</h2>

        <textarea id="textInput" rows="24" cols="240" placeholder="Enter question here..." oninput="updatePreview()"></textarea><br>
        <br/>
        <button onclick="sendData()">Submit</button>
        <br/>
        <h3>Response:</h3>
        <p id="responseBox"></p>
    </body>
    </html>
    """
