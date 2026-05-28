from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="KIOAI Mini Automation API")


class Lead(BaseModel):
    name: str
    email: str
    message: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "mini-automation-api"}


@app.post("/lead")
def create_lead(lead: Lead):
    return {
        "success": True,
        "message": "Lead received successfully",
        "data": lead,
    }
