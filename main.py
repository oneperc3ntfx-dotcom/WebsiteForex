from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

# ================= STATIC =================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================= TEMPLATES =================
templates = Jinja2Templates(directory="templates")

# 🔥 FIX IMPORTANT (anti error Jinja cache rusak)
templates.env.cache = {}
templates.env.auto_reload = True

# ================= DATA =================
VALID_CODES = ["VIP123"]

# ================= LOGIN =================
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/")
async def login(request: Request, code: str = Form(...)):
    if code in VALID_CODES:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie("access", code)
        return response

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Kode salah"
    })


# ================= DASHBOARD =================
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not request.cookies.get("access"):
        return RedirectResponse(url="/")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": request.cookies.get("access")
    })


# ================= PAIR =================
@app.get("/pair/{name}", response_class=HTMLResponse)
async def pair(request: Request, name: str):
    if not request.cookies.get("access"):
        return RedirectResponse(url="/")

    return templates.TemplateResponse("pair.html", {
        "request": request,
        "pair": name.upper() if name else "UNKNOWN",
        "user": request.cookies.get("access")
    })
