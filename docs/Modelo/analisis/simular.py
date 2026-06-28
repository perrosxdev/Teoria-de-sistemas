import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import os, json

OUT = r"C:\Users\corte\Desktop\tsistemas\analisis"
os.makedirs(OUT, exist_ok=True)

# ── Estilo general ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0f1117",
    "axes.facecolor":   "#1a1d27",
    "axes.edgecolor":   "#3a3d4d",
    "axes.labelcolor":  "#c8ccd8",
    "xtick.color":      "#8b8fa8",
    "ytick.color":      "#8b8fa8",
    "grid.color":       "#2a2d3d",
    "grid.linestyle":   "--",
    "grid.alpha":       0.6,
    "text.color":       "#c8ccd8",
    "font.family":      "DejaVu Sans",
    "font.size":        10,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.titlecolor":  "#e8ecf4",
    "legend.facecolor": "#1a1d27",
    "legend.edgecolor": "#3a3d4d",
    "legend.fontsize":  9,
    "figure.dpi":       150,
})

COLORES = {
    0: "#f97316",   # naranja  – sin inversión
    1: "#60a5fa",   # azul     – reactivo
    2: "#34d399",   # verde    – proactivo
}
LABELS = {0: "Escenario 0 – Sin inversión", 1: "Escenario 1 – Reactivo", 2: "Escenario 2 – Proactivo"}

# ── Lookups ────────────────────────────────────────────────────────────────────
_est = {0:1.84,1:1.81,2:0.84,3:0.78,4:0.90,5:0.75,6:0.84,7:0.67,8:0.69,9:0.91,10:0.71,11:1.27}
def estacionalidad(t):    return _est[int(t) % 12]
def disp_proveedor(t):    return 0.8 if int(t) % 12 in (0, 1) else 1.0
_fx = [0, 0.1, 0.3, 0.5, 0.7, 1.0]
_fy = [0, 0.02, 0.1, 0.25, 0.3, 0.32]
def fuga_lookup(x):       return float(np.interp(x, _fx, _fy))

# ── Parámetros ─────────────────────────────────────────────────────────────────
MP   = 1200;   TCB  = 0.02;   PV   = 33000; PC   = 24000
CVR  = 500;    CFM  = 200;    CV   = 50_000_000
ICLP = 4.328e-5; DM  = 200;   DMC  = 700
CMP  = 1500;   CBS  = 867;    MEC  = 8

# ── Simulación (Euler, dt=1) ───────────────────────────────────────────────────
def simular(politica):
    N = 97  # t = 0..96
    DB=700.; SH=750.; CR=720.; VC=0.; MA=12e6; BAC=0.
    r = {k: np.zeros(N) for k in [
        "DB","SH","CR","VC","MA","BAC","DT","TD","TI",
        "TC","TP","TCompra","INV","ROI","CamUso","CapAtrib","DispAtrib","BNeto"
    ]}
    t_compra = None

    for i in range(N):
        t = float(i)
        est  = estacionalidad(t);  disp = disp_proveedor(t)
        DT_  = DB * est
        inv_obj = 2000. if VC >= 1 else 850.
        necesidad = max(0., inv_obj - SH)
        tcompra   = min(necesidad, disp * CMP)
        tdesp     = min(CR, min(DT_, SH))        # paso_tiempo = 1
        ti        = max(0., (DT_ - tdesp) / DT_) if DT_ > 0 else 0.
        fuga      = fuga_lookup(ti)
        frac_disp = max(0., MP - DB) / MP
        tcapt     = DB * TCB * frac_disp
        tperd     = DB * fuga if DB > DM else 0.

        g_pro = 1 if t >= MEC else 0
        g_rea = 1 if (MA > CV and ti > 0.1) else 0
        g_act = g_pro if politica==2 else (g_rea if politica==1 else 0)
        pulso = (1. if g_act==1 and VC < 1 else 0.)
        if pulso and t_compra is None: t_compra = i
        inversion = pulso * CV

        cam_uso  = 1 if (VC >= 1 and DT_ >= DMC) else 0
        cap_atr  = max(0., CR - CBS)
        disp_atr = min(tdesp, cap_atr) if cam_uso else 0.
        mant      = cam_uso * cap_atr * CFM
        bbruto    = disp_atr * (PV - PC - CVR)
        bneto     = bbruto - mant
        ingresos  = tdesp * PV
        costo_c   = tcompra * PC
        cos_fij   = 700_000 + mant
        cos_op    = cos_fij + tdesp * CVR
        roi       = BAC / CV if VC >= 1 else 0.

        r["DB"][i]=DB; r["SH"][i]=SH; r["CR"][i]=CR; r["VC"][i]=VC
        r["MA"][i]=MA; r["BAC"][i]=BAC; r["DT"][i]=DT_; r["TD"][i]=tdesp
        r["TI"][i]=ti; r["TC"][i]=tcapt; r["TP"][i]=tperd; r["TCompra"][i]=tcompra
        r["INV"][i]=inversion; r["ROI"][i]=roi; r["CamUso"][i]=cam_uso
        r["CapAtrib"][i]=cap_atr; r["DispAtrib"][i]=disp_atr; r["BNeto"][i]=bneto

        DB  += (tcapt - tperd)
        SH  += (tcompra - tdesp)
        CR  += inversion * ICLP
        VC  += pulso
        MA  += ingresos - costo_c - cos_op - inversion
        BAC += bneto

    return r, t_compra

esc = {}
t_compras = {}
for p in [0, 1, 2]:
    esc[p], t_compras[p] = simular(p)

T = np.arange(97)

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 1 — Demanda Base por escenario
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [0,1,2]:
    ax.plot(T, esc[p]["DB"], color=COLORES[p], lw=2, label=LABELS[p])
for p in [1,2]:
    if t_compras[p]:
        ax.axvline(t_compras[p], color=COLORES[p], lw=1, ls=":", alpha=0.7)
        ax.text(t_compras[p]+0.5, ax.get_ylim()[0]+5, f"Compra E{p}\nmes {t_compras[p]}", color=COLORES[p], fontsize=7)
ax.axhline(MP, color="#a78bfa", lw=1, ls="--", alpha=0.5, label="Mercado potencial (1200)")
ax.set_title("Demanda Base por Escenario (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Demanda Base (Caja/mes)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "01_demanda_base.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 2 — Tasa de incumplimiento por escenario
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [0,1,2]:
    ax.plot(T, esc[p]["TI"]*100, color=COLORES[p], lw=2, label=LABELS[p])
ax.axhline(10, color="#f43f5e", lw=1, ls="--", alpha=0.6, label="Umbral reactivo (10%)")
for p in [1,2]:
    if t_compras[p]:
        ax.axvline(t_compras[p], color=COLORES[p], lw=1, ls=":", alpha=0.7)
ax.set_title("Tasa de Incumplimiento por Escenario (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Incumplimiento (%)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "02_tasa_incumplimiento.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 3 — Margen acumulado por escenario
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [0,1,2]:
    ax.plot(T, esc[p]["MA"]/1e6, color=COLORES[p], lw=2, label=LABELS[p])
ax.axhline(50, color="#facc15", lw=1, ls="--", alpha=0.6, label="Umbral gatillo reactivo (50 M CLP)")
for p in [1,2]:
    if t_compras[p]:
        ax.axvline(t_compras[p], color=COLORES[p], lw=1, ls=":", alpha=0.7)
ax.set_title("Margen Acumulado por Escenario (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Margen acumulado (M CLP)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.0f} M"))
plt.tight_layout()
plt.savefig(os.path.join(OUT, "03_margen_acumulado.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 4 — Capacidad de Reparto por escenario
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [0,1,2]:
    ax.plot(T, esc[p]["CR"], color=COLORES[p], lw=2, label=LABELS[p])
ax.axhline(CBS, color="#a78bfa", lw=1, ls="--", alpha=0.5, label=f"Capacidad base sin camión ({CBS})")
for p in [1,2]:
    if t_compras[p]:
        ax.axvline(t_compras[p], color=COLORES[p], lw=1, ls=":", alpha=0.7)
ax.set_title("Capacidad de Reparto por Escenario (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Capacidad Reparto (Caja/mes)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "04_capacidad_reparto.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 5 — ROI del camión (E1 y E2)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [1,2]:
    ax.plot(T, esc[p]["ROI"], color=COLORES[p], lw=2, label=LABELS[p])
ax.axhline(1.0, color="#f43f5e", lw=1.5, ls="--", alpha=0.8, label="ROI = 1 (camión se paga solo)")
ax.set_title("ROI del Camión por Escenario (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("ROI (adimensional)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "05_roi_camion.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 6 — Beneficio acumulado del camión (E1 y E2)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [1,2]:
    ax.plot(T, esc[p]["BAC"]/1e6, color=COLORES[p], lw=2, label=LABELS[p])
ax.axhline(50, color="#f43f5e", lw=1, ls="--", alpha=0.6, label="Costo del camión (50 M CLP)")
ax.set_title("Beneficio Acumulado del Camión (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Beneficio acumulado (M CLP)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.0f} M"))
plt.tight_layout()
plt.savefig(os.path.join(OUT, "06_beneficio_acumulado_camion.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 7 — Stock de huevos por escenario
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
for p in [0,1,2]:
    ax.plot(T, esc[p]["SH"], color=COLORES[p], lw=2, label=LABELS[p])
ax.set_title("Stock de Huevos por Escenario (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Stock de huevos (Caja)")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "07_stock_huevos.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 8 — Estacionalidad mensual
# ═══════════════════════════════════════════════════════════════════════════════
meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
factores = [_est[i] for i in range(12)]
colores_bar = ["#f97316" if f > 1 else "#60a5fa" for f in factores]
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(meses, factores, color=colores_bar, edgecolor="#0f1117", linewidth=0.5, zorder=3)
ax.axhline(1.0, color="#a78bfa", lw=1.5, ls="--", alpha=0.8, label="Factor neutro (1.0)")
for bar, f in zip(bars, factores):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02, f"{f:.2f}",
            ha="center", va="bottom", fontsize=8, color="#e8ecf4")
ax.set_title("Factor de Estacionalidad Mensual de la Demanda")
ax.set_ylabel("Factor multiplicador"); ax.set_ylim(0, 2.1)
ax.grid(True, axis="y"); ax.legend()
naranja = mpatches.Patch(color="#f97316", label="Demanda alta (> 1)")
azul    = mpatches.Patch(color="#60a5fa", label="Demanda baja (< 1)")
ax.legend(handles=[naranja, azul, plt.Line2D([0],[0], color="#a78bfa", ls="--", label="Factor neutro (1.0)")])
plt.tight_layout()
plt.savefig(os.path.join(OUT, "08_estacionalidad.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO 9 — Tasa de despacho vs Demanda total (E0, para ver brecha)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(T, esc[0]["DT"], color="#a78bfa", lw=1.5, ls="--", label="Demanda total (E0)")
ax.plot(T, esc[0]["TD"], color=COLORES[0], lw=2, label="Tasa despacho E0 (sin inversión)")
ax.plot(T, esc[2]["TD"], color=COLORES[2], lw=2, label="Tasa despacho E2 (proactivo)")
ax.fill_between(T, esc[0]["TD"], esc[0]["DT"],
                where=esc[0]["DT"] > esc[0]["TD"],
                alpha=0.15, color="#f43f5e", label="Brecha incumplimiento E0")
ax.set_title("Demanda Total vs Tasa de Despacho (meses 0–96)")
ax.set_xlabel("Tiempo (meses)"); ax.set_ylabel("Cajas/mes")
ax.legend(); ax.grid(True); ax.set_xlim(0,96)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "09_despacho_vs_demanda.png"), bbox_inches="tight")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# GUARDAR DATOS PARA TABLAS (JSON)
# ═══════════════════════════════════════════════════════════════════════════════
hitos = [12, 36, 60, 96]
datos_tabla = {}
for p in [0,1,2]:
    datos_tabla[p] = {}
    for h in hitos:
        datos_tabla[p][h] = {
            "DB":  round(esc[p]["DB"][h], 1),
            "TI":  round(esc[p]["TI"][h]*100, 2),
            "MA":  round(esc[p]["MA"][h]/1e6, 2),
            "ROI": round(esc[p]["ROI"][h], 3),
            "CR":  round(esc[p]["CR"][h], 1),
        }
    datos_tabla[p]["t_compra"] = t_compras[p]

# Mes en que ROI >= 1
for p in [1,2]:
    roi_1 = next((i for i in range(97) if esc[p]["ROI"][i] >= 1.0), None)
    datos_tabla[p]["mes_roi_1"] = roi_1

with open(os.path.join(OUT, "datos_tabla.json"), "w", encoding="utf-8") as f:
    json.dump(datos_tabla, f, indent=2, ensure_ascii=False)

print("OK - Todos los graficos generados en:", OUT)
print(f"   Escenario 1 (reactivo)  -> compra en mes: {t_compras[1]}")
print(f"   Escenario 2 (proactivo) -> compra en mes: {t_compras[2]}")
for p in [1,2]:
    roi_1 = datos_tabla[p].get("mes_roi_1")
    print(f"   Escenario {p} -> ROI = 1 en mes: {roi_1}")
print("\nDatos al mes 96:")
for p in [0,1,2]:
    d = datos_tabla[p][96]
    print(f"  E{p}: DB={d['DB']} | Incumpl={d['TI']}% | Margen={d['MA']} M CLP | ROI={d['ROI']}")
