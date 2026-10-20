import json
import os
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
DATA_FILE = "sleep_data_pro_profiles.json"

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
    .author-banner {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border-left: 4px solid #38bdf8;
        padding: 14px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: #f3f4f6;
        font-size: 15px;
    }
    .report-box {
        background: #1f2937;
        border: 1px solid #374151;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA Y AUTORÍA ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌙 SleepArchitect Pro 🛌✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Asistente clínico avanzado con perfiles de usuario y optimización del descanso</p>", unsafe_allow_html=True)

st.markdown("""
    <div class='author-banner'>
        ✨ <b>Aplicación diseñada y desarrollada profesionalmente por:</b> Rosa Muelas Martínez 🩺💤
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Cargar datos para métricas globales superiores
data = load_data()
if data:
    total_regs = len(data)
    promedio_horas = sum(d["hours"] for d in data) / total_regs
    promedio_estres = sum(d["stress"] for d in data) / total_regs
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>📊 TOTAL REGISTROS</p><h2 style='color:#ffffff;margin:5px 0 0 0;'>{total_regs}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>💤 MEDIA HORAS (Global)</p><h2 style='color:#38bdf8;margin:5px 0 0 0;'>{promedio_horas:.1f} h</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>⚡ MEDIA ESTRÉS (Global)</p><h2 style='color:#f43f5e;margin:5px 0 0 0;'>{promedio_estres:.1f} / 5</h2></div>", unsafe_allow_html=True)
    st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📝 Registro Diario & Análisis", "👥 Historial e Informes por Persona", "🔬 Ciencia y Pautas Avanzadas"])

# --- PESTAÑA 1: REGISTRO DIARIO & SLEEP SCORE ---
with tab1:
    st.subheader("🛏️ ¿Cómo ha ido el descanso hoy?")
    
    # Campo de nombre del usuario
    nombre_usuario = st.text_input("👤 Nombre o Identificador de la persona:", placeholder="Ej: Rosa, Juan, Paciente 1...")

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
    if st.button("🧠 Calcular Sleep Score y Guardar Registro", type="primary", use_container_width=True):
        if not nombre_usuario.strip():
            st.warning("⚠️ Por favor, introduce un nombre o identificador antes de guardar el registro.")
        else:
            score = 100
            if horas_sueno < 6: score -= 30
            elif 6 <= horas_sueno < 7: score -= 15
            elif horas_sueno > 10: score -= 10
                
            score -= (estres - 1) * 6
            score -= despertares * 5
            if uso_pantallas: score -= 10
            if cena_pesada: score -= 12
            if cafe_tarde: score -= 15
            if ejercicio_tarde: score -= 8
            score = max(10, min(100, score))

            entry = {
                "name": nombre_usuario.strip().title(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
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
            data.append(entry)
            save_data(data)

            st.success(f"✅ ¡Registro guardado para **{entry['name']}** con éxito!")
            st.markdown("---")
            
            col_s1, col_s2 = st.columns([1, 2])
            with col_s1:
                if score >= 80:
                    st.markdown(f"<div class='metric-card' style='border-color:#22c55e;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#22c55e;margin:5px 0;'>{score}/100</h1><p style='color:#22c55e;margin:0;font-size:12px;'>¡Excelente Descanso! 🌟</p></div>", unsafe_allow_html=True)
                elif score >= 55:
                    st.markdown(f"<div class='metric-card' style='border-color:#eab308;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#eab308;margin:5px 0;'>{score}/100</h1><p style='color:#eab308;margin:0;font-size:12px;'>Descanso Aceptable ⚠️</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='metric-card' style='border-color:#f43f5e;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#f43f5e;margin:5px 0;'>{score}/100</h1><p style='color:#f43f5e;margin:0;font-size:12px;'>Calidad Baja 🔴</p></div>", unsafe_allow_html=True)
            
            with col_s2:
                st.markdown(f"### 📋 Diagnóstico para {entry['name']}")
                diagnostico_texto = []
                if horas_sueno < 6:
                    diagnostico_texto.append(f"Has dormido **{horas_sueno} horas**, un déficit crítico que afectará a tu recuperación hoy.")
                elif 6 <= horas_sueno < 7:
                    diagnostico_texto.append(f"Has dormido **{horas_sueno} horas**, ligeramente por debajo del óptimo.")
                else:
                    diagnostico_texto.append(f"Has registrado **{horas_sueno} horas**, una duración estupenda.")

                if estres >= 4:
                    diagnostico_texto.append(f"Estrés elevado ({estres}/5) previo al sueño.")
                if despertares > 0:
                    diagnostico_texto.append(f"Se registraron {despertares} despertares nocturnos.")
                
                st.info(" ".join(diagnostico_texto))


# --- PESTAÑA 2: HISTORIAL E INFORMES POR PERSONA ---
with tab2:
    st.subheader("👥 Informes Globales por Persona")
    data = load_data()
    if not data:
        st.info("Aún no hay registros guardados en la aplicación.")
    else:
        # Extraer nombres únicos
        nombres_disponibles = sorted(list(set(d["name"] for d in data)))
        
        persona_seleccionada = st.selectbox("Selecciona una persona para ver su informe global:", nombres_disponibles)
        
        # Filtrar registros de la persona
        registros_persona = [d for d in data if d["name"] == persona_seleccionada]
        
        st.markdown("---")
        st.markdown(f"### 📄 Informe Global de Descanso: **{persona_seleccionada}**")
        
        # Calcular métricas de la persona
        total_p = len(registros_persona)
        media_horas_p = sum(d["hours"] for d in registros_persona) / total_p
        media_score_p = sum(d.get("score", 70) for d in registros_persona) / total_p
        media_estres_p = sum(d["stress"] for d in registros_persona) / total_p
        
        # Tarjetas de resumen de la persona
        cp1, cp2, cp3 = st.columns(3)
        cp1.metric("Registros de la persona", total_p)
        cp2.metric("Sleep Score Medio", f"{media_score_p:.1f} / 100")
        cp3.metric("Media de Horas", f"{media_horas_p:.1f} h")
        
        # Evaluación automática del informe global
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.write(f"**Valoración clínica general para {persona_seleccionada}:**")
        if media_score_p >= 75:
            st.success(f"🌟 {persona_seleccionada} mantiene una excelente media de descanso general. Sus hábitos protegen de forma constante la calidad de su sueño.")
        elif media_score_p >= 50:
            st.warning(f"⚠️ El rendimiento de descanso de {persona_seleccionada} es moderado. Conviene revisar los factores de estrés o el uso de pantallas recurrentes.")
        else:
            st.error(f"🔴 Se observa una tendencia acumulada de baja calidad de sueño en los registros de {persona_seleccionada}. Se recomienda aplicar estrictamente las pautas de higiene.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader(f"📋 Historial Detallado de {persona_seleccionada}")
        for d in reversed(registros_persona):
            with st.expander(f"📅 {d['date']} — 🌟 Sleep Score: {d.get('score', 'N/A')}/100 (🛏️ {d['hours']}h)"):
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    st.write(f"• **Hora de acostarse:** {d.get('bedtime', 'No ind.')}")
                    st.write(f"• **Nivel de estrés:** {d['stress']}/5")
                    st.write(f"• **Despertares:** {d.get('wakeups', 0)}")
                with col_h2:
                    st.write(f"• **Suplementos:** {d['supplements'] if d['supplements'] else 'Ninguno'}")
                    habitos_guardados = []
                    if d.get('screens'): habitos_guardados.append("📱 Pantallas")
                    if d.get('caffeine'): habitos_guardados.append("☕ Cafeína")
                    if d.get('heavy_dinner'): habitos_guardados.append("🍕 Cena pesada")
                    if d.get('exercise'): habitos_guardados.append("🏃‍♂️ Ejercicio tarde")
                    st.write(f"• **Factores registrados:** {', '.join(habitos_guardados) if habitos_guardados else 'Ninguno 🎉'}")


# --- PESTAÑA 3: CIENCIA Y PAUTAS AVANZADAS ---
with tab3:
    st.subheader("🔬 Ciencia del Sueño y Pautas Avanzadas")
    
    with st.expander("⏱️ Calculadora de Ciclos de Sueño", expanded=True):
        st.write("Un ciclo de sueño humano dura aproximadamente 90 minutos.")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            hora_despertar = st.time_input("¿A qué hora te quieres despertar?", value=datetime.now().time().replace(hour=7, minute=0))
        with col_c2:
            dummy_date = datetime.today()
            dt_despert = datetime.combine(dummy_date, hora_despertar)
            ciclo_5 = dt_despert - timedelta(hours=7.5, minutes=15)
            ciclo_6 = dt_despert - timedelta(hours=9.0, minutes=15)
            ciclo_4 = dt_despert - timedelta(hours=6.0, minutes=15)
            st.success(f"🌙 **Ciclo óptimo (5 ciclos / 7.5h):** {ciclo_5.strftime('%H:%M')}")
            st.info(f"🌙 **Ciclo largo (6 ciclos / 9h):** {ciclo_6.strftime('%H:%M')}")

    st.markdown("---")
    st.subheader("🌅 Pautas Diarias por Cronobiología")
    f1, f2, f3 = st.tabs(["☀️ Mañana", "🌇 Tarde", "🌙 Noche"])
    with f1:
        st.markdown("* **Luz solar directa:** Exponte al sol 10-15 min en tu primera hora al despertar.")
    with f2:
        st.markdown("* **Corte de cafeína:** Evita el café 8 horas antes de acostarte.")
    with f3:
        st.markdown("* **Oscuridad y Temperatura:** Mantén la habitación a 18°C-20°C y en total oscuridad.")

    st.markdown("---")
    st.subheader("📝 Test Avanzado de Hábitos")
    t_q1 = st.radio("1. ¿Utiliza dispositivos con pantallas en la cama antes de apagar la luz?", ["No, los evito 45 min antes", "A veces o unos minutos", "Sí, hasta que me duermo"])
    t_q2 = st.radio("2. ¿A qué temperatura aproximada mantienes tu dormitorio?", ["Fresca (18°C - 20°C)", "Templada / Normal", "Calurosa"])
    t_q3 = st.radio("3. ¿Consumes café o alcohol en las 4-6 horas previas?", ["Nunca", "Ocasionalmente", "Sí, con frecuencia"])
    t_q4 = st.radio("4. ¿Tienes un horario de despertador constante?", ["Sí, varía menos de 30 min", "Varía entre 1 y 2 horas", "Varía totalmente"])

    if st.button("Calcular Diagnóstico de Hábitos", type="secondary"):
        puntuacion_test = 0
        if t_q1 == "No, los evito 45 min antes": puntuacion_test += 25
        elif t_q1 == "A veces o unos minutos": puntuacion_test += 10
        if t_q2 == "Fresca (18°C - 20°C)": puntuacion_test += 25
        elif t_q2 == "Templada / Normal": puntuacion_test += 10
        if t_q3 == "Nunca": puntuacion_test += 25
        elif t_q3 == "Ocasionalmente": puntuacion_test += 10
        if t_q4 == "Sí, varía menos de 30 min": puntuacion_test += 25
        elif t_q4 == "Varía entre 1 y 2 horas": puntuacion_test += 10

        st.markdown(f"### 🎯 Tu Puntuación de Hábitos: {puntuacion_test} / 100")
        if puntuacion_test >= 75:
            st.success("🌟 ¡Excepcional! Tienes unos hábitos de higiene del sueño de referencia.")
        else:
            st.warning("⚠️ Hay margen de mejora en tus hábitos nocturnos.")
