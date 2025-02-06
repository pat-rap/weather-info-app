from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import urllib.parse
from contextlib import asynccontextmanager

from src.scheduler import start_scheduler
from src.auth import router as auth_router
from src.auth import get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # アプリ起動時の処理
    start_scheduler()
    # lifespan の中で起動時の処理 (yield の前) と終了時の処理 (yield の後) を書ける
    yield
    # アプリ終了時の処理（必要に応じて）

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# 認証用エンドポイントの追加
app.include_router(auth_router)

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

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
