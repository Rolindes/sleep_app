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

st.set_page_config(
    page_title="SleepArchitect Pro", 
    page_icon="🌙", 
    layout="centered"
)

# --- ESTILOS CSS LIMPIOS (Sin forzar colores en pestañas) ---
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
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌙 SleepArchitect Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Tu ecosistema inteligente de análisis y optimización del descanso</p>", unsafe_allow_html=True)
st.markdown("---")

# Cargar datos para métricas superiores
data = load_data()
if data:
    ultimos_registros = data[-7:]
    promedio_horas = sum(d["hours"] for d in ultimos_registros) / len(ultimos_registros)
    promedio_estres = sum(d["stress"] for d in ultimos_registros) / len(ultimos_registros)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>REGISTROS</p><h2 style='color:#ffffff;margin:5px 0 0 0;'>{len(data)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>MEDIA HORAS (7d)</p><h2 style='color:#38bdf8;margin:5px 0 0 0;'>{promedio_horas:.1f} h</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>MEDIA ESTRÉS (7d)</p><h2 style='color:#f43f5e;margin:5px 0 0 0;'>{promedio_estres:.1f} / 5</h2></div>", unsafe_allow_html=True)
    st.markdown("---")

# Pestañas (usando el formato nativo de Streamlit que se lee a la perfección)
tab1, tab2, tab3 = st.tabs(["📝 Registro Diario", "📊 Historial y Gráficos Avanzados", "💡 Pautas y Consejos"])

# --- PESTAÑA 1: REGISTRO DIARIO ---
with tab1:
    st.subheader("¿Cómo ha ido tu descanso?")
    
    c1, c2 = st.columns(2)
    with c1:
        horas_sueno = st.slider("Horas de sueño estimadas:", 1.0, 12.0, 7.5, 0.5)
        estres = st.selectbox("Nivel de estrés previo al dormir (1-5):", [1, 2, 3, 4, 5])
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

    st.markdown("")
    if st.button("🚀 Analizar mi Noche y Guardar Registro", type="primary", use_container_width=True):
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
        st.subheader("📊 Informe Inteligente de la Noche")

        calificacion_sueno = ""
        if horas_sueno < 6:
            st.error(f"⚠️ **Alerta crítica:** Has dormido solo {horas_sueno} horas. Tu rendimiento cognitivo hoy estará mermado. Prioriza descanso o una siesta corta.")
            calificacion_sueno = "malo"
        elif 6 <= horas_sueno < 7:
            st.warning(f"📉 **Sueño insuficiente:** {horas_sueno} horas. Lo recomendado para la recuperación celular son al menos 7h.")
            calificacion_sueno = "bajo"
        else:
            st.success(f"🌟 **Excelente descanso:** {horas_sueno} horas. Gran trabajo manteniendo el ciclo.")
            calificacion_sueno = "bueno"

        st.markdown("---")
        st.write("**Análisis Cruzado de Factores:**")
        if estres >= 4 and horas_sueno < 7:
            st.warning("🔴 **Bucle de estrés y fatiga:** El estrés elevado eleva el cortisol y arruina el sueño profundo. Hoy desconecta de pantallas y noticias 1h antes.")
        elif uso_pantallas and estres >= 4:
            st.write("📱+🤯 **Cóctel activador:** La luz azul sumada al estrés mantiene tu cerebro en estado de alerta constante.")
        elif cafe_tarde:
            st.write("☕ **Efecto residual de cafeína:** Reduce la eficiencia del sueño profundo aunque logres conciliar el sueño.")
        elif not uso_pantallas and estres <= 2 and horas_sueno >= 7:
            st.write("✨ **Hábitos óptimos:** Mantienes una rutina de desconexión envidiable.")

        st.markdown("---")
        st.info("🎯 **Acción recomendada para hoy:**")
        if calificacion_sueno in ["malo", "bajo"]:
             st.markdown("- Exponte a luz solar directa durante 15 minutos en tu primera hora de despertar para sincronizar tu reloj interno.")
        else:
            st.markdown("- Mantén tu horario de acostarte constante para reforzar tu ritmo circadiano.")


# --- PESTAÑA 2: HISTORIAL Y GRÁFICOS AVANZADOS ---
with tab2:
    st.subheader("📊 Panel de Tendencias Avanzadas")
    data = load_data()
    if not data:
        st.info("Aún no hay registros suficientes para generar gráficos. ¡Haz tu primer registro!")
    else:
        dates = [d["date"][-5:] for d in data[-14:]]
        hours = [d["hours"] for d in data[-14:]]
        stress_levels = [d["stress"] for d in data[-14:]]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), facecolor='#0e1117')
        
        # Subgráfico 1: Horas
        ax1.set_facecolor('#161b22')
        ax1.plot(dates, hours, marker="o", color="#38bdf8", linewidth=3, markersize=7, label="Horas Dormidas")
        ax1.axhline(7, color="#22c55e", linestyle="--", alpha=0.7, label="Mínimo Óptimo (7h)")
        ax1.set_title("Evolución del Tiempo de Sueño", color="#ffffff", fontsize=11, fontweight='bold', pad=10)
        ax1.tick_params(colors='#8b949e', labelsize=9)
        ax1.grid(True, linestyle=":", alpha=0.3, color="#8b949e")
        ax1.legend(facecolor='#161b22', edgecolor='none', labelcolor='#ffffff', loc='lower right')
        
        # Subgráfico 2: Estrés
        ax2.set_facecolor('#161b22')
        ax2.bar(dates, stress_levels, color="#f43f5e", alpha=0.8, width=0.5, label="Nivel de Estrés")
        ax2.set_title("Nivel de Estrés Previo al Sueño (1-5)", color="#ffffff", fontsize=11, fontweight='bold', pad=10)
        ax2.set_ylim(0, 5.5)
        ax2.tick_params(colors='#8b949e', labelsize=9)
        ax2.grid(True, linestyle=":", alpha=0.3, color="#8b949e")
        ax2.legend(facecolor='#161b22', edgecolor='none', labelcolor='#ffffff', loc='upper right')

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("📋 Historial Detallado")
        for d in reversed(data):
            with st.expander(f"📅 Fecha: {d['date']} — 🛏️ {d['hours']} horas (Estrés: {d['stress']}/5)"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"• **Hora de acostarse:** {d['bedtime']}")
                    st.write(f"• **Suplementos:** {d['supplements']}")
                with col_b:
                    factores = []
                    if d.get('screens'): factores.append("📱 Pantallas")
                    if d.get('caffeine'): factores.append("☕ Cafeína tarde")
                    if d.get('heavy_dinner'): factores.append("🍕 Cena pesada")
                    st.write(f"• **Factores negativos:** {', '.join(factores) if factores else 'Ninguno 🎉'}")


# --- PESTAÑA 3: PAUTAS ---
with tab3:
    st.subheader("💡 Pautas de Higiene del Sueño")
    st.markdown("""
    * **Consistencia horaria:** Acuéstate y despiértate a la misma hora incluso en fines de semana.
    * **Control lumínico:** Elimina la luz artificial y pantallas al menos 45 minutos antes de dormir.
    * **Temperatura ambiental:** Mantén el dormitorio fresco (18°C - 20°C).
    * **Digestión:** Cena al menos 2 a 3 horas antes de acostarte para evitar picos de actividad metabólica.
    """)
