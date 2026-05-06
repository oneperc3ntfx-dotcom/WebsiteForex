from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# ================= STATIC =================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================= TEMPLATES =================
templates = Jinja2Templates(directory="templates")

# 🔥 FIX: reset Jinja cache (penting di container)
templates.env.cache = {}

# ================= DATA =================
VALID_CODES = ["VIP123"]

# ================= LOGIN PAGE =================
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/")
async def login(request: Request, code: str = Form(...)):
    if code in VALID_CODES:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access", value=code)
        return response

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Kode salah"
    })


# ================= DASHBOARD =================
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    access = request.cookies.get("access")

    if not access:
        return RedirectResponse(url="/")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": access
    })


# ================= PAIR PAGE =================
@app.get("/pair/{name}", response_class=HTMLResponse)
async def pair(request: Request, name: str):
    access = request.cookies.get("access")

    if not access:
        return RedirectResponse(url="/")

    return templates.TemplateResponse("pair.html", {
        "request": request,
        "pair": name.upper() if name else "UNKNOWN",
        "user": access
    })
