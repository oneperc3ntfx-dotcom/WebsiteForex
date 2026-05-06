from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

VALID_CODES = ["VIP123"]

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/")
async def login(request: Request, code: str = Form(...)):
    if code in VALID_CODES:
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie(key="access", value=code)
        return response
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Kode salah"
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not request.cookies.get("access"):
        return RedirectResponse("/")
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/pair/{name}", response_class=HTMLResponse)
async def pair(request: Request, name: str):
    if not request.cookies.get("access"):
        return RedirectResponse("/")
    return templates.TemplateResponse("pair.html", {
        "request": request,
        "pair": name.upper()
    })
