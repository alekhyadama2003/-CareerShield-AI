from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "project": "CareerShield AI",
        "message": "Workforce Intelligence for the AI Era"
    }