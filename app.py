import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import math
import random
import hashlib
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🚑 ResQ-Path v7.0 — Real-Time Green Corridor", layout="wide", page_icon="🚑")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
html,body,[class*="css"]{font-family:'Rajdhani',sans-serif;background:#060c16;color:#d0e8ff;}
.main{background:linear-gradient(160deg,#060c16 0%,#091220 100%);}
.resq-header{background:linear-gradient(90deg,#0a1828,#0d2040,#0a1828);border:1px solid #1a3a5c;border-radius:14px;padding:1.2rem 2rem;margin-bottom:1rem;position:relative;overflow:hidden;}
.resq-header::after{content:'';position:absolute;top:0;left:-100%;right:0;height:2px;background:linear-gradient(90deg,transparent,#00d4ff,#ff4444,#00d4ff,transparent);animation:scan 3s linear infinite;}
@keyframes scan{to{left:100%;}}
.resq-title{font-family:'Share Tech Mono';font-size:1.8rem;color:#00d4ff;margin:0;}
.resq-sub{color:#3a6a8a;font-size:.85rem;font-family:'Share Tech Mono';}
.mc{background:#0a1828;border:1px solid #1a3a5c;border-radius:10px;padding:1rem;text-align:center;transition:.3s;}
.mc:hover{border-color:#00d4ff;}
.mc.crit{border-color:#ff4444;animation:pb 1.5s infinite;}
@keyframes pb{0%,100%{box-shadow:0 0 0 0 rgba(255,68,68,.4)}50%{box-shadow:0 0 0 8px rgba(255,68,68,0)}}
.mv{font-family:'Share Tech Mono';font-size:1.7rem;color:#00d4ff;}
.mvg{color:#00ff88;}.mvr{color:#ff4444;}.mvo{color:#ffaa00;}
.ml{color:#3a6a8a;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-top:3px;}
.md{font-size:.72rem;margin-top:3px;}
.sig{border-radius:8px;padding:10px 6px;text-align:center;font-family:'Share Tech Mono';font-size:.72rem;border:1px solid #1a3a5c;transition:.4s;}
.sig.green{background:#001a0d;border-color:#00ff88;color:#00ff88;box-shadow:0 0 12px rgba(0,255,136,.25);}
.sig.red{background:#1a0000;border-color:#ff4444;color:#ff4444;}
.sig.yellow{background:#1a1200;border-color:#ffaa00;color:#ffaa00;}
.sig.hold{background:#1a0800;border-color:#ff6600;color:#ff6600;animation:pb 1s infinite;}
.countdown-big{font-family:'Share Tech Mono';font-size:2.8rem;text-align:center;padding:1rem;border-radius:12px;}
.countdown-big.green{color:#00ff88;background:#001a0d;border:2px solid #00ff88;}
.countdown-big.yellow{color:#ffaa00;background:#1a1200;border:2px solid #ffaa00;}
.countdown-big.red{color:#ff4444;background:#1a0000;border:2px solid #ff4444;}
.alert-g{background:#001a0d;border:1px solid #00ff88;border-left:4px solid #00ff88;border-radius:6px;padding:10px 14px;margin:5px 0;font-family:'Share Tech Mono';font-size:.82rem;color:#00cc66;}
.alert-r{background:#1a0000;border:1px solid #ff4444;border-left:4px solid #ff4444;border-radius:6px;padding:10px 14px;margin:5px 0;font-family:'Share Tech Mono';font-size:.82rem;color:#ff8888;animation:pb 2s infinite;}
.alert-b{background:#001020;border:1px solid #00d4ff;border-left:4px solid #00d4ff;border-radius:6px;padding:10px 14px;margin:5px 0;font-family:'Share Tech Mono';font-size:.82rem;color:#00aacc;}
.alert-o{background:#1a0800;border:1px solid #ff6600;border-left:4px solid #ff6600;border-radius:6px;padding:10px 14px;margin:5px 0;font-family:'Share Tech Mono';font-size:.82rem;color:#ff9933;}
.prog-wrap{margin:.8rem 0;}
.prog-bar{height:7px;background:#0a1828;border-radius:4px;overflow:hidden;}
.prog-fill{height:100%;border-radius:4px;transition:width .8s;background:linear-gradient(90deg,#00ff88,#00d4ff);box-shadow:0 0 8px rgba(0,212,255,.5);}
.mission-complete{background:linear-gradient(135deg,#001a0d,#002a15);border:3px solid #00ff88;border-radius:20px;padding:3rem;text-align:center;margin:1rem 0;animation:mglow 2s ease-in-out infinite;}
@keyframes mglow{0%,100%{box-shadow:0 0 20px rgba(0,255,136,.3);}50%{box-shadow:0 0 60px rgba(0,255,136,.8);}}
.mission-title{font-family:'Share Tech Mono';font-size:3rem;color:#00ff88;text-shadow:0 0 20px rgba(0,255,136,.6);margin-bottom:1rem;}
.conflict-resolved{background:#001a0d;border:2px solid #00ff88;border-radius:10px;padding:.8rem 1.2rem;margin:.4rem 0;font-family:'Share Tech Mono';font-size:.85rem;}
[data-testid="stSidebar"]{background:#060c16 !important;border-right:1px solid #1a3a5c !important;}
.stButton>button{background:#0d2040 !important;border:1px solid #1a3a5c !important;color:#00d4ff !important;font-family:'Rajdhani',sans-serif !important;font-weight:700 !important;border-radius:8px !important;transition:.3s !important;}
.stButton>button:hover{border-color:#00d4ff !important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#003366,#004488) !important;border-color:#00d4ff !important;color:#fff !important;}
[data-testid="stMetricValue"]{font-family:'Share Tech Mono' !important;color:#00d4ff !important;}
.stTabs [data-baseweb="tab-list"]{background:#0a1828;border-radius:8px;padding:3px;}
.stTabs [data-baseweb="tab"]{color:#3a6a8a;font-family:'Rajdhani',sans-serif;font-weight:700;}
.stTabs [aria-selected="true"]{background:#0d2040 !important;color:#00d4ff !important;border-radius:6px;}
</style>
<script>
let _actx=null;
function _getCtx(){if(!_actx)_actx=new(window.AudioContext||window.webkitAudioContext)();return _actx;}
function playTone(freq,dur,type,vol){
  try{const ctx=_getCtx();const osc=ctx.createOscillator();const gain=ctx.createGain();
  osc.connect(gain);gain.connect(ctx.destination);osc.frequency.value=freq;osc.type=type||'sine';
  gain.gain.setValueAtTime(vol||0.3,ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+dur);
  osc.start();osc.stop(ctx.currentTime+dur);}catch(e){}}
function playSignalGreen(){playTone(880,.12,'sine',.25);setTimeout(()=>playTone(1100,.18,'sine',.3),130);}
function playCorridorActivate(){playTone(660,.1,'sine',.3);setTimeout(()=>playTone(880,.1,'sine',.3),120);setTimeout(()=>playTone(1100,.2,'sine',.35),240);}
function playMissionComplete(){[523,659,784,1047].forEach((f,i)=>setTimeout(()=>playTone(f,.25,'sine',.35),i*200));}
function playConflict(){playTone(220,.15,'sawtooth',.2);setTimeout(()=>playTone(180,.15,'sawtooth',.2),180);}
function playReroute(){playTone(660,.1,'square',.15);setTimeout(()=>playTone(440,.1,'square',.15),120);setTimeout(()=>playTone(550,.15,'square',.2),250);}
window.resqAudio={playSignalGreen,playCorridorActivate,playMissionComplete,playConflict,playReroute};
</script>
""", unsafe_allow_html=True)

# =============================================================================
# AUTH
# =============================================================================
def _hash(p): return hashlib.sha256(p.encode()).hexdigest()
USERS = {
    "driver1":{"password":_hash("driver123"),"role":"driver","name":"Ambulance Driver 1"},
    "driver2":{"password":_hash("driver456"),"role":"driver","name":"Ambulance Driver 2"},
    "police1":{"password":_hash("police789"),"role":"police","name":"Police Commander"},
    "admin":  {"password":_hash("admin000"), "role":"admin", "name":"System Admin"},
}
for k,v in [("authenticated",False),("user_role",None),("username",None)]:
    if k not in st.session_state: st.session_state[k]=v

def attempt_login(u,p):
    if u in USERS and USERS[u]["password"]==_hash(p):
        st.session_state.user_role=USERS[u]["role"]; st.session_state.username=u; return True
    return False

def logout():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

def login_page():
    st.markdown("""<div style="text-align:center;margin-top:3rem;">
      <div style="font-family:'Share Tech Mono';font-size:2.5rem;color:#00d4ff;text-shadow:0 0 20px rgba(0,212,255,.4);">🚑 ResQ-Path v7.0</div>
      <div style="color:#3a6a8a;font-family:'Share Tech Mono';margin-bottom:2rem;">REAL-TIME DYNAMIC GREEN CORRIDOR — BANGALORE</div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3=st.columns([1.5,1,1.5])
    with c2:
        u=st.text_input("Username",placeholder="driver1 / police1 / admin")
        p=st.text_input("Password",type="password")
        if st.button("🚀 ACCESS SYSTEM",use_container_width=True,type="primary"):
            if attempt_login(u,p): st.session_state.authenticated=True; st.rerun()
            else: st.error("❌ Invalid credentials")
        with st.expander("ℹ️ Demo credentials"):
            st.code("driver1 / driver123\npolice1 / police789\nadmin   / admin000")

if not st.session_state.authenticated:
    login_page(); st.stop()

# =============================================================================
# DATA
# =============================================================================
HOSPITALS = {
    "🩺 NIMHANS":{"loc":[12.9431,77.5910],"capacity":72,"specialty":"Neurology / Neuro-Surgery","routes":{
        "⚡ Main Road":{"path":[[12.9174,77.6238],[12.9250,77.6200],[12.9320,77.6100],[12.9400,77.5980],[12.9431,77.5910]],"base_traffic":42,"signals":5,"distance":5.2,"cross_traffic":"HIGH","speed_kmh":45},
        "🛣️ Outer Ring":{"path":[[12.9174,77.6238],[12.9150,77.6150],[12.9250,77.5950],[12.9350,77.5850],[12.9431,77.5910]],"base_traffic":78,"signals":7,"distance":6.8,"cross_traffic":"MEDIUM","speed_kmh":30},
        "🏗️ Service Lane":{"path":[[12.9174,77.6238],[12.9280,77.6300],[12.9360,77.6150],[12.9410,77.6020],[12.9431,77.5910]],"base_traffic":28,"signals":4,"distance":4.9,"cross_traffic":"LOW","speed_kmh":55}}},
    "🏥 St. Johns":{"loc":[12.9344,77.6121],"capacity":88,"specialty":"Cardiac / Trauma","routes":{
        "🛣️ 80ft Road":{"path":[[12.9174,77.6238],[12.9220,77.6220],[12.9280,77.6180],[12.9344,77.6121]],"base_traffic":35,"signals":3,"distance":2.8,"cross_traffic":"LOW","speed_kmh":50},
        "🌆 Sarjapur Rd":{"path":[[12.9174,77.6238],[12.9150,77.6280],[12.9250,77.6200],[12.9344,77.6121]],"base_traffic":62,"signals":4,"distance":3.4,"cross_traffic":"HIGH","speed_kmh":35}}},
    "🏨 Manipal Hospital":{"loc":[12.9553,77.6427],"capacity":65,"specialty":"Multi-Specialty / ICU","routes":{
        "🛣️ HAL Airport Rd":{"path":[[12.9174,77.6238],[12.9280,77.6280],[12.9380,77.6340],[12.9480,77.6400],[12.9553,77.6427]],"base_traffic":55,"signals":6,"distance":4.5,"cross_traffic":"MEDIUM","speed_kmh":40},
        "🌉 Old Airport Rd":{"path":[[12.9174,77.6238],[12.9200,77.6320],[12.9350,77.6380],[12.9450,77.6410],[12.9553,77.6427]],"base_traffic":40,"signals":5,"distance":4.1,"cross_traffic":"LOW","speed_kmh":52}}},
    "🏛️ Victoria Hospital":{"loc":[12.9658,77.5720],"capacity":91,"specialty":"Government / General Surgery","routes":{
        "🏙️ KR Road":{"path":[[12.9174,77.6238],[12.9350,77.6100],[12.9500,77.5900],[12.9600,77.5800],[12.9658,77.5720]],"base_traffic":70,"signals":8,"distance":7.2,"cross_traffic":"HIGH","speed_kmh":32},
        "🌿 Palace Road":{"path":[[12.9174,77.6238],[12.9300,77.6000],[12.9480,77.5820],[12.9580,77.5760],[12.9658,77.5720]],"base_traffic":45,"signals":6,"distance":6.5,"cross_traffic":"MEDIUM","speed_kmh":45}}},
    "🏥 Fortis Hospital":{"loc":[12.9279,77.6271],"capacity":78,"specialty":"Orthopedics / Trauma","routes":{
        "🚀 Bannerghatta Rd":{"path":[[12.9174,77.6238],[12.9200,77.6260],[12.9250,77.6265],[12.9279,77.6271]],"base_traffic":30,"signals":2,"distance":1.4,"cross_traffic":"LOW","speed_kmh":60}}},
}
AMBULANCES = {
    "🚑 A1-CARDIAC":  {"priority":10,"emergency":"Cardiac Arrest","color":"red",    "critical":True, "gps":[12.9174,77.6238]},
    "🚑 A2-TRAUMA":   {"priority":7, "emergency":"Road Trauma",   "color":"orange", "critical":False,"gps":[12.9150,77.6250]},
    "🚑 A3-FRACTURE": {"priority":4, "emergency":"Fracture",      "color":"gold",   "critical":False,"gps":[12.9200,77.6180]},
    "🚑 A4-STROKE":   {"priority":9, "emergency":"Stroke",        "color":"darkred","critical":True, "gps":[12.9180,77.6200]},
    "🚑 A5-BURNS":    {"priority":8, "emergency":"Severe Burns",  "color":"purple", "critical":True, "gps":[12.9190,77.6215]},
    "🚑 A6-MATERNITY":{"priority":6, "emergency":"Maternity",     "color":"pink",   "critical":False,"gps":[12.9160,77.6225]},
}
SURVIVAL = {
    "Cardiac Arrest":{"without":45,"with":82,"golden":4, "loss_per_min":10},
    "Stroke":        {"without":58,"with":78,"golden":60,"loss_per_min":2},
    "Road Trauma":   {"without":62,"with":82,"golden":30,"loss_per_min":3},
    "Severe Burns":  {"without":58,"with":75,"golden":45,"loss_per_min":2},
    "Maternity":     {"without":85,"with":94,"golden":60,"loss_per_min":1},
    "Fracture":      {"without":97,"with":99,"golden":120,"loss_per_min":0},
}

# =============================================================================
# SESSION STATE
# =============================================================================
DEFAULTS = {
    "step":0,"active":False,"auth":False,"live_gps":[12.9174,77.6238],
    "target_hospital":"🩺 NIMHANS","selected_route":"⚡ Main Road",
    "route_data":None,"dispatch_time":None,
    "active_ambulances":{},"amb_steps":{k:0 for k in AMBULANCES},
    "alerts":[],"mission_log":[],"signal_states":{},
    "traffic_tick":0,"live_traffic":{},"traffic_history":{},
    "signal_timers":{},"last_tick_time":None,
    "interpolated_gps":[12.9174,77.6238],"interp_progress":0.0,
    "mission_complete":False,"mission_stats":{},
    "last_signal_step":-1,"conflict_log":[],"audio_queue":[],
}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

def sg(k,d=None): return st.session_state.get(k,d)

# =============================================================================
# MATH
# =============================================================================
def haversine(la1,lo1,la2,lo2):
    R=6371; d1,d2=math.radians(la2-la1),math.radians(lo2-lo1)
    a=math.sin(d1/2)**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(d2/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

def interpolate_gps(p1,p2,t): return [p1[0]+(p2[0]-p1[0])*t,p1[1]+(p2[1]-p1[1])*t]
def seg_time(p1,p2,spd): return (haversine(p1[0],p1[1],p2[0],p2[1])/spd)*3600

def eta_to_signal(path,spd,cur,idx):
    if idx<=cur: return 0
    return sum(seg_time(path[i],path[i+1],spd) for i in range(cur,idx))

def best_route(hospital):
    routes=HOSPITALS[hospital]["routes"]; best,bs=None,float("inf")
    for rn,rd in routes.items():
        tf=rd["base_traffic"]/100*2.0
        cf={"HIGH":1.5,"MEDIUM":1.2,"LOW":1.0}.get(rd["cross_traffic"],1.2)
        sc=rd["distance"]*(1+tf)*cf+rd["signals"]*0.3
        if sc<bs: bs,best=sc,rn
    return best

def impact(rdata,emergency,step=0):
    dist,spd=rdata["distance"],rdata.get("speed_kmh",40)
    ne=(dist/20)*60; ce=(dist/spd)*60; saved=max(0,ne-ce)
    sv=SURVIVAL.get(emergency,SURVIVAL["Road Trauma"])
    return {"normal_eta":round(ne,1),"corridor_eta":round(ce,1),"time_saved":round(saved,1),
            "survival_with":sv["with"],"survival_without":sv["without"],"survival_gain":sv["with"]-sv["without"],
            "golden":sv["golden"],"golden_left":round(max(0,sv["golden"]-ce),1),
            "progress":round(step/max(len(rdata["path"])-1,1)*100)}

# =============================================================================
# REAL-TIME ENGINE
# =============================================================================
def update_live_traffic():
    st.session_state["traffic_tick"]+=1
    tick=st.session_state["traffic_tick"]
    if tick%3!=0: return
    for h,hdata in HOSPITALS.items():
        for r,rdata in hdata["routes"].items():
            key=f"{h}|{r}"; base=rdata["base_traffic"]
            new_val=max(5,min(98,base+random.gauss(0,8)+10*math.sin(tick/30)))
            old_val=st.session_state["live_traffic"].get(key,base)
            st.session_state["live_traffic"][key]=round(new_val,1)
            hist=st.session_state["traffic_history"].get(key,[])
            hist.append(round(old_val,1))
            if len(hist)>8: hist=hist[-8:]
            st.session_state["traffic_history"][key]=hist

def get_live_traffic(h,r):
    return st.session_state["live_traffic"].get(f"{h}|{r}",HOSPITALS[h]["routes"][r]["base_traffic"])

def traffic_arrow(h,r):
    hist=st.session_state["traffic_history"].get(f"{h}|{r}",[])
    if len(hist)<2: return "→"
    return "▲" if hist[-1]>hist[-2] else "▼"

def update_signal_timers(path,spd,cur,active):
    if not active: st.session_state["signal_timers"]={};return
    now=datetime.now(); last=st.session_state.get("last_tick_time")
    elapsed=(now-last).total_seconds() if last else 1.5
    st.session_state["last_tick_time"]=now
    timers=st.session_state.get("signal_timers",{})
    for idx in range(len(path)):
        key=f"sig_{idx}"
        if idx<cur: timers[key]=0
        elif idx==cur: timers[key]=max(0,timers.get(key,15)-elapsed)
        else:
            raw=eta_to_signal(path,spd,cur,idx)
            timers[key]=raw if key not in timers or timers[key]<=0 else max(0,timers[key]-elapsed)
    st.session_state["signal_timers"]=timers

def fmt_cd(s):
    if s<=0: return "NOW"
    m,sec=int(s//60),int(s%60)
    return f"{m}m {sec:02d}s" if m>0 else f"{sec}s"

def signal_phase(idx,cur,timers):
    secs=timers.get(f"sig_{idx}",999)
    if idx<cur:      return "green","✅ PASSED","—"
    if idx==cur:     return "green","🟢 GREEN NOW",f"{int(secs)}s left"
    if idx==cur+1:   return "green","🟢 PRE-CLEARED",fmt_cd(secs)
    if idx==cur+2:   return "yellow","🟡 PREPARING",fmt_cd(secs)
    return "hold","🚫 CROSS HOLD",fmt_cd(secs)

def update_interp_gps(path,spd,cur,active):
    if not active or cur>=len(path)-1:
        st.session_state["interpolated_gps"]=path[min(cur,len(path)-1)];st.session_state["interp_progress"]=0.0;return
    now=datetime.now(); last=st.session_state.get("last_tick_time",now)
    elapsed=min(2.0,(now-last).total_seconds())
    st_t=seg_time(path[cur],path[cur+1],spd)
    prog=st.session_state["interp_progress"]+elapsed/max(st_t,1)
    if prog>=1.0: prog=0.0
    st.session_state["interp_progress"]=prog
    st.session_state["interpolated_gps"]=interpolate_gps(path[cur],path[cur+1],prog)

# =============================================================================
# AUDIO
# =============================================================================
def play_audio(event):
    q=st.session_state.get("audio_queue",[])
    if event not in q: q.append(event)
    st.session_state["audio_queue"]=q

def render_audio_queue():
    import streamlit.components.v1 as components
    q = st.session_state.get("audio_queue", [])
    if not q: return
    calls = "\n".join([f"    {e}();" for e in q])
    html = f"""<script>
function playTone(freq,dur,type,vol){{
  try{{const ctx=new(window.AudioContext||window.webkitAudioContext)();
  const osc=ctx.createOscillator();const gain=ctx.createGain();
  osc.connect(gain);gain.connect(ctx.destination);
  osc.frequency.value=freq;osc.type=type||'sine';
  gain.gain.setValueAtTime(vol||0.3,ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+dur);
  osc.start();osc.stop(ctx.currentTime+dur);}}catch(e){{}}
}}
function playSignalGreen(){{playTone(880,.12,'sine',.25);setTimeout(()=>playTone(1100,.18,'sine',.3),130);}}
function playCorridorActivate(){{playTone(660,.1,'sine',.3);setTimeout(()=>playTone(880,.1,'sine',.3),120);setTimeout(()=>playTone(1100,.2,'sine',.35),240);}}
function playMissionComplete(){{[523,659,784,1047].forEach((f,i)=>setTimeout(()=>playTone(f,.25,'sine',.35),i*200));}}
function playConflict(){{playTone(220,.15,'sawtooth',.2);setTimeout(()=>playTone(180,.15,'sawtooth',.2),180);}}
function playReroute(){{playTone(660,.1,'square',.15);setTimeout(()=>playTone(440,.1,'square',.15),120);setTimeout(()=>playTone(550,.15,'square',.2),250);}}
{calls}
</script>"""
    components.html(html, height=0, scrolling=False)
    st.session_state["audio_queue"] = []

# =============================================================================
# CONFLICT RESOLUTION
# =============================================================================
def resolve_conflicts(active_ambulances):
    amb_list=list(active_ambulances.items())
    for i in range(len(amb_list)):
        for j in range(i+1,len(amb_list)):
            na,da=amb_list[i]; nb,db=amb_list[j]
            sa=sg("amb_steps",{}).get(na,0); sb=sg("amb_steps",{}).get(nb,0)
            pa=da["path"][min(sa,len(da["path"])-1)]; pb=db["path"][min(sb,len(db["path"])-1)]
            dist=haversine(pa[0],pa[1],pb[0],pb[1])
            if dist<0.5:
                pia=AMBULANCES.get(na,{}).get("priority",5); pib=AMBULANCES.get(nb,{}).get("priority",5)
                loser,winner,loser_data=(nb,na,db) if pia>=pib else (na,nb,da)
                hosp=loser_data["hospital"]; cur_r=loser_data["route"]
                alts=[r for r in HOSPITALS[hosp]["routes"] if r!=cur_r]
                if alts:
                    nr=alts[0]; nrd=HOSPITALS[hosp]["routes"][nr]
                    st.session_state["active_ambulances"][loser]["path"]=nrd["path"]
                    st.session_state["active_ambulances"][loser]["route"]=nr
                    st.session_state["amb_steps"][loser]=0
                    msg=f"⚠️ CONFLICT: {loser} rerouted to {nr} (yielded to {winner})"
                    st.session_state["conflict_log"].append({
                        "time":datetime.now().strftime("%H:%M:%S"),
                        "units":f"{winner} vs {loser}","winner":winner,"loser":loser,
                        "action":f"{loser} → {nr}","dist_m":round(dist*1000)})
                    st.session_state["alerts"].append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
                    play_audio("playConflict"); play_audio("playReroute")

# =============================================================================
# MISSION COMPLETE SCREEN
# =============================================================================
def show_mission_complete():
    stats=sg("mission_stats",{}); dispatch=sg("dispatch_time")
    total=round((datetime.now()-dispatch).total_seconds()/60,1) if dispatch else "—"
    st.markdown(f"""
    <div class="mission-complete">
      <div class="mission-title">✅ PATIENT DELIVERED</div>
      <div style="font-size:1.5rem;color:#00d4ff;font-family:'Share Tech Mono';margin-bottom:1.5rem;">CORRIDOR CLOSED — MISSION COMPLETE</div>
      <div style="font-family:'Share Tech Mono';font-size:1.4rem;color:#d0e8ff;margin:.4rem 0;">🏥 {stats.get('hospital','—')}</div>
      <div style="font-family:'Share Tech Mono';font-size:1rem;color:#3a6a8a;margin:.3rem 0;">🛣️ {stats.get('route','—')}</div>
      <div style="font-family:'Share Tech Mono';font-size:1rem;color:#d0e8ff;margin:.3rem 0;">⏱️ Mission Time: {total} min &nbsp;|&nbsp; ⚡ Time Saved: +{stats.get('time_saved','—')} min &nbsp;|&nbsp; 🚦 Signals: {stats.get('signals','—')}</div>
      <div style="margin-top:1.5rem;padding:1.2rem;background:rgba(0,255,136,.08);border-radius:10px;border:1px solid #00ff88;">
        <div style="font-family:'Share Tech Mono';font-size:2rem;color:#00ff88;">❤️ {stats.get('survival_with','—')}% SURVIVAL WITH CORRIDOR</div>
        <div style="color:#3a6a8a;font-family:'Share Tech Mono';margin-top:.4rem;">vs {stats.get('survival_without','—')}% without &nbsp;→&nbsp; +{stats.get('survival_gain','—')}% lives saved</div>
      </div>
    </div>""", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("🔄 NEW MISSION",use_container_width=True,type="primary"):
            for k in ["active","step","auth","mission_complete","mission_stats","interp_progress","signal_timers","last_tick_time","last_signal_step"]:
                st.session_state[k]=DEFAULTS.get(k,False)
            st.session_state["live_gps"]=[12.9174,77.6238]
            st.rerun()
    with c2:
        if st.button("📊 VIEW IMPACT",use_container_width=True):
            st.session_state["mission_complete"]=False; st.rerun()

# =============================================================================
# AUTO DEPLOY
# =============================================================================
def auto_deploy():
    for aname,adata in AMBULANCES.items():
        if adata["critical"] and aname not in sg("active_ambulances",{}):
            nh=min(HOSPITALS.keys(),key=lambda h:haversine(adata["gps"][0],adata["gps"][1],HOSPITALS[h]["loc"][0],HOSPITALS[h]["loc"][1]))
            rn=best_route(nh); rd=HOSPITALS[nh]["routes"][rn]
            st.session_state["active_ambulances"][aname]={"step":0,"path":rd["path"],"hospital":nh,"route":rn,"emergency":adata["emergency"],"speed_kmh":rd.get("speed_kmh",40),"interp":0.0}
            dist=haversine(adata["gps"][0],adata["gps"][1],HOSPITALS[nh]["loc"][0],HOSPITALS[nh]["loc"][1])
            st.session_state["alerts"].append(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 AUTO-DEPLOY: {aname} ({adata['emergency']}) → {nh} ({dist:.1f}km)")

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(f"""<div style="text-align:center;padding:.8rem 0;">
      <div style="font-family:'Share Tech Mono';font-size:1.3rem;color:#00d4ff;">🚑 ResQ-Path v7</div>
      <div style="color:#3a6a8a;font-size:.72rem;font-family:'Share Tech Mono';">REAL-TIME GREEN CORRIDOR</div></div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**👤 {USERS[sg('username')]['name']}**")
    st.markdown(f"**🔐 `{sg('user_role','').upper()}`**")
    st.markdown(f"**🕐 {datetime.now().strftime('%H:%M:%S')}**")
    st.markdown("---")
    st.markdown(f"🚑 Active: **`{len(sg('active_ambulances',{}))}`**")
    st.markdown(f"🚨 Alerts: **`{len(sg('alerts',[]))}`**")
    st.markdown(f"⚠️ Conflicts: **`{len(sg('conflict_log',[]))}`**")
    st.markdown("---")
    if st.button("🚪 LOGOUT",use_container_width=True): logout()

# =============================================================================
# HEADER
# =============================================================================
st.markdown(f"""
<div class="resq-header">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div class="resq-title">🚑 ResQ-Path — Real-Time Dynamic Green Corridor</div>
      <div class="resq-sub">BANGALORE · V2I SIGNAL COORDINATION · LIVE GPS · AUDIO ALERTS · CONFLICT RESOLUTION</div>
    </div>
    <div style="text-align:right;font-family:'Share Tech Mono';font-size:.78rem;color:#3a6a8a;">
      <div style="color:#00ff88;">● SYSTEM ONLINE</div>
      <div>{len(HOSPITALS)} HOSPITALS · {sum(len(h['routes']) for h in HOSPITALS.values())} ROUTES</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# Mission complete full screen
if sg("mission_complete"):
    show_mission_complete(); render_audio_queue(); st.stop()

# =============================================================================
# TABS
# =============================================================================
show_driver=sg("user_role") in ["driver","admin"]
show_police=sg("user_role") in ["police","admin"]

if show_driver and show_police:
    tabs=st.tabs(["🚑 DRIVER","🚦 SIGNAL CORRIDOR","📡 LIVE TRAFFIC","📊 IMPACT","👮 POLICE","⚠️ CONFLICTS","🚨 ALERTS"])
    tab_driver,tab_signals,tab_traffic,tab_impact,tab_police,tab_conflicts,tab_alerts=tabs
elif show_driver:
    tabs=st.tabs(["🚑 DRIVER","🚦 SIGNAL CORRIDOR","📡 LIVE TRAFFIC","📊 IMPACT","⚠️ CONFLICTS"])
    tab_driver,tab_signals,tab_traffic,tab_impact,tab_conflicts=tabs
    tab_police=tab_alerts=None
else:
    tabs=st.tabs(["👮 POLICE","⚠️ CONFLICTS","🚨 ALERTS"])
    tab_police,tab_conflicts,tab_alerts=tabs
    tab_driver=tab_signals=tab_traffic=tab_impact=None

# =============================================================================
# TAB: DRIVER
# =============================================================================
if tab_driver:
  with tab_driver:
    st.markdown("### 🛰️ Live GPS + Route Control")
    c1,c2,c3,c4=st.columns(4)
    with c1: lat=st.number_input("📍 Latitude",value=sg("live_gps")[0],min_value=12.85,max_value=13.10,step=0.0001,format="%.4f")
    with c2: lon=st.number_input("📍 Longitude",value=sg("live_gps")[1],min_value=77.50,max_value=77.75,step=0.0001,format="%.4f")
    with c3:
        if st.button("🛰️ GPS PING",use_container_width=True):
            st.session_state["live_gps"]=[lat+random.gauss(0,.0001),lon+random.gauss(0,.0001)]; st.rerun()
    st.session_state["live_gps"]=[lat,lon]
    with c4:
        dists={h:haversine(lat,lon,HOSPITALS[h]["loc"][0],HOSPITALS[h]["loc"][1]) for h in HOSPITALS}
        nearest=min(dists,key=dists.get)
        st.metric("📏 Nearest",f"{dists[nearest]:.1f} km",nearest[:14])

    ch,cr=st.columns(2)
    with ch:
        hosp=st.selectbox("🏥 Target Hospital",list(HOSPITALS.keys()),key="hosp_sel")
        st.session_state["target_hospital"]=hosp
    with cr:
        rec=best_route(hosp)
        route=st.selectbox("🛣️ Route",list(HOSPITALS[hosp]["routes"].keys()),key="route_sel")
        st.session_state["selected_route"]=route

    rdata={**HOSPITALS[hosp]["routes"][route]}
    st.session_state["route_data"]=rdata
    lt=get_live_traffic(hosp,route)

    if rec!=route:
        st.markdown(f'<div class="alert-b">💡 AI Recommends: <b>{rec}</b> — Live Traffic: {get_live_traffic(hosp,rec):.0f}%</div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-g">✅ Optimal route — Live Traffic: {lt:.0f}%</div>',unsafe_allow_html=True)

    ca,cd,cs=st.columns(3)
    with ca:
        if not sg("auth"):
            if st.button("🔓 AUTHENTICATE V2I",use_container_width=True,type="primary"):
                st.session_state["auth"]=True
                st.session_state["alerts"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ V2I Auth success")
                st.rerun()
        else: st.markdown('<div class="alert-g">✅ V2I AUTHENTICATED</div>',unsafe_allow_html=True)

    with cd:
        if sg("auth") and not sg("active"):
            if st.button("🚀 ACTIVATE GREEN CORRIDOR",use_container_width=True,type="primary"):
                st.session_state.update({"active":True,"step":0,"dispatch_time":datetime.now(),
                    "interp_progress":0.0,"last_tick_time":datetime.now(),"signal_timers":{},"last_signal_step":-1})
                st.session_state["alerts"].append(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 CORRIDOR ACTIVATED → {hosp} via {route}")
                play_audio("playCorridorActivate"); st.rerun()
        elif sg("active"): st.markdown('<div class="alert-r">🟢 CORRIDOR ACTIVE</div>',unsafe_allow_html=True)

    with cs:
        if st.button("🛑 STOP/RESET",use_container_width=True):
            for k in ["active","step","auth","interp_progress","signal_timers","last_tick_time","mission_complete","last_signal_step"]:
                st.session_state[k]=DEFAULTS.get(k,False)
            st.rerun()

    step=sg("step",0); imp=impact(rdata,"Cardiac Arrest",step)
    path=rdata["path"]; timers=sg("signal_timers",{})
    nsi=min(step+1,len(path)-1); nss=timers.get(f"sig_{nsi}",0)
    cd_class="green" if nss>20 else ("yellow" if nss>8 else "red")

    st.markdown("---")
    if sg("active"):
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 2fr 1fr;gap:12px;margin:.5rem 0 1rem;">
          <div class="mc"><div class="mv mvo">{imp['corridor_eta']}m</div><div class="ml">ETA with corridor</div><div class="md" style="color:#3a6a8a;">vs {imp['normal_eta']}m normal</div></div>
          <div class="countdown-big {cd_class}">⏱ {fmt_cd(nss)}<br><span style="font-size:.9rem;">Next signal S{nsi+1} pre-clears</span></div>
          <div class="mc crit"><div class="mv mvg">+{imp['survival_gain']}%</div><div class="ml">Survival gain</div><div class="md" style="color:#3a6a8a;">{imp['survival_with']}% vs {imp['survival_without']}%</div></div>
        </div>""",unsafe_allow_html=True)
        prog=imp["progress"]
        st.markdown(f"""<div class="prog-wrap">
          <div style="display:flex;justify-content:space-between;font-family:'Share Tech Mono';font-size:.8rem;">
            <span style="color:#00d4ff;">🟢 CORRIDOR PROGRESS</span>
            <span style="color:#00ff88;">{prog}% — Waypoint {step+1}/{len(path)}</span></div>
          <div class="prog-bar"><div class="prog-fill" style="width:{prog}%"></div></div></div>""",unsafe_allow_html=True)
    else:
        m1,m2,m3,m4,m5=st.columns(5)
        with m1: st.metric("⏱️ ETA",f"{imp['corridor_eta']}m",f"vs {imp['normal_eta']}m")
        with m2: st.metric("⚡ Saved",f"+{imp['time_saved']}m")
        with m3: st.metric("❤️ Survival",f"+{imp['survival_gain']}%")
        with m4: st.metric("⏰ Window",f"{imp['golden_left']}m")
        with m5: st.metric("🚦 Signals",rdata["signals"])

    # MAP — auto-zooms to ambulance when active
    st.markdown("### 🗺️ Live Corridor Map")
    display_gps=sg("interpolated_gps",sg("live_gps"))
    zoom=15 if sg("active") else 14
    m=folium.Map(location=display_gps,zoom_start=zoom,tiles="CartoDB dark_matter")

    folium.Marker(display_gps,popup=f"🚑 A1-LIVE | {display_gps[0]:.5f},{display_gps[1]:.5f}",
        tooltip="🚑 Ambulance — LIVE GPS",icon=folium.Icon(color="blue",icon="ambulance",prefix="fa")).add_to(m)

    for hname,hdata in HOSPITALS.items():
        is_t=hname==hosp
        folium.Marker(hdata["loc"],popup=f"{hname}\n{hdata['specialty']}",tooltip=hname,
            icon=folium.Icon(color="red" if is_t else "gray",icon="plus-square",prefix="fa")).add_to(m)
        if is_t: folium.Circle(hdata["loc"],radius=200,color="#ff4444",fill=True,fillOpacity=0.1).add_to(m)

    folium.PolyLine(path,color="#00ff88" if sg("active") else "#00d4ff",weight=8,opacity=0.9).add_to(m)

    cur_step=min(step,len(path)-1)
    cmap={"green":"#00ff88","yellow":"#ffaa00","red":"#ff4444","hold":"#ff6600"}
    for i,node in enumerate(path):
        css,label,cd_str=signal_phase(i,cur_step,timers)
        fc=cmap.get(css,"#444")
        cross="🚫 CROSS HELD" if i<=cur_step+1 and sg("active") else "Normal"
        folium.CircleMarker(node,radius=18 if i==cur_step else 13,color=fc,fill=True,fillColor=fc,fillOpacity=0.85,
            popup=f"S{i+1}: {label}\nETA: {cd_str}\n{cross}",tooltip=f"S{i+1}: {label} | {cd_str}").add_to(m)
        folium.Marker(node,icon=folium.DivIcon(
            html=f'<div style="font-family:monospace;font-size:11px;color:white;font-weight:bold;text-shadow:1px 1px 2px black;margin-left:-8px;">S{i+1}</div>',
            icon_size=(22,16))).add_to(m)

    st_folium(m,width=1100,height=520,key=f"dmap_{cur_step}_{sg('active')}_{hosp}_{route}")

# =============================================================================
# TAB: SIGNAL CORRIDOR
# =============================================================================
if tab_signals:
  with tab_signals:
    st.markdown("### 🚦 Real-Time Signal Countdown Matrix")
    st.markdown('<div class="alert-b">🧠 Each timer shows exact seconds until that signal clears. Pre-clearance 2 signals ahead. Cross-traffic held simultaneously.</div>',unsafe_allow_html=True)
    rd=sg("route_data") or list(HOSPITALS["🩺 NIMHANS"]["routes"].values())[0]
    path=rd["path"]; spd=rd.get("speed_kmh",40)
    cur=min(sg("step",0),len(path)-1); timers=sg("signal_timers",{}); is_active=sg("active",False)
    cols=st.columns(len(path))
    for i,node in enumerate(path):
        css,label,cd_str=signal_phase(i,cur,timers)
        with cols[i]:
            st.markdown(f"""<div class="sig {css}" style="padding:16px 8px;">
              <div style="font-size:1.2rem;margin-bottom:6px;">S{i+1}</div>
              <div style="font-size:.8rem;margin-bottom:8px;">{label if is_active else '🔴 INACTIVE'}</div>
              <div style="font-size:1.4rem;font-weight:bold;">{cd_str if is_active else '—'}</div>
              <div style="font-size:.65rem;margin-top:6px;opacity:.8;">{'🚫 CROSS HELD' if i<=cur+1 and is_active else 'Normal'}</div>
            </div>""",unsafe_allow_html=True)
    if not is_active: st.markdown('<div class="alert-b">⚡ Activate corridor in Driver tab to see live countdowns</div>',unsafe_allow_html=True)
    st.markdown("---")
    rows=[]
    for i,node in enumerate(path):
        raw=eta_to_signal(path,spd,cur,i) if is_active else 0
        css,label,cd_str=signal_phase(i,cur,timers)
        rows.append({"Signal":f"S{i+1}","Coordinates":f"{node[0]:.4f},{node[1]:.4f}",
                     "ETA":f"{int(raw//60)}m {int(raw%60)}s" if is_active and raw>0 else "—",
                     "Countdown":cd_str if is_active else "inactive",
                     "Status":label if is_active else "STANDBY",
                     "Cross-Traffic":"🚫 HELD" if i<=cur+1 and is_active else "Normal"})
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# =============================================================================
# TAB: LIVE TRAFFIC
# =============================================================================
if tab_traffic:
  with tab_traffic:
    st.markdown("### 📡 Live Traffic Monitor")
    st.markdown(f"**Last update:** `{datetime.now().strftime('%H:%M:%S')}` | **Tick:** `{sg('traffic_tick',0)}`")
    for hname,hdata in HOSPITALS.items():
        st.markdown(f"**{hname}** — {hdata['specialty']}")
        rcols=st.columns(len(hdata["routes"]))
        for j,(rname,rdata) in enumerate(hdata["routes"].items()):
            lt=get_live_traffic(hname,rname); trend=traffic_arrow(hname,rname)
            col='#00ff88' if lt<40 else ('#ffaa00' if lt<70 else '#ff4444')
            with rcols[j]:
                st.markdown(f"""<div class="mc" style="padding:.9rem;">
                  <div style="font-size:.78rem;color:#3a6a8a;margin-bottom:4px;">{rname}</div>
                  <div style="font-family:'Share Tech Mono';font-size:1.6rem;color:{col};">{lt:.0f}% {trend}</div>
                  <div style="font-size:.72rem;margin-top:4px;color:#3a6a8a;">{rdata['signals']} signals · {rdata['distance']}km · {rdata['speed_kmh']}km/h</div>
                </div>""",unsafe_allow_html=True)
        st.markdown("")

# =============================================================================
# TAB: IMPACT
# =============================================================================
if tab_impact:
  with tab_impact:
    st.markdown("### 📊 Real-World Impact Analysis")
    em=st.selectbox("Emergency Type",list(SURVIVAL.keys()),key="em_sel")
    hs=st.selectbox("Hospital",list(HOSPITALS.keys()),key="h_sel_i")
    rs=st.selectbox("Route",list(HOSPITALS[hs]["routes"].keys()),key="r_sel_i")
    rdi=HOSPITALS[hs]["routes"][rs]; impi=impact(rdi,em); sv=SURVIVAL[em]
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f"""<div class="mc" style="padding:1.5rem;text-align:left;">
          <div style="color:#00d4ff;font-family:'Share Tech Mono';font-size:1rem;margin-bottom:1rem;">⏱ Time Analysis</div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a3a5c;"><span style="color:#3a6a8a;">Normal ETA</span><span style="font-family:'Share Tech Mono';color:#ff4444;">{impi['normal_eta']} min</span></div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a3a5c;"><span style="color:#3a6a8a;">With Corridor</span><span style="font-family:'Share Tech Mono';color:#00ff88;">{impi['corridor_eta']} min</span></div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a3a5c;"><span style="color:#3a6a8a;">Time Saved</span><span style="font-family:'Share Tech Mono';color:#00ff88;">+{impi['time_saved']} min</span></div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;"><span style="color:#3a6a8a;">Golden Window Left</span><span style="font-family:'Share Tech Mono';color:{'#00ff88' if impi['golden_left']>5 else '#ff4444'};">{impi['golden_left']} min</span></div>
        </div>""",unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="mc" style="padding:1.5rem;text-align:left;">
          <div style="color:#00d4ff;font-family:'Share Tech Mono';font-size:1rem;margin-bottom:1rem;">❤️ Survival Probability</div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a3a5c;"><span style="color:#3a6a8a;">Without corridor</span><span style="font-family:'Share Tech Mono';color:#ff4444;">{sv['without']}%</span></div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a3a5c;"><span style="color:#3a6a8a;">With corridor</span><span style="font-family:'Share Tech Mono';color:#00ff88;">{sv['with']}%</span></div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a3a5c;"><span style="color:#3a6a8a;">Survival Gain</span><span style="font-family:'Share Tech Mono';color:#00ff88;">+{impi['survival_gain']}%</span></div>
          <div style="display:flex;justify-content:space-between;padding:7px 0;"><span style="color:#3a6a8a;">Loss/min delay</span><span style="font-family:'Share Tech Mono';color:#ffaa00;">-{sv['loss_per_min']}%/min</span></div>
        </div>""",unsafe_allow_html=True)
    st.markdown("---")
    rows=[{"Emergency":et,"Golden":f"{ed['golden']}m","Without":f"{ed['without']}%","With":f"{ed['with']}%",
           "Gain":f"+{ed['with']-ed['without']}%","Loss/Min":f"-{ed['loss_per_min']}%/min"} for et,ed in SURVIVAL.items()]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    st.markdown("---")
    saved=impi["time_saved"]; sigs=rdi["signals"]
    ci1,ci2,ci3=st.columns(3)
    with ci1: st.markdown(f"""<div class="mc" style="text-align:left;padding:1.2rem;"><div style="color:#00d4ff;margin-bottom:.5rem;font-family:'Share Tech Mono';">📊 Bangalore Stats</div><div style="font-size:.85rem;line-height:2;">~850 calls/day<br>+{saved:.1f} min saved each<br><b style="color:#00ff88;">~{int(850*saved/60)} hours saved daily</b></div></div>""",unsafe_allow_html=True)
    with ci2: st.markdown(f"""<div class="mc" style="text-align:left;padding:1.2rem;"><div style="color:#00d4ff;margin-bottom:.5rem;font-family:'Share Tech Mono';">💓 Lives Impacted</div><div style="font-size:.85rem;line-height:2;">1 cardiac life per 6 min<br>+{max(1,int(saved/6))} lives/day<br><b style="color:#00ff88;">~{max(30,int(saved/6*365))} lives/year</b></div></div>""",unsafe_allow_html=True)
    with ci3: st.markdown(f"""<div class="mc" style="text-align:left;padding:1.2rem;"><div style="color:#00d4ff;margin-bottom:.5rem;font-family:'Share Tech Mono';">🚦 Signal Overhead</div><div style="font-size:.85rem;line-height:2;">{sigs} signals/corridor<br>~45s hold each<br><b style="color:#00ff88;">Only {sigs*45}s disruption</b></div></div>""",unsafe_allow_html=True)

# =============================================================================
# TAB: POLICE
# =============================================================================
if tab_police:
  with tab_police:
    st.markdown("### 👮 Police Command")
    aas=sg("active_ambulances",{})
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("🚨 Critical",sum(1 for a in aas if AMBULANCES.get(a,{}).get("critical")))
    with c2: st.metric("🚑 Corridors",len(aas))
    with c3: st.metric("🚦 Signals",sum(len(d["path"]) for d in aas.values()))
    with c4: st.metric("⚠️ Conflicts",len(sg("conflict_log",[])))
    st.markdown("#### 🚀 Manual Deploy")
    dc1,dc2,dc3=st.columns(3)
    with dc1: sel_amb=st.selectbox("Ambulance",list(AMBULANCES.keys()),key="p_amb")
    with dc2: sel_hosp_p=st.selectbox("Hospital",list(HOSPITALS.keys()),key="p_hosp")
    with dc3:
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("🚀 DEPLOY",use_container_width=True,type="primary"):
            rn=best_route(sel_hosp_p); rdp=HOSPITALS[sel_hosp_p]["routes"][rn]
            st.session_state["active_ambulances"][sel_amb]={"step":0,"path":rdp["path"],"hospital":sel_hosp_p,"route":rn,"emergency":AMBULANCES[sel_amb]["emergency"],"speed_kmh":rdp.get("speed_kmh",40),"interp":0.0}
            play_audio("playCorridorActivate"); st.success(f"✅ {sel_amb} → {sel_hosp_p}"); st.rerun()
    mp=folium.Map(location=[12.93,77.61],zoom_start=13,tiles="CartoDB dark_matter")
    for hn,hd in HOSPITALS.items(): folium.Marker(hd["loc"],popup=hn,icon=folium.Icon(color="red",icon="plus-square",prefix="fa")).add_to(mp)
    for an,ad in aas.items():
        p=ad["path"]; color=AMBULANCES.get(an,{}).get("color","blue")
        folium.PolyLine(p,color=color,weight=8).add_to(mp)
        pos=p[min(sg("amb_steps",{}).get(an,0),len(p)-1)]
        folium.Marker(pos,popup=f"{an}",icon=folium.Icon(color="blue",icon="ambulance",prefix="fa")).add_to(mp)
    st_folium(mp,width=1100,height=500,key="police_map_v7")
    rows=[{"Unit":an,"Emergency":ad["emergency"],"Priority":ad["priority"],"Critical":"⚠️ YES" if ad["critical"] else "—",
           "Status":"🟢 DEPLOYED" if an in aas else "🔴 STANDBY","GPS":f"{ad['gps'][0]:.4f},{ad['gps'][1]:.4f}",
           "Step":sg("amb_steps",{}).get(an,0) if an in aas else "—"} for an,ad in AMBULANCES.items()]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# =============================================================================
# TAB: CONFLICTS
# =============================================================================
if tab_conflicts:
  with tab_conflicts:
    st.markdown("### ⚠️ Conflict Resolution Log")
    st.markdown("""<div class="alert-b">🧠 When two ambulances are within 500m on overlapping routes, the lower priority unit is automatically rerouted. Priority = emergency severity score.</div>""",unsafe_allow_html=True)
    conflicts=sg("conflict_log",[])
    if not conflicts: st.markdown('<div class="alert-g">✅ No conflicts — All corridors clear</div>',unsafe_allow_html=True)
    else:
        for c in reversed(conflicts[-10:]):
            st.markdown(f"""<div class="conflict-resolved">
              <b>[{c['time']}]</b> ⚠️ Conflict: {c['units']}<br>
              🏆 <b>{c['winner']}</b> retained corridor &nbsp;|&nbsp; 🔄 <b>{c['loser']}</b> auto-rerouted → {c['action']}<br>
              📏 Distance at conflict: {c['dist_m']}m
            </div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🧠 Priority Matrix")
    rows=[{"Unit":an,"Emergency":ad["emergency"],"Priority Score":ad["priority"],
           "Corridor Rights":"🥇 HIGHEST" if ad["priority"]==10 else ("🥈 HIGH" if ad["priority"]>=8 else ("🥉 MEDIUM" if ad["priority"]>=6 else "⬇️ LOW"))}
          for an,ad in AMBULANCES.items()]
    st.dataframe(pd.DataFrame(rows).sort_values("Priority Score",ascending=False),use_container_width=True,hide_index=True)
    st.markdown("---")
    st.markdown("#### 🧪 Test Conflict Resolution")
    if st.button("🧪 SIMULATE CONFLICT",use_container_width=True):
        rds=HOSPITALS["🩺 NIMHANS"]["routes"]["⚡ Main Road"]
        for an in ["🚑 A2-TRAUMA","🚑 A4-STROKE"]:
            st.session_state["active_ambulances"][an]={"step":2,"path":rds["path"],"hospital":"🩺 NIMHANS","route":"⚡ Main Road","emergency":AMBULANCES[an]["emergency"],"speed_kmh":40,"interp":0.0}
            st.session_state["amb_steps"][an]=2
        st.success("✅ Conflict scenario loaded — watch it resolve automatically"); st.rerun()

# =============================================================================
# TAB: ALERTS
# =============================================================================
if tab_alerts:
  with tab_alerts:
    st.markdown("### 🚨 Live Alert Feed")
    ca,cb=st.columns([3,1])
    with cb:
        if st.button("🗑️ Clear",use_container_width=True):
            st.session_state["alerts"]=[]; st.rerun()
    alerts=sg("alerts",[])
    if not alerts: st.markdown('<div class="alert-g">✅ No alerts</div>',unsafe_allow_html=True)
    else:
        for alert in reversed(alerts[-20:]):
            css="alert-r" if ("🚨" in alert or "⚠️" in alert) else ("alert-g" if ("✅" in alert or "🟢" in alert) else "alert-b")
            st.markdown(f'<div class="{css}">{alert}</div>',unsafe_allow_html=True)
    st.markdown("---")
    h1,h2,h3,h4=st.columns(4)
    with h1: st.metric("V2I Link","🟢 ONLINE")
    with h2: st.metric("GPS Feed","🟢 ACTIVE")
    with h3: st.metric("Signals","🟢 ALL UP")
    with h4: st.metric("Hospitals",f"🟢 {len(HOSPITALS)}/{len(HOSPITALS)}")

# =============================================================================
# REAL-TIME ENGINE
# =============================================================================
update_live_traffic()
rd_now=sg("route_data")

if rd_now and sg("active"):
    pn=rd_now["path"]; sn=rd_now.get("speed_kmh",40); stn=sg("step",0)
    update_signal_timers(pn,sn,stn,True)
    update_interp_gps(pn,sn,stn,True)
    # Audio: beep when signal step advances
    last_sig=sg("last_signal_step",-1)
    if stn>last_sig and stn>0:
        play_audio("playSignalGreen")
        st.session_state["last_signal_step"]=stn

if sg("traffic_tick",0)==6: auto_deploy()
if sg("traffic_tick",0)%5==0 and sg("active_ambulances"): resolve_conflicts(sg("active_ambulances",{}))

# Driver waypoint advance
if sg("active") and rd_now:
    pa=rd_now["path"]; cs=sg("step",0)
    if cs<len(pa)-1:
        time.sleep(3)
        st.session_state["step"]=cs+1
        st.session_state["live_gps"]=pa[st.session_state["step"]]
        st.session_state["interp_progress"]=0.0
        st.session_state["last_tick_time"]=datetime.now()
        st.rerun()
    else:
        impf=impact(rd_now,"Cardiac Arrest",len(pa)-1)
        st.session_state.update({"mission_complete":True,"active":False,"mission_stats":{
            "hospital":sg("target_hospital","Hospital"),"route":sg("selected_route","—"),
            "time_saved":impf["time_saved"],"signals":rd_now["signals"],
            "survival_with":impf["survival_with"],"survival_without":impf["survival_without"],
            "survival_gain":impf["survival_gain"]}})
        play_audio("playMissionComplete"); st.rerun()

# Multi-ambulance advance
for an in list(sg("active_ambulances",{}).keys()):
    cs=sg("amb_steps",{}).get(an,0); ap=sg("active_ambulances",{})[an]["path"]
    if cs<len(ap)-1:
        time.sleep(3); st.session_state["amb_steps"][an]=cs+1; st.rerun(); break

render_audio_queue()

st.markdown("---")
st.markdown("""<div style="text-align:center;font-family:'Share Tech Mono';font-size:.72rem;color:#1a3a5c;padding:.8rem 0;">
🚑 ResQ-Path v7.0 — Audio Alerts · Auto-Zoom · Mission Complete · Conflict Resolution | Bangalore Emergency Response
</div>""",unsafe_allow_html=True)