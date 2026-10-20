import json
import os
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

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
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #e6edf3;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA Y AUTORÍA ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌙 SleepArchitect Pro 🛌✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Asistente clínico avanzado con perfiles de usuario, test de cortisol y optimización del descanso</p>", unsafe_allow_html=True)

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
    promedio_horas = sum(float(d.get("hours", 7)) for d in data) / total_regs
    promedio_estres = sum(float(d.get("stress", 3)) for d in data) / total_regs
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>📊 TOTAL REGISTROS</p><h2 style='color:#ffffff;margin:5px 0 0 0;'>{total_regs}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>💤 MEDIA HORAS (Global)</p><h2 style='color:#38bdf8;margin:5px 0 0 0;'>{promedio_horas:.1f} h</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color:#9ca3af;font-size:12px;margin:0;'>⚡ MEDIA ESTRÉS (Global)</p><h2 style='color:#f43f5e;margin:5px 0 0 0;'>{promedio_estres:.1f} / 5</h2></div>", unsafe_allow_html=True)
    st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Registro Diario", "🧬 Test de Cortisol Diario", "👥 Historial e Informes", "🔬 Ciencia y Pautas"])

# --- PESTAÑA 1: REGISTRO DIARIO & SLEEP SCORE ---
with tab1:
    st.subheader("🛏️ ¿Cómo ha ido el descanso hoy?")
    
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

            hoy_fecha = datetime.now().strftime("%Y-%m-%d")
            nombre_limpio = nombre_usuario.strip().title()

            data = load_data()
            
            registro_existente = None
            for d in data:
                if d.get("name") == nombre_limpio and str(d.get("date", "")).startswith(hoy_fecha):
                    registro_existente = d
                    break

            if registro_existente:
                registro_existente["hours"] = horas_sueno
                registro_existente["stress"] = estres
                registro_existente["wakeups"] = despertares
                registro_existente["bedtime"] = str(hora_acostarse)
                registro_existente["supplements"] = ", ".join(suplementos)
                registro_existente["screens"] = uso_pantallas
                registro_existente["heavy_dinner"] = cena_pesada
                registro_existente["caffeine"] = cafe_tarde
                registro_existente["exercise"] = ejercicio_tarde
                registro_existente["score"] = score
                st.success(f"✅ ¡Registro del día actualizado para **{nombre_limpio}** sin duplicar!")
            else:
                entry = {
                    "name": nombre_limpio,
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
                    "score": score,
                    "cortisol_index": "N/A"
                }
                data.append(entry)
                st.success(f"✅ ¡Nuevo registro guardado con éxito para **{nombre_limpio}**!")

            save_data(data)
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
                st.markdown(f"### 📋 Diagnóstico para {nombre_limpio}")
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


# --- PESTAÑA 2: TEST DE CORTISOL DIARIO ---
with tab2:
    st.subheader("🧬 Test de Evaluación del Cortisol Diario")
    st.write("Mide cómo tus hábitos, carga laboral, discusiones y momentos de ocio han afectado a tus niveles de estrés y cortisol acumulado antes de dormir.")
    
    nombre_cortisol = st.text_input("👤 Nombre o Identificador para el Test de Cortisol:", placeholder="Ej: Rosa, Juan...")
    
    st.markdown("---")
    horas_trabajo = st.slider("⏱️ Horas totales de trabajo (en casa o fuera):", 0, 16, 8)
    tipo_deporte = st.selectbox("🏃‍♂️ Actividad física o deporte realizado hoy:", [
        "Ninguno (sedentarismo)", 
        "Suave (paseo, estiramientos, yoga)", 
        "Moderado (gym, correr suave, natación)", 
        "Intenso / De competición a última hora"
    ])
    tipo_comida = st.selectbox("🍔 Alimentación principal del día:", [
        "Equilibrada, ligera y a sus horas", 
        "Comida rápida, ultraprocesados o picoteo constante", 
        "Cena muy copiosa o pesada cerca de la hora de dormir"
    ])
    discusiones = st.radio("🗣️ ¿Has tenido discusiones, tensiones o conflictos emocionales hoy?", [
        "No, día tranquilo", 
        "Algún roce menor o tensión leve", 
        "Sí, discusiones intensas o altercados importantes"
    ])
    ocio_desconexion = st.radio("🎮 Tiempo dedicado al ocio y desconexión real:", [
        "Más de 1 hora de desconexión plena", 
        "Entre 30 minutos y 1 hora", 
        "Menos de 30 minutos o nada de tiempo libre"
    ])

    if st.button("🧬 Calcular y Añadir Índice de Cortisol al Día", type="primary", use_container_width=True):
        if not nombre_cortisol.strip():
            st.warning("⚠️ Por favor, introduce tu nombre para guardar el test.")
        else:
            puntos_cortisol = 20
            if horas_trabajo > 10: puntos_cortisol += 25
            elif horas_trabajo > 8: puntos_cortisol += 15
            elif horas_trabajo <= 5: puntos_cortisol += 5
            
            if tipo_deporte == "Intenso / De competición a última hora": puntos_cortisol += 25
            elif tipo_deporte == "Ninguno (sedentarismo)": puntos_cortisol += 15
            elif tipo_deporte == "Moderado (gym, correr suave, natación)": puntos_cortisol -= 10
            elif tipo_deporte == "Suave (paseo, estiramientos, yoga)": puntos_cortisol -= 15
            
            if tipo_comida == "Cena muy copiosa o pesada cerca de la hora de dormir": puntos_cortisol += 25
            elif tipo_comida == "Comida rápida, ultraprocesados o picoteo constante": puntos_cortisol += 15
            else: puntos_cortisol -= 10
            
            if discusiones == "Sí, discusiones intensas o altercados importantes": puntos_cortisol += 30
            elif discusiones == "Algún roce menor o tensión leve": puntos_cortisol += 15
            else: puntos_cortisol -= 10
            
            if ocio_desconexion == "Menos de 30 minutos o nada de tiempo libre": puntos_cortisol += 20
            elif ocio_desconexion == "Entre 30 minutos y 1 hora": puntos_cortisol += 5
            else: puntos_cortisol -= 15
            
            indice_cortisol = max(5, min(100, puntos_cortisol))
            
            hoy_fecha = datetime.now().strftime("%Y-%m-%d")
            nombre_limpio = nombre_cortisol.strip().title()

            data = load_data()
            
            registro_existente = None
            for d in data:
                if d.get("name") == nombre_limpio and str(d.get("date", "")).startswith(hoy_fecha):
                    registro_existente = d
                    break

            if registro_existente:
                registro_existente["cortisol_index"] = indice_cortisol
                st.success(f"✅ ¡Índice de Cortisol ({indice_cortisol}/100) añadido al registro de hoy para **{nombre_limpio}**!")
            else:
                entry_cortisol = {
                    "name": nombre_limpio,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "hours": 7.5,
                    "stress": 3,
                    "wakeups": 0,
                    "bedtime": "23:00",
                    "supplements": "No especificado",
                    "screens": False,
                    "heavy_dinner": False,
                    "caffeine": False,
                    "exercise": False,
                    "score": 75,
                    "cortisol_index": indice_cortisol
                }
                data.append(entry_cortisol)
                st.success(f"✅ ¡Test de Cortisol guardado con éxito para **{nombre_limpio}**!")

            save_data(data)
            st.markdown("---")
            
            col_c1, col_c2 = st.columns([1, 2])
            with col_c1:
                if indice_cortisol <= 35:
                    st.markdown(f"<div class='metric-card' style='border-color:#22c55e;'><p style='color:#9ca3af;margin:0;'>ÍNDICE CORTISOL</p><h1 style='color:#22c55e;margin:5px 0;'>{indice_cortisol}/100</h1><p style='color:#22c55e;margin:0;font-size:12px;'>Nivel Bajo y Saludable 🌿</p></div>", unsafe_allow_html=True)
                elif indice_cortisol <= 65:
                    st.markdown(f"<div class='metric-card' style='border-color:#eab308;'><p style='color:#9ca3af;margin:0;'>ÍNDICE CORTISOL</p><h1 style='color:#eab308;margin:5px 0;'>{indice_cortisol}/100</h1><p style='color:#eab308;margin:0;font-size:12px;'>Nivel Moderado ⚠️</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='metric-card' style='border-color:#f43f5e;'><p style='color:#9ca3af;margin:0;'>ÍNDICE CORTISOL</p><h1 style='color:#f43f5e;margin:5px 0;'>{indice_cortisol}/100</h1><p style='color:#f43f5e;margin:0;font-size:12px;'>Nivel Alto / Alerta 🔴</p></div>", unsafe_allow_html=True)
            
            with col_c2:
                st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                st.write("**Análisis de la Carga de Cortisol Diario:**")
                if indice_cortisol <= 35:
                    st.success("Tus hábitos diarios han mantenido la hormona del estrés bajo control.")
                elif indice_cortisol <= 65:
                    st.warning("Se detecta una sobrecarga moderada debido a tus horas de trabajo o hábitos.")
                else:
                    st.error("¡Alerta de picos de cortisol! Esto interferirá con la melatonina.")
                st.markdown("</div>", unsafe_allow_html=True)


# --- PESTAÑA 3: HISTORIAL E INFORMES ---
with tab3:
    st.subheader("👥 Informes Globales y Gráficos por Persona")
    data = load_data()
    if not data:
        st.info("Aún no hay registros guardados en la aplicación.")
    else:
        nombres_disponibles = sorted(list(set(str(d.get("name", "")) for d in data if d.get("name"))))
        persona_seleccionada = st.selectbox("Selecciona una persona para generar su informe completo:", nombres_disponibles)
        
        registros_persona = [d for d in data if str(d.get("name", "")) == persona_seleccionada]
        
        st.markdown("---")
        st.markdown(f"### 📄 Informe Clínico Global: **{persona_seleccionada}**")
        
        total_p = len(registros_persona)
        media_horas_p = sum(float(d.get("hours", 7)) for d in registros_persona) / total_p
        media_score_p = sum(float(d.get("score", 70)) for d in registros_persona) / total_p
        media_estres_p = sum(float(d.get("stress", 3)) for d in registros_persona) / total_p
        
        cp1, cp2, cp3 = st.columns(3)
        cp1.metric("Total Registros", total_p)
        cp2.metric("Sleep Score Promedio", f"{media_score_p:.1f} / 100")
        cp3.metric("Media de Horas", f"{media_horas_p:.1f} h")
        
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(f"#### 🩺 Evaluación y Análisis de Causas para {persona_seleccionada}")
        if media_score_p >= 75:
            st.success(f"✅ **Estado general óptimo:** {persona_seleccionada} muestra una sólida estabilidad en su descanso.")
        elif media_score_p >= 50:
            st.warning(f"⚠️ **Descanso fluctuante:** El descanso de {persona_seleccionada} se ve interrumpido de manera intermitente.")
        else:
            st.error(f"🔴 **Alerta por fatiga:** Los registros de {persona_seleccionada} indican una merma continuada.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader(f"📈 Gráficos de Evolución Temporal ({persona_seleccionada})")
        
        fechas_p = [str(d.get("date", ""))[-11:] for d in registros_persona]
        scores_p = [float(d.get("score", 70)) for d in registros_persona]
        estres_p = [float(d.get("stress", 3)) for d in registros_persona]

        fig, (g1, g2) = plt.subplots(2, 1, figsize=(8, 6), facecolor='#0e1117')
        
        g1.set_facecolor('#161b22')
        g1.plot(fechas_p, scores_p, marker="o", color="#38bdf8", linewidth=2.5, label="Sleep Score (0-100)")
        g1.set_title("Evolución del Sleep Score", color="#ffffff", fontsize=11, fontweight='bold', pad=10)
        g1.set_ylim(0, 105)
        g1.tick_params(colors='#8b949e', labelsize=8)
        g1.grid(True, linestyle=":", alpha=0.3, color="#8b949e")
        g1.legend(facecolor='#161b22', edgecolor='none', labelcolor='#ffffff', loc='lower right')

        g2.set_facecolor('#161b22')
        g2.bar(fechas_p, estres_p, color="#f43f5e", alpha=0.8, width=0.4, label="Nivel de Estrés (1-5)")
        g2.set_title("Nivel de Estrés Registrado", color="#ffffff", fontsize=11, fontweight='bold', pad=10)
        g2.set_ylim(0, 5.5)
        g2.tick_params(colors='#8b949e', labelsize=8)
        g2.grid(True, linestyle=":", alpha=0.3, color="#8b949e")
        g2.legend(facecolor='#161b22', edgecolor='none', labelcolor='#ffffff', loc='upper right')

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("---")
        df_export = pd.DataFrame(registros_persona)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar copia de seguridad (CSV) de esta persona",
            data=csv_data,
            file_name=f"informe_sueño_{persona_seleccionada}.csv",
            mime="text/csv"
        )

        st.markdown("---")
        # --- ZONA DE BORRADO ---
        with st.expander("🗑️ Zona de Gestión y Borrado de Datos"):
            st.warning("⚠️ Opciones de eliminación permanente de registros:")
            
            if st.button(f"🗑️ Borrar todos los registros de {persona_seleccionada}", type="secondary"):
                nuevo_data = [d for d in data if str(d.get("name", "")) != persona_seleccionada]
                save_data(nuevo_data)
                st.success(f"¡Registros de {persona_seleccionada} borrados con éxito! Recarga la página.")
                st.rerun()

            if st.button("⚠️ Borrar TODO el historial de la aplicación", type="primary"):
                save_data([])
                st.success("¡Historial completamente vaciado! Recarga la página.")
                st.rerun()


# --- PESTAÑA 4: CIENCIA Y PAUTAS AVANZADAS ---
with tab4:
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
