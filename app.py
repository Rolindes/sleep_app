import json
import os
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
DATA_FILE = "sleep_data_pro_ai.json"

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

st.set_page_config(
    page_title="SleepArchitect AI Pro", 
    page_icon="🧠", 
    layout="centered"
)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🧠 SleepArchitect AI Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Asistente inteligente con cálculo de Puntuación de Sueño y Diagnóstico Avanzado</p>", unsafe_allow_html=True)
st.markdown("---")

# Cargar datos para métricas superiores
data = load_data()
if data:
    ultimos_registros = data[-7:]
    promedio_horas = sum(d["hours"] for d in ultimos_registros) / len(ultimos_registros)
    promedio_estres = sum(d["stress"] for d in ultimos_registros) / len(ultimos_registros)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>TOTAL REGISTROS</p><h2 style='color:#ffffff;margin:5px 0 0 0;'>{len(data)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>MEDIA HORAS (7d)</p><h2 style='color:#38bdf8;margin:5px 0 0 0;'>{promedio_horas:.1f} h</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>MEDIA ESTRÉS (7d)</p><h2 style='color:#f43f5e;margin:5px 0 0 0;'>{promedio_estres:.1f} / 5</h2></div>", unsafe_allow_html=True)
    st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📝 Registro Diario & IA", "📊 Historial y Gráficos", "💡 Pautas Profesionales"])

# --- PESTAÑA 1: REGISTRO DIARIO & SLEEP SCORE ---
with tab1:
    st.subheader("¿Cómo ha ido tu descanso hoy?")
    
    c1, c2 = st.columns(2)
    with c1:
        horas_sueno = st.slider("Horas de sueño estimadas:", 1.0, 12.0, 7.5, 0.5)
        estres = st.selectbox("Nivel de estrés previo al dormir (1-5):", [1, 2, 3, 4, 5])
        despertares = st.slider("Número de despertares nocturnos:", 0, 5, 0)
    with c2:
        hora_acostarse = st.time_input("Hora aproximada de acostarte:", value=datetime.now().time().replace(hour=23, minute=0, second=0))
        suplementos = st.multiselect("¿Tomaste suplementos?", ["Melatonina", "Valeriana", "Infusión Relajante", "CBD", "Nada"])

    st.markdown("#### ⚙️ Hábitos y Entorno Nocturno")
    c3, c4 = st.columns(2)
    with c3:
        uso_pantallas = st.checkbox("📱 Uso de pantallas 30 min antes")
        cena_pesada = st.checkbox("🍕 Cena copiosa o alcohol tarde")
    with c4:
        cafe_tarde = st.checkbox("☕ Cafeína después de las 16:00")
        ejercicio_tarde = st.checkbox("🏃‍♂️ Ejercicio intenso a última hora")

    st.markdown("")
    if st.button("🧠 Calcular Sleep Score y Analizar Noche", type="primary", use_container_width=True):
        
        # --- ALGORITMO SLEEP SCORE (0 a 100) ---
        score = 100
        
        # Penalización por horas (ideal entre 7 y 9)
        if horas_sueno < 6:
            score -= 30
        elif 6 <= horas_sueno < 7:
            score -= 15
        elif horas_sueno > 10:
            score -= 10
            
        # Penalización por estrés (1 a 5)
        score -= (estres - 1) * 6
        
        # Penalización por despertares
        score -= despertares * 5
        
        # Penalización por malos hábitos
        if uso_pantallas: score -= 10
        if cena_pesada: score -= 12
        if cafe_tarde: score -= 15
        if ejercicio_tarde: score -= 8
        
        score = max(10, min(100, score)) # Limitar entre 10 y 100

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hours": horas_sueno,
            "stress": estres,
            "wakeups": despertares,
            "bedtime": str(hora_acostarse),
            "supplements": ", ".join(suplementos),
            "screens": uso_pantallas,
            "heavy_dinner": cena_pesada,
            "caffeine": cafe_tarde,
            "exercise": ejercicio_tarde,
            "score": score
        }
        data = load_data()
        data = [d for d in data if d["date"] != entry["date"]]
        data.append(entry)
        save_data(data)

        st.success("✅ ¡Registro analizado con éxito!")
        st.markdown("---")
        
        # Mostrar Puntuación Visual
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            if score >= 80:
                st.markdown(f"<div class='metric-card' style='border-color:#22c55e;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#22c55e;margin:5px 0;'>{score}/100</h1><p style='color:#22c55e;margin:0;font-size:12px;'>¡Excelente!</p></div>", unsafe_allow_html=True)
            elif score >= 55:
                st.markdown(f"<div class='metric-card' style='border-color:#eab308;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#eab308;margin:5px 0;'>{score}/100</h1><p style='color:#eab308;margin:0;font-size:12px;'>Aceptable</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='metric-card' style='border-color:#f43f5e;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#f43f5e;margin:5px 0;'>{score}/100</h1><p style='color:#f43f5e;margin:0;font-size:12px;'>Mejorable</p></div>", unsafe_allow_html=True)
        with col_s2:
            st.subheader("📊 Diagnóstico Dinámico por IA")
            if score >= 80:
                st.success("Tu noche ha sido de alta calidad regenerativa. Has mantenido a raya los disruptores del sueño.")
            elif score >= 55:
                st.warning("Tu descanso ha sido regular. Algunos factores han mermado la profundidad de tu sueño.")
            else:
                st.error("Alerta de baja calidad de sueño. La acumulación de varios factores negativos ha impactado fuertemente tu descanso.")

        st.markdown("---")
        st.write("**Desglose de Factores Disruptivos Detectados:**")
        
        factores_activos = []
        if horas_sueno < 7: factores_activos.append("⚠️ **Déficit de horas:** No has alcanzado el mínimo recomendado.")
        if estres >= 4: factores_activos.append("🤯 **Estrés elevado:** Niveles de tensión que generan picos de cortisol nocturno.")
        if despertares >= 2: factores_activos.append("🔄 **Sueño fragmentado:** Múltiples despertares reducen la fase REM y profunda.")
        if uso_pantallas: factores_activos.append("📱 **Luz azul:** Inhibición directa de la melatonina por las pantallas.")
        if cafe_tarde: factores_activos.append("☕ **Cafeína residual:** Bloqueadores de adenosina activos en sangre.")
        if cena_pesada: factores_activos.append("🍕 **Digestión pesada:** Actividad metabólica alta interfiriendo con la bajada de temperatura corporal.")

        if factores_activos:
            for f in factores_activos:
                st.markdown(f"- {f}")
        else:
            st.markdown("- ✨ ¡Ningún factor negativo relevante detectado! Has protegido tu ciclo circadiano.")

        st.markdown("---")
        st.info("🎯 **Plan de Acción Personalizado para Hoy:**")
        if score < 60:
            st.markdown("- **Prioridad alta:** Hoy es un día para bajar revoluciones. Cena ligero, apaga pantallas 1 hora antes de dormir y sal a caminar a la luz del sol esta mañana.")
        else:
            st.markdown("- **Consistencia:** Todo marcha sobre ruedas. Mantén los mismos horarios de acostarte hoy para automatizar tu reloj biológico.")


# --- PESTAÑA 2: HISTORIAL Y GRÁFICOS ---
with tab2:
    st.subheader("📊 Panel de Tendencias Avanzadas")
    data = load_data()
    if not data:
        st.info("Aún no hay registros suficientes.")
    else:
        dates = [d["date"][-5:] for d in data[-14:]]
        scores = [d.get("score", 70) for d in data[-14:]]
        hours = [d["hours"] for d in data[-14:]]

        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0e1117')
        ax.set_facecolor('#161b22')
        ax.plot(dates, scores, marker="o", color="#22c55e", linewidth=3, markersize=7, label="Sleep Score (0-100)")
        ax.set_title("Evolución de tu Puntuación de Sueño", color="#ffffff", fontsize=12, fontweight='bold', pad=10)
        ax.set_ylim(0, 105)
        ax.tick_params(colors='#8b949e', labelsize=9)
        ax.grid(True, linestyle=":", alpha=0.3, color="#8b949e")
        ax.legend(facecolor='#161b22', edgecolor='none', labelcolor='#ffffff', loc='lower right')
        
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("📋 Historial Detallado")
        for d in reversed(data):
            with st.expander(f"📅 {d['date']} — 🌟 Sleep Score: {d.get('score', 'N/A')}/100 (🛏️ {d['hours']}h)"):
                st.write(f"• **Estrés:** {d['stress']}/5 | **Despertares:** {d.get('wakeups', 0)}")
                st.write(f"• **Suplementos:** {d['supplements']}")


# --- PESTAÑA 3: PAUTAS ---
with tab3:
    st.subheader("💡 Pautas de Higiene del Sueño")
    st.markdown("""
    * **Consistencia horaria:** Acuéstate y despiértate a la misma hora.
    * **Control lumínico:** Elimina pantallas 45 minutos antes.
    * **Temperatura:** Mantén la habitación entre 18°C y 20°C.
    * **Cenas ligeras:** Evita comidas pesadas o alcohol 3 horas antes.
    """)
