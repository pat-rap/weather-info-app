from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import urllib.parse
from src.scheduler import start_scheduler

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    # スケジューラーを起動する
    start_scheduler()

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    # Cookieから取得した値は必要に応じてデコード（unquote）する
    prefecture = request.cookies.get("prefecture", "")
    if prefecture:
        prefecture = urllib.parse.unquote(prefecture, encoding="utf-8")
    category = request.cookies.get("category", "")
    if category:
        category = urllib.parse.unquote(category, encoding="utf-8")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prefecture": prefecture,
        "category": category,
    })

@app.post("/select", response_class=HTMLResponse)
async def select(request: Request, prefecture: str = Form(...), category: str = Form(...)):
    # Cookieに保存する前にURLエンコードする
    encoded_prefecture = urllib.parse.quote(prefecture, encoding="utf-8")
    encoded_category = urllib.parse.quote(category, encoding="utf-8")
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="prefecture", value=encoded_prefecture)
    response.set_cookie(key="category", value=encoded_category)
    return response
