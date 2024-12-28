from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
#from logic.utils import authenticate_user, get_login_time_diff, set_session_cookie, unset_session_cookie, login_required
from  utils import authenticate_user, get_login_time_diff, set_session_cookie, unset_session_cookie, login_required
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
#import secrets
app = FastAPI()
#secret_key=secrets.token_hex(32)
# Configure Session Middleware
load_dotenv()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  if "session" in request.cookies:
    return RedirectResponse(url="/dashboard")
  return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not authenticate_user(username, password):
      raise HTTPException(status_code=401, detail="Invalid credentials")
    response = RedirectResponse(url="/dashboard")
    set_session_cookie(response, session_cookie_name="session")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    login_required(request, session_cookie_name="session")
    login_time = get_login_time_diff(request, session_cookie_name="session")
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": "test", "logged_in_time": login_time})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = templates.TemplateResponse("logout.html", {"request": request})
    unset_session_cookie(response, session_cookie_name="session")
    return response