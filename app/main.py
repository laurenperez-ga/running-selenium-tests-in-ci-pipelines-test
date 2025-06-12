from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, constr
from pathlib import Path

app = FastAPI()

# Serve files from the "static" folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Model for validating form input
class SignupForm(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr


@app.get("/signup", response_class=HTMLResponse)
def get_signup_form():
    # Load and return the signup HTML file
    html_path = Path("static/newsletter_signup.html")
    return html_path.read_text()


@app.post("/signup")
def post_signup(
    name: str = Form(...),
    email: str = Form(...)
):
    # FastAPI automatically validates these against the type hints
    form = SignupForm(name=name, email=email)
    return {"message": f"Thanks for subscribing, {form.name}!"}
