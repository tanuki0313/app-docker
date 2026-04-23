from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import create_engine, text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aiworklab.jp", "https://d59awmwd9zst4.cloudfront.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB接続
DATABASE_URL = "mysql+pymysql://admin:{Gql9W0b2_MX.}Du@my-rds.ct0q0ugm42z3.ap-northeast-1.rds.amazonaws.com:3306/appdb"
engine = create_engine(DATABASE_URL)

# =========================
# 管理画面
# =========================
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>ブログアクセス数画面</h1>
    <h2>今日のアクセス数</h2>
    <div id="daily">0</div>
    <h2>総合アクセス数</h2>
    <div id="total">0</div>
    <h2>人気記事ランキング</h2>
    <ul id="top"></ul>
    <script>
    fetch("/stats/total").then(res => res.json()).then(data => {
        document.getElementById("total").innerText = data.total;
    });
    fetch("/stats/daily").then(res => res.json()).then(data => {
        document.getElementById("daily").innerText = data.daily;
    });
    fetch("/stats/top").then(res => res.json()).then(data => {
        const ul = document.getElementById("top");
        ul.innerHTML = "";
        data.top.forEach(item => {
            const li = document.createElement("li");
            li.innerText = item.path + " : " + item.count;
            ul.appendChild(li);
        });
    });
    </script>
    """

# =========================
# ログ登録（DBに保存）
# =========================
@app.post("/log")
def log(data: dict):
    with engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO access_log (article_id, count, access_date) VALUES (:article_id, 1, :access_date)"
        ), {"article_id": data.get("path", "/"), "access_date": datetime.now().date()})
        conn.commit()
    return {"status": "ok"}

# =========================
# 総合アクセス数（DBから集計）
# =========================
@app.get("/stats/total")
def total():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT SUM(count) FROM access_log"))
        total = result.scalar() or 0
    return {"total": total}

# =========================
# 今日のアクセス数（DBから集計）
# =========================
@app.get("/stats/daily")
def daily():
    today = datetime.now().date()
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT SUM(count) FROM access_log WHERE access_date = :today"
        ), {"today": today})
        count = result.scalar() or 0
    return {"daily": count}

# =========================
# 人気記事ランキング（DBから集計）
# =========================
@app.get("/stats/top")
def top():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT article_id, SUM(count) as total FROM access_log GROUP BY article_id ORDER BY total DESC LIMIT 5"
        ))
        top_list = [{"path": str(row[0]), "count": row[1]} for row in result]
    return {"top": top_list}