
import os, json, hmac, hashlib, secrets, uuid, sqlite3, asyncio
from pathlib import Path
from datetime import date, datetime
from typing import Optional
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel, Field

BASE=Path(__file__).resolve().parent
DB=Path(os.getenv("BRONI_DB",str(BASE/"broni.sqlite3")))
UPLOADS=Path(os.getenv("BRONI_UPLOADS",str(BASE/"uploads"))); UPLOADS.mkdir(parents=True,exist_ok=True)
SECRET=os.getenv("APP_SECRET",secrets.token_hex(32))
BOT_TOKEN=os.getenv("BOT_TOKEN","")
ADMIN_CHAT_ID=os.getenv("ADMIN_CHAT_ID","")
ADMIN_LOGIN=os.getenv("ADMIN_LOGIN","admin")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD","change-me-now")

app=FastAPI(title="Broni API")
PUBLIC_API_BASE=os.getenv('PUBLIC_API_BASE','https://tihiiidon.bothost.tech').rstrip('/')
FRONTEND_ORIGINS=[x.strip().rstrip('/') for x in os.getenv('FRONTEND_ORIGINS','').split(',') if x.strip()]
if PUBLIC_API_BASE not in FRONTEND_ORIGINS:
    FRONTEND_ORIGINS.append(PUBLIC_API_BASE)
# Разрешаем работу интерфейса как с этого же домена, так и с отдельного фронтенда.
app.add_middleware(CORSMiddleware,allow_origins=FRONTEND_ORIGINS,allow_origin_regex=r'https?://.*',allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

# На HTTPS-сайте сессия должна передаваться только по защищённому соединению.
app.add_middleware(SessionMiddleware,secret_key=SECRET,same_site="lax",https_only=True)

def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c
def now(): return datetime.now().astimezone().replace(microsecond=0).isoformat()
def hp(p,s=None):
    s=s or secrets.token_hex(16); d=hashlib.pbkdf2_hmac("sha256",p.encode(),s.encode(),160000).hex(); return s+"$"+d
def vp(p,e):
    try:
        s,d=e.split("$",1); return hmac.compare_digest(hashlib.pbkdf2_hmac("sha256",p.encode(),s.encode(),160000).hex(),d)
    except: return False
def me(req):
    uid=req.session.get("uid")
    if not uid:return None
    c=conn(); r=c.execute("select * from users where id=?",(uid,)).fetchone(); c.close()
    return dict(r) if r else None
def user(req):
    u=me(req)
    if not u: raise HTTPException(401,"Требуется вход")
    return u
def admin(req):
    u=user(req)
    if u["role"]!="admin": raise HTTPException(403,"Нет доступа")
    return u
def house(r):
    x=dict(r); x["amenities"]=json.loads(x["amenities"] or "[]"); x["images"]=json.loads(x["images"] or "[]"); x["active"]=bool(x["active"]); return x

def init():
    c=conn(); c.executescript("""
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,tg_id TEXT UNIQUE,name TEXT NOT NULL,phone TEXT DEFAULT '',password_hash TEXT DEFAULT '',role TEXT DEFAULT 'user',created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS houses(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,description TEXT DEFAULT '',price INTEGER NOT NULL,guests INTEGER DEFAULT 2,bedrooms INTEGER DEFAULT 1,bathrooms INTEGER DEFAULT 1,area REAL DEFAULT 0,amenities TEXT DEFAULT '[]',images TEXT DEFAULT '[]',active INTEGER DEFAULT 1,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,house_id INTEGER NOT NULL,check_in TEXT NOT NULL,check_out TEXT NOT NULL,guests INTEGER DEFAULT 1,comment TEXT DEFAULT '',status TEXT DEFAULT 'confirmed',created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS favorites(user_id INTEGER NOT NULL,house_id INTEGER NOT NULL,created_at TEXT NOT NULL,PRIMARY KEY(user_id,house_id));
    CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,booking_id INTEGER,house_id INTEGER,category TEXT NOT NULL,message TEXT NOT NULL,status TEXT DEFAULT 'new',created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    """)
    if not c.execute("select 1 from settings where key='theme'").fetchone(): c.execute("insert into settings values('theme','light')")
    if c.execute("select count(*) n from houses").fetchone()["n"]==0:
        demos=[("Дом №1","Уютный дом с панорамными окнами и видом на природу.",8000,4,1,1,48,["Wi‑Fi","Кухня","Парковка","Баня","Терраса"]),("Дом №2","Просторный дом для компании, рядом лес и вода.",11000,6,2,2,72,["Wi‑Fi","Кухня","Парковка","Чан","Мангал"]),("Дом №3","Тихий компактный дом для пары или семьи.",7000,4,1,1,40,["Wi‑Fi","Кухня","Парковка"]),("Дом №4","Большой дом для компании с зоной отдыха.",14000,8,3,2,96,["Wi‑Fi","Кухня","Парковка","Чан","Мангал","Терраса"])]
        for x in demos:c.execute("insert into houses(title,description,price,guests,bedrooms,bathrooms,area,amenities,images,active,created_at,updated_at) values(?,?,?,?,?,?,?,?,?,?,?,?)",(*x[:7],json.dumps(x[7],ensure_ascii=False),json.dumps([]),1,now(),now()))
    c.commit(); c.close()
init()

class Register(BaseModel): name:str=Field(min_length=2,max_length=80); phone:str=""; password:str=Field(min_length=6,max_length=128)
class Login(BaseModel): name:str; password:str
class Booking(BaseModel): house_id:int; check_in:str; check_out:str; guests:int=Field(ge=1,le=50); comment:str=""
class Report(BaseModel): booking_id:Optional[int]=None; house_id:Optional[int]=None; category:str; message:str
class Theme(BaseModel): theme:str

@app.get("/",response_class=HTMLResponse)
async def index():
    for name in ("broni.html", "broni(2).html", "broni(1).html"):
        p=BASE/name
        if p.exists():
            return HTMLResponse(p.read_text(encoding="utf-8"))
    raise HTTPException(500,"Файл интерфейса broni.html не найден")
@app.get("/uploads/{name}")
async def upload(name:str):
    p=UPLOADS/Path(name).name
    if not p.exists(): raise HTTPException(404,"Файл не найден")
    return FileResponse(p)
@app.get("/health")
async def health(): return {"ok":True,"service":"broni","database":str(DB.name)}

@app.get("/api/info")
async def api_info():
    return {"ok":True,"api":PUBLIC_API_BASE+"/api","api_base":PUBLIC_API_BASE,"telegram_configured":bool(BOT_TOKEN)}

@app.get("/api/config")
async def config():
    c=conn(); r=c.execute("select value from settings where key='theme'").fetchone(); c.close(); return {"theme":r["value"] if r else "light","api_base":PUBLIC_API_BASE}
@app.post("/api/auth/register")
async def register(x:Register,request:Request):
    c=conn()
    if c.execute("select id from users where lower(name)=lower(?)",(x.name.strip(),)).fetchone(): c.close(); raise HTTPException(409,"Такое имя уже занято")
    cur=c.execute("insert into users(name,phone,password_hash,role,created_at) values(?,?,?,?,?)",(x.name.strip(),x.phone.strip(),hp(x.password),"user",now())); c.commit(); uid=cur.lastrowid; c.close(); request.session["uid"]=uid
    return {"user":{"id":uid,"name":x.name.strip(),"phone":x.phone,"role":"user"}}
@app.post("/api/auth/login")
async def login(x:Login,request:Request):
    c=conn(); r=c.execute("select * from users where lower(name)=lower(?)",(x.name.strip(),)).fetchone(); c.close()
    if not r or not vp(x.password,r["password_hash"]): raise HTTPException(401,"Неверное имя или пароль")
    request.session["uid"]=r["id"]; return {"user":{"id":r["id"],"name":r["name"],"phone":r["phone"],"role":r["role"]}}
@app.post("/api/auth/logout")
async def logout(request:Request): request.session.clear(); return {"success":True}
@app.get("/api/auth/me")
async def authme(request:Request):
    u=me(request); return {"user":({"id":u["id"],"name":u["name"],"phone":u["phone"],"role":u["role"]} if u else None)}

@app.post("/api/auth/telegram")
async def telegram(x:dict,request:Request):
    if not BOT_TOKEN: raise HTTPException(503,"Telegram авторизация не настроена")
    raw=x.get("initData",""); parts=dict(p.split("=",1) for p in raw.split("&") if "=" in p); got=parts.pop("hash","")
    check="\n".join(f"{k}={parts[k]}" for k in sorted(parts)); secret=hmac.new(b"WebAppData",BOT_TOKEN.encode(),hashlib.sha256).digest()
    expected=hmac.new(secret,check.encode(),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(got,expected): raise HTTPException(401,"Недействительная Telegram-сессия")
    tg=json.loads(parts.get("user","{}")); tid=str(tg.get("id",""))
    if not tid: raise HTTPException(400,"Telegram ID не найден")
    c=conn(); r=c.execute("select * from users where tg_id=?",(tid,)).fetchone()
    if not r:
        name=(x.get("name") or tg.get("first_name") or "Гость")[:80]; cur=c.execute("insert into users(tg_id,name,role,created_at) values(?,?,?,?)",(tid,name,"user",now())); c.commit(); r=c.execute("select * from users where id=?",(cur.lastrowid,)).fetchone()
    request.session["uid"]=r["id"]; c.close(); return {"user":{"id":r["id"],"name":r["name"],"role":r["role"]}}

@app.get("/api/houses")
async def houses(search:str="",amenity:str="",guests:int=0):
    c=conn(); rows=c.execute("select * from houses where active=1 order by id").fetchall(); c.close(); out=[]
    for r in rows:
        h=house(r)
        if search and search.lower() not in (h["title"]+" "+h["description"]).lower(): continue
        if amenity and amenity not in h["amenities"]: continue
        if guests and h["guests"]<guests: continue
        out.append(h)
    return {"houses":out}
@app.get("/api/houses/{hid}")
async def onehouse(hid:int):
    c=conn(); r=c.execute("select * from houses where id=? and active=1",(hid,)).fetchone(); c.close()
    if not r: raise HTTPException(404,"Дом не найден")
    return {"house":house(r)}
@app.get("/api/favorites")
async def favs(request:Request):
    u=user(request); c=conn(); r=c.execute("select house_id from favorites where user_id=?",(u["id"],)).fetchall(); c.close(); return {"favorites":[x["house_id"] for x in r]}
@app.post("/api/favorites/{hid}")
async def fav(hid:int,request:Request):
    u=user(request); c=conn(); ex=c.execute("select 1 from favorites where user_id=? and house_id=?",(u["id"],hid)).fetchone()
    if ex:c.execute("delete from favorites where user_id=? and house_id=?",(u["id"],hid)); val=False
    else:c.execute("insert into favorites values(?,?,?)",(u["id"],hid,now())); val=True
    c.commit(); c.close(); return {"favorite":val}

@app.post("/api/bookings")
async def make_booking(x:Booking,request:Request):
    u=user(request)
    try:a=date.fromisoformat(x.check_in); b=date.fromisoformat(x.check_out)
    except: raise HTTPException(400,"Некорректные даты")
    if a<date.today() or b<=a: raise HTTPException(400,"Проверьте даты")
    c=conn(); h=c.execute("select * from houses where id=? and active=1",(x.house_id,)).fetchone()
    if not h: c.close(); raise HTTPException(404,"Дом не найден")
    if x.guests>h["guests"]: c.close(); raise HTTPException(400,"Слишком много гостей")
    busy=c.execute("select id from bookings where house_id=? and status='confirmed' and check_in<? and check_out>?",(x.house_id,b.isoformat(),a.isoformat())).fetchone()
    if busy:c.close(); raise HTTPException(409,"Эти даты уже заняты")
    cur=c.execute("insert into bookings(user_id,house_id,check_in,check_out,guests,comment,status,created_at) values(?,?,?,?,?,?,?,?)",(u["id"],x.house_id,a.isoformat(),b.isoformat(),x.guests,x.comment,"confirmed",now())); c.commit(); bid=cur.lastrowid; c.close()
    return {"booking_id":bid}
@app.get("/api/bookings")
async def bookings(request:Request):
    u=user(request); c=conn(); rs=c.execute("select b.*,h.title,h.price,h.images from bookings b join houses h on h.id=b.house_id where b.user_id=? order by b.id desc",(u["id"],)).fetchall(); c.close(); out=[]
    for r in rs:
        x=dict(r); x["images"]=json.loads(x["images"] or "[]"); x["nights"]=(date.fromisoformat(x["check_out"])-date.fromisoformat(x["check_in"])).days; x["total"]=x["nights"]*x["price"]; out.append(x)
    return {"bookings":out}
@app.post("/api/bookings/{bid}/cancel")
async def cancel(bid:int,request:Request):
    u=user(request); c=conn(); r=c.execute("select id from bookings where id=? and user_id=?",(bid,u["id"])).fetchone()
    if not r:c.close(); raise HTTPException(404,"Бронирование не найдено")
    c.execute("update bookings set status='cancelled' where id=?",(bid,)); c.commit(); c.close(); return {"success":True}

async def tg_notify(text):
    if not BOT_TOKEN or not ADMIN_CHAT_ID:return
    try:
        import urllib.request
        data=json.dumps({"chat_id":ADMIN_CHAT_ID,"text":text}).encode()
        req=urllib.request.Request(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data=data,headers={"Content-Type":"application/json"},method="POST")
        await asyncio.to_thread(urllib.request.urlopen,req,timeout=8)
    except: pass
@app.post("/api/reports")
async def report(x:Report,request:Request):
    u=user(request); c=conn(); cur=c.execute("insert into reports(user_id,booking_id,house_id,category,message,status,created_at) values(?,?,?,?,?,?,?)",(u["id"],x.booking_id,x.house_id,x.category,x.message,"new",now())); rid=cur.lastrowid; c.commit(); c.close()
    await tg_notify(f"🚨 Новая проблема #{rid}\nГость: {u['name']}\nКатегория: {x.category}\n{x.message}")
    return {"report_id":rid}

@app.post("/api/admin/login")
async def alogin(x:Login,request:Request):
    if not hmac.compare_digest(x.name,ADMIN_LOGIN) or not hmac.compare_digest(x.password,ADMIN_PASSWORD): raise HTTPException(401,"Неверные данные администратора")
    c=conn(); r=c.execute("select id from users where lower(name)=lower(?)",(ADMIN_LOGIN,)).fetchone()
    if r: uid=r["id"]; c.execute("update users set role='admin',password_hash=? where id=?",(hp(ADMIN_PASSWORD),uid))
    else: cur=c.execute("insert into users(name,password_hash,role,created_at) values(?,?,?,?)",(ADMIN_LOGIN,hp(ADMIN_PASSWORD),"admin",now())); uid=cur.lastrowid
    c.commit(); c.close(); request.session["uid"]=uid; return {"user":{"id":uid,"name":ADMIN_LOGIN,"role":"admin"}}

@app.get("/api/admin/dashboard")
async def dashboard(request:Request):
    admin(request); c=conn()
    counts={k:c.execute(q).fetchone()["n"] for k,q in {"houses":"select count(*) n from houses","active":"select count(*) n from houses where active=1","bookings":"select count(*) n from bookings where status='confirmed'","reports":"select count(*) n from reports where status='new'"}.items()}
    reps=c.execute("select r.*,u.name,h.title from reports r join users u on u.id=r.user_id left join houses h on h.id=r.house_id order by r.id desc limit 100").fetchall(); bs=c.execute("select b.*,u.name user_name,h.title from bookings b join users u on u.id=b.user_id join houses h on h.id=b.house_id order by b.id desc limit 100").fetchall(); c.close()
    return {"counts":counts,"reports":[dict(x) for x in reps],"bookings":[dict(x) for x in bs]}
@app.get("/api/admin/houses")
async def ahouses(request:Request):
    admin(request); c=conn(); rs=c.execute("select * from houses order by id desc").fetchall(); c.close(); return {"houses":[house(x) for x in rs]}
@app.post("/api/admin/houses")
async def create_house(request:Request,title:str=Form(...),description:str=Form(""),price:int=Form(...),guests:int=Form(2),bedrooms:int=Form(1),bathrooms:int=Form(1),area:float=Form(0),amenities:str=Form("[]"),images:list[UploadFile]=File(default=[])):
    admin(request)
    try: am=json.loads(amenities)
    except: am=[x.strip() for x in amenities.split(",") if x.strip()]
    saved=[]
    for f in images[:12]:
        if not f.filename:continue
        ext=Path(f.filename).suffix.lower()
        if ext not in [".jpg",".jpeg",".png",".webp"]:continue
        data=await f.read()
        if len(data)>8*1024*1024:continue
        name=uuid.uuid4().hex+ext; (UPLOADS/name).write_bytes(data); saved.append("/uploads/"+name)
    c=conn(); cur=c.execute("insert into houses(title,description,price,guests,bedrooms,bathrooms,area,amenities,images,created_at,updated_at) values(?,?,?,?,?,?,?,?,?,?,?,?)",(title,description,max(price,0),max(guests,1),max(bedrooms,1),max(bathrooms,1),max(area,0),json.dumps(am,ensure_ascii=False),json.dumps(saved),now(),now())); c.commit(); hid=cur.lastrowid; c.close(); return {"house_id":hid}
@app.post("/api/admin/houses/{hid}/images")
async def add_images(hid:int,request:Request,images:list[UploadFile]=File(...)):
    admin(request); c=conn(); r=c.execute("select images from houses where id=?",(hid,)).fetchone()
    if not r:c.close();raise HTTPException(404,"Дом не найден")
    saved=json.loads(r["images"] or "[]")
    for f in images[:12]:
        ext=Path(f.filename or "").suffix.lower()
        if ext not in [".jpg",".jpeg",".png",".webp"]:continue
        data=await f.read()
        if len(data)>8*1024*1024:continue
        n=uuid.uuid4().hex+ext;(UPLOADS/n).write_bytes(data);saved.append("/uploads/"+n)
    c.execute("update houses set images=?,updated_at=? where id=?",(json.dumps(saved),now(),hid));c.commit();c.close();return {"images":saved}
@app.delete("/api/admin/houses/{hid}")
async def hide_house(hid:int,request:Request):
    admin(request);c=conn();c.execute("update houses set active=0,updated_at=? where id=?",(now(),hid));c.commit();c.close();return {"success":True}
@app.post("/api/admin/reports/{rid}/close")
async def close_report(rid:int,request:Request):
    admin(request);c=conn();c.execute("update reports set status='closed' where id=?",(rid,));c.commit();c.close();return {"success":True}
@app.post("/api/admin/settings/theme")
async def theme(x:Theme,request:Request):
    admin(request)
    if x.theme not in ["light","dark","system"]:raise HTTPException(400,"Недопустимая тема")
    c=conn();c.execute("insert into settings(key,value) values('theme',?) on conflict(key) do update set value=excluded.value",(x.theme,));c.commit();c.close();return {"theme":x.theme}

if __name__=="__main__":
    import uvicorn; uvicorn.run("bot:app",host="0.0.0.0",port=int(os.getenv("PORT","8000")))
