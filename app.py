import json
import os
from datetime import datetime, timedelta
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
    .diagnosis-box {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA Y AUTORÍA ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌙 SleepArchitect Pro 🛌✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Tu asistente clínico avanzado de análisis de sueño y optimización del descanso</p>", unsafe_allow_html=True)

st.markdown("""
    <div class='author-banner'>
        ✨ <b>Aplicación diseñada y desarrollada profesionalmente por:</b> Rosa Muelas Martínez 🩺💤
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Cargar datos para métricas superiores
data = load_data()
if data:
    ultimos_registros = data[-7:]
    promedio_horas = sum(d["hours"] for d in ultimos_registros) / len(ultimos_registros)
    promedio_estres = sum(d["stress"] for d in ultimos_registros) / len(ultimos_registros)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>📊 TOTAL REGISTROS</p><h2 style='color:#ffffff;margin:5px 0 0 0;'>{len(data)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>💤 MEDIA HORAS (7d)</p><h2 style='color:#38bdf8;margin:5px 0 0 0;'>{promedio_horas:.1f} h</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>⚡ MEDIA ESTRÉS (7d)</p><h2 style='color:#f43f5e;margin:5px 0 0 0;'>{promedio_estres:.1f} / 5</h2></div>", unsafe_allow_html=True)
    st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📝 Registro Diario & Análisis", "📊 Historial y Gráficos", "🔬 Ciencia y Pautas Avanzadas"])

# --- PESTAÑA 1: REGISTRO DIARIO & SLEEP SCORE ---
with tab1:
    st.subheader("🛏️ ¿Cómo ha ido tu descanso hoy?")
    
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
    if st.button("🧠 Calcular Sleep Score y Generar Diagnóstico", type="primary", use_container_width=True):
        
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
        
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            if score >= 80:
                st.markdown(f"<div class='metric-card' style='border-color:#22c55e;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#22c55e;margin:5px 0;'>{score}/100</h1><p style='color:#22c55e;margin:0;font-size:12px;'>¡Excelente Descanso! 🌟</p></div>", unsafe_allow_html=True)
            elif score >= 55:
                st.markdown(f"<div class='metric-card' style='border-color:#eab308;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#eab308;margin:5px 0;'>{score}/100</h1><p style='color:#eab308;margin:0;font-size:12px;'>Descanso Aceptable ⚠️</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='metric-card' style='border-color:#f43f5e;'><p style='color:#9ca3af;margin:0;'>SLEEP SCORE</p><h1 style='color:#f43f5e;margin:5px 0;'>{score}/100</h1><p style='color:#f43f5e;margin:0;font-size:12px;'>Calidad Baja 🔴</p></div>", unsafe_allow_html=True)
        
        with col_s2:
            st.markdown("### 📋 Diagnóstico Personalizado de la Noche")
            
            # Diagnóstico dinámico detallado basado estrictamente en las respuestas
            diagnostico_texto = []
            if horas_sueno < 6:
                diagnostico_texto.append(f"Has dormido un total de **{horas_sueno} horas**, lo cual representa un déficit crítico que afectará directamente a tu atención y recuperación física hoy.")
            elif 6 <= horas_sueno < 7:
                diagnostico_texto.append(fHas dormido **{horas_sueno} horas**. Estás ligeramente por debajo del umbral óptimo de 7-8 horas necesario para completar los ciclos de reparación celular.")
            else:
                diagnostico_texto.append(f"Has registrado **{horas_sueno} horas** de sueño, una duración excelente para mantener tu rendimiento cognitivo.")

            if estres >= 4:
                diagnostico_texto.append(f"Se ha detectado un **nivel de estrés muy alto antes de dormir ({estres}/5)**, lo que eleva los niveles de cortisol e impide alcanzar las fases de sueño profundo.")
            elif estres == 3:
                diagnostico_texto.append("El nivel de estrés previo era moderado, lo que pudo retrasar ligeramente la velocidad a la que te quedaste dormido.")

            if despertares > 0:
                diagnostico_texto.append(f"Has sufrido **{despertares} despertares nocturnos**, fragmentando la continuidad del descanso y generando fatiga matutina.")

            habitos_malos = []
            if uso_pantallas: habitos_malos.append("el uso de pantallas (luz azul)")
            if cafe_tarde: habitos_malos.append("el consumo tardío de cafeína")
            if cena_pesada: habitos_malos.append("la cena pesada o alcohol")
            if ejercicio_tarde: habitos_malos.append("el ejercicio intenso nocturno")

            if habitos_malos:
                diagnostico_texto.append(f"Además, influyeron factores disruptivos como {' y '.join(habitos_malos)}, alterando tu ritmo biológico natural.")
            else:
                diagnostico_texto.append("¡Has evitado con éxito los principales disruptores de hábitos nocturnos!")

            st.info(" ".join(diagnostico_texto))

        st.markdown("---")
        st.subheader("🎯 Plan de Acción Específico para Hoy")
        
        if score < 60:
            st.markdown("""
            * **Apagón digital:** Cero pantallas al menos 1 hora antes de acostarte hoy.
            * **Regulación térmica:** Asegúrate de mantener la habitación fresca (18°C - 20°C).
            * **Luz de mañana:** Sal a caminar 15 minutos bajo la luz solar directa durante la mañana para reajustar tu reloj circadiano.
            """)
        elif score < 80:
            st.markdown("""
            * **Cena temprana:** Intenta cenar al menos 2 horas antes de irte a la cama para favorecer la digestión.
            * **Control de estímulos:** Evita bebidas con cafeína por la tarde y realiza respiraciones profundas si notas tensión acumulada.
            """)
        else:
            st.markdown("""
            * **Consistencia:** ¡Gran trabajo! Intenta acostarte y levantarte a la misma hora exacta hoy para consolidar este hábito positivo.
            """)


# --- PESTAÑA 2: HISTORIAL Y GRÁFICOS ---
with tab2:
    st.subheader("📊 Panel de Tendencias Avanzadas")
    data = load_data()
    if not data:
        st.info("Aún no hay registros suficientes.")
    else:
        dates = [d["date"][-5:] for d in data[-14:]]
        scores = [d.get("score", 70) for d in data[-14:]]

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


# --- PESTAÑA 3: CIENCIA Y PAUTAS AVANZADAS ---
with tab3:
    st.subheader("🔬 Ciencia del Sueño y Pautas Avanzadas")
    
    # 1. CALCULADORA DE CICLOS DE SUEÑO
    with st.expander("⏱️ Calculadora de Ciclos de Sueño (Basada en bloques de 90 min)", expanded=True):
        st.write("Un ciclo de sueño humano dura aproximadamente 90 minutos. Despertarse al final de un ciclo (y no a mitad) evita la inercia del sueño (mareo matutino).")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            hora_despertar = st.time_input("¿A qué hora te quieres despertar?", value=datetime.now().time().replace(hour=7, minute=0))
        with col_c2:
            st.write("**Horas recomendadas para acostarte (contando 15 min para dormir):**")
            dummy_date = datetime.today()
            dt_despert = datetime.combine(dummy_date, hora_despertar)
            
            ciclo_5 = dt_despert - timedelta(hours=7.5, minutes=15)
            ciclo_6 = dt_despert - timedelta(hours=9.0, minutes=15)
            ciclo_4 = dt_despert - timedelta(hours=6.0, minutes=15)
            
            st.success(f"🌙 **Ciclo óptimo (5 ciclos / 7.5h):** {ciclo_5.strftime('%H:%M')}")
            st.info(f"🌙 **Ciclo largo (6 ciclos / 9h):** {ciclo_6.strftime('%H:%M')}")
            st.warning(f"🌙 **Ciclo corto (4 ciclos / 6h):** {ciclo_4.strftime('%H:%M')}")

    st.markdown("---")

    # 2. CRONOBIOLOGÍA POR FASES
    st.subheader("🌅 Pautas Diarias por Cronobiología")
    
    f1, f2, f3 = st.tabs(["☀️ Mañana", "🌇 Tarde", "🌙 Noche"])
    with f1:
        st.markdown("""
        * **Luz solar directa:** Exponte al sol durante 10-15 minutos en tu primera hora al despertar. Esto detiene la producción de melatonina y pone en marcha tu reloj biológico.
        * **Cafeína estratégica:** Espera al menos 60-90 minutos tras levantarte para tomar tu primer café. Deja que el cortisol natural actúe primero.
        """)
    with f2:
        st.markdown("""
        * **Corte de cafeína:** Evita el café, té con teína o bebidas energéticas 8 horas antes de acostarte.
        * **Ejercicio físico:** Realiza ejercicio preferiblemente por la mañana o tarde, evitando entrenamientos de alta intensidad justo antes de dormir.
        """)
    with f3:
        st.markdown("""
        * **Oscuridad y Temperatura:** Mantén la habitación a unos 18°C-20°C y en total oscuridad.
        * **Desconexión digital:** Apaga pantallas y luces intensas al menos 45 minutos antes de ir a la cama.
        """)

    st.markdown("---")

    # 3. MITOS VS REALIDADES
    st.subheader("🧩 Mitos vs. Realidades del Sueño")
    
    with st.expander("❌ Mito 1: 'El alcohol ayuda a relajarse y dormir mejor'"):
        st.write("**Realidad:** Falso. Aunque el alcohol puede ayudarte a conciliar el sueño más rápido, fragmenta el sueño en la segunda mitad de la noche, destruye el sueño REM y provoca despertares frecuentes.")
        
    with st.expander("❌ Mito 2: 'Puedo recuperar el sueño perdido el fin de semana'"):
        st.write("**Realidad:** Parcialmente falso. Dormir 12 horas el domingo altera tu ritmo circadiano (jet-lag social), haciendo que te cueste mucho más conciliar el sueño el domingo por la noche.")

    with st.expander("❌ Mito 3: 'Con 5 o 6 horas de sueño al día mi cuerpo se acostumbra'"):
        st.write("**Realidad:** Falso. Menos del 1% de la población tiene una mutación genética real para funcionar con <6h. El resto sufre una merma cognitiva acumulativa que el cerebro oculta.")

    st.markdown("---")

    # 4. MINI-QUIZ INTERACTIVO AMPLIADO Y MEJORADO
    st.subheader("📝 Test Avanzado: ¿Qué tan saludable es tu higiene de sueño?")
    st.write("Responde a estas 4 preguntas clave para auditar tus hábitos nocturnos:")
    
    t_q1 = st.radio("1. ¿Utiliza dispositivos con pantallas (móvil, tablet, TV) en la cama antes de apagar la luz?", ["No, los evito 45 min antes", "A veces o unos minutos", "Sí, hasta que me duermo"])
    t_q2 = st.radio("2. ¿A qué temperatura aproximada mantienes tu dormitorio por la noche?", ["Fresca (18°C - 20°C)", "Templada / Normal", "Calurosa (más de 23°C)"])
    t_q3 = st.radio("3. ¿Consumes café, bebidas energéticas o alcohol en las 4-6 horas previas a acostarte?", ["Nunca", "Ocasionalmente", "Sí, con frecuencia"])
    t_q4 = st.radio("4. ¿Tienes un horario de despertador constante (incluso los fines de semana)?", ["Sí, varía menos de 30 min", "Varía entre 1 y 2 horas", "Varía totalmente según el día"])

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

        st.markdown("---")
        st.markdown(f"### 🎯 Tu Puntuación de Hábitos: {puntuacion_test} / 100")
        
        if puntuacion_test >= 75:
            st.success("🌟 ¡Excepcional! Tienes unos hábitos de higiene del sueño de referencia. Proteges tu descanso de maravilla.")
        elif puntuacion_test >= 40:
            st.warning("⚠️ Vas por buen camino, pero tienes algunos hábitos invisibles (como pantallas o cafeína) que están restando calidad a tus noches.")
        else:
            st.error("🔴 Tus hábitos actuales presentan múltiples factores de riesgo para el insomnio. Te recomendamos revisar las pautas superiores para empezar a cambiarlos.") superiores para empezar a cambiarlos.")
