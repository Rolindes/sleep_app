import json
import os
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
DATA_FILE = "sleep_data_advanced.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Configuración de página con diseño limpio
st.set_page_config(
    page_title="SleepArchitect AI", 
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PERSONALIZADOS (MEJORA VISUAL) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: #c9d1d9;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        color: white !important;
        font-weight: bold;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA VISUAL ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🧠 SleepArchitect</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Tu asistente inteligente de sueño y optimización del descanso</p>", unsafe_allow_html=True)
st.markdown("---")

# Cargar datos para métricas rápidas
data = load_data()
if data:
    ultimos_registros = data[-7:]
    promedio_horas = sum(d["hours"] for d in ultimos_registros) / len(ultimos_registros)
    promedio_estres = sum(d["stress"] for d in ultimos_registros) / len(ultimos_registros)
    
    # Tarjetas de métricas visuales arriba
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("📊 Registros Totales", len(data))
    col_m2.metric("💤 Media Horas (Últimos)", f"{promedio_horas:.1f} h")
    col_m3.metric("⚡ Media Estrés", f"{promedio_estres:.1f} / 5")
    st.markdown("---")

# Pestañas
tab1, tab2, tab3 = st.tabs(["📝 Registro Diario", "📋 Historial y Tendencias", "💡 Pautas de Higiene"])

# --- PESTAÑA 1: REGISTRO DIARIO ---
with tab1:
    st.subheader("¿Cómo dormiste anoche?")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            horas_sueno = st.slider("Horas de sueño:", 1.0, 12.0, 7.0, 0.5, help="Calcula el tiempo total estimado de sueño")
            estres = st.selectbox("Nivel de estrés previo al sueño (1-5):", [1, 2, 3, 4, 5], help="1=Muy relajado, 5=Muy estresado")
        with c2:
            hora_acostarse = st.time_input("Hora aproximada de acostarte:", value=datetime.now().time().replace(hour=23, minute=0, second=0))
            suplementos = st.multiselect("¿Tomaste algo para dormir?", ["Melatonina", "Valeriana", "Infusión Relajante", "CBD", "Nada"])

    st.markdown("### Hábitos y Entorno")
    c3, c4 = st.columns(2)
    with c3:
        uso_pantallas = st.checkbox("📱 Uso de pantallas (móvil/TV) 30 min antes")
        cena_pesada = st.checkbox("🍕 Cena copiosa o alcohol tarde")
    with c4:
        cafe_tarde = st.checkbox("☕ Cafeína después de las 16:00")

    st.markdown("")
    if st.button("Analizar mi Noche y Guardar Registro", type="primary"):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hours": horas_sueno,
            "stress": estres,
            "bedtime": str(hora_acostarse),
            "supplements": ", ".join(suplementos),
            "screens": uso_pantallas,
            "heavy_dinner": cena_pesada,
            "caffeine": cafe_tarde
        }
        data = load_data()
        data = [d for d in data if d["date"] != entry["date"]]
        data.append(entry)
        save_data(data)

        st.success("✅ ¡Datos guardados correctamente!")
        st.markdown("---")
        st.subheader("📊 Tu Informe de Sueño Asistido")

        # --- LÓGICA DE CONSEJOS INTELIGENTES (IDÉNTICA A ANTES) ---
        calificacion_sueno = ""
        if horas_sueno < 6:
            st.error(f"⚠️ **Alerta de sueño crítico:** Solo has dormido {horas_sueno} horas. Tu rendimiento cognitivo y estado de ánimo se verán afectados hoy. Prioriza una siesta corta o vete a dormir pronto hoy.")
            calificacion_sueno = "malo"
        elif 6 <= horas_sueno < 7:
            st.warning(f"📉 **Sueño insuficiente:** Has dormido {horas_sueno} horas. Necesitas consolidar al menos 7 para una reparación óptima.")
            calificacion_sueno = "bajo"
        else:
            st.success(f"🌟 **Buena duración:** Has dormido {horas_sueno} horas. Es un gran punto de partida.")
            calificacion_sueno = "bueno"

        st.markdown("---")
        st.write("**Análisis de Factores Clave:**")
        
        if estres >= 4 and horas_sueno < 7:
            st.warning("🔴 **Bucle de estrés:** El estrés elevado dificulta entrar en sueño profundo y tú ya dormiste poco. Para hoy, evita noticias y prueba meditación o lectura 1 hora antes de dormir.")
        elif uso_pantallas and estres >= 4:
            st.write("📱+🤯 **Cóctel estimulante:** La luz azul de pantallas y el estrés mantienen tu cerebro alerta. El uso de gafas con filtro azul o modo nocturno es esencial si no puedes evitarlas.")
        elif cafe_tarde:
            st.write("☕ **Efecto de cafeína:** Si tomaste café después de las 16:00, aunque te duermas, reduce la calidad del sueño profundo. Intenta cortarla 8h antes de dormir.")
        elif not uso_pantallas and estres <= 2 and horas_sueno >= 7:
            st.write("✨ **Excelente rutina:** Mantienes unos hábitos de desconexión envidiables. ¡Sigue así! Tu descanso será de calidad.")

        if "Melatonina" in suplementos and horas_sueno < 6:
            st.write("💊 **Nota sobre Melatonina:** Si la tomas y sigues durmiendo mal, quizás necesites ajustar la hora de toma o consultar a un médico, no es una solución mágica si hay estrés elevado.")

        st.markdown("---")
        st.info("🎯 **Consejo para tu próximo ciclo de sueño (HOY):**")
        if calificacion_sueno == "malo" or calificacion_sueno == "bajo":
             st.markdown("- **La acción de hoy:** Exponte a la luz solar de la mañana (sal a pasear 10-15 min al despertar) para sincronizar tu reloj biológico y facilitar que el sueño llegue a su hora esta noche.")
        else:
            st.markdown("- **La acción de hoy:** Mantén la constancia. Intenta acostarte a la misma hora que ayer para reforzar tu ritmo circadiano.")


# --- PESTAÑA 2: HISTORIAL ---
with tab2:
    st.subheader("📋 Historial y Tendencias")
    data = load_data()
    if not data:
        st.info("Aún no hay datos registrados.")
    else:
        dates = [d["date"][-5:] for d in data[-15:]]
        hours = [d["hours"] for d in data[-15:]]
        
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(dates, hours, marker="o", color="#2ecc71", linewidth=2.5, markersize=6)
        ax.set_title("Tendencia de Sueño (Últimos 15 días)", color="white", pad=10)
        ax.set_ylabel("Horas", color="white")
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.grid(True, linestyle="--", alpha=0.2)
        st.pyplot(fig)

        st.markdown("---")
        st.write("**Detalle de registros anteriores:**")
        for d in reversed(data):
            with st.expander(f"📅 {d['date']} — {d['hours']}h de sueño"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Hora acostarse:** {d['bedtime']}")
                    st.write(f"**Estrés:** {d['stress']}/5")
                with col_b:
                    st.write(f"**Suplementos:** {d['supplements']}")
                    factores_negativos = []
                    if d.get('screens'): factores_negativos.append("📱 Pantallas")
                    if d.get('caffeine'): factores_negativos.append("☕ Cafeína")
                    if d.get('heavy_dinner'): factores_negativos.append("🍕 Cena/Alcohol")
                    if factores_negativos:
                        st.write(f"**Factores negativos:** {', '.join(factores_negativos)}")


# --- PESTAÑA 3: PAUTAS GENERALES ---
with tab3:
    st.subheader("💡 Pautas de Higiene del Sueño")
    st.markdown("""
    * **Regularidad:** Acuéstate y despiértate a la misma hora todos los días.
    * **Oscuridad:** Duerme en total oscuridad para proteger la melatonina natural.
    * **Temperatura:** Mantén la habitación fresca (18°C - 21°C).
    * **Vientre ligero:** Evita comidas pesadas o alcohol 2-4 horas antes de acostarte.
    * **Asociación de cama:** La cama es exclusivamente para dormir.
    """)
