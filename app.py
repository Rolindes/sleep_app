import json
import os
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

DATA_FILE = "sleep_data_web.json"

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

st.set_page_config(page_title="SleepArchitect", page_icon="🌙", layout="centered")

st.title("🌙 SleepArchitect - Tu Asistente de Sueño Avanzado")
st.write("Registra tus hábitos diarios, analiza tus estadísticas y recibe recomendaciones personalizadas para descansar mejor.")

# Pestañas de la aplicación
tab1, tab2, tab3, tab4 = st.tabs(["📝 Registro Diario", "📋 Historial", "📊 Estadísticas", "💡 Pautas y Consejos"])

with tab1:
    st.subheader("¿Cómo ha ido tu noche?")
    
    col1, col2 = st.columns(2)
    with col1:
        horas = st.slider("Horas de sueño:", 1.0, 12.0, 7.5, 0.5)
        estres = st.selectbox("Nivel de estrés antes de dormir (1-5):", [1, 2, 3, 4, 5])
    with col2:
        hora_acostarse = st.text_input("Hora aproximada de acostarte (ej. 23:30):", "23:30")
        suplemento = st.checkbox("💊 ¿Tomé melatonina o suplemento natural?")
    
    pantallas = st.checkbox("📱 ¿Usé pantallas tarde (-30 min antes)?")
    cafe = st.checkbox("☕ ¿Tomé café o alcohol por la tarde/noche?")
    
    if st.button("Guardar Registro del Día", type="primary"):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hours": horas,
            "stress": estres,
            "bedtime": hora_acostarse,
            "supplement": suplemento,
            "screens": pantallas,
            "coffee": cafe
        }
        
        data = load_data()
        data = [d for d in data if d["date"] != entry["date"]]
        data.append(entry)
        save_data(data)
        
        st.success("¡Registro guardado con éxito! Revisa tu historial y recomendaciones.")
        
        # Recomendación automática inmediata (Opción 2)
        st.info("💡 **Análisis rápido de tu noche:**")
        if horas < 6:
            st.warning("⚠️ Has dormido pocas horas. Intenta buscar un hueco para descansar hoy o acostarte antes.")
        elif horas >= 7.5:
            st.warning("🌟 ¡Excelente cantidad de horas de sueño! Sigue manteniendo este hábito.")
            
        if estres >= 4:
            st.error("⚠️ Tu nivel de estrés era elevado antes de dormir. Te recomendamos técnicas de respiración o lectura ligera.")
        if pantallas:
            st.info("📱 El uso de pantallas antes de dormir reduce la melatonina natural. Prueba a apagarlas 30 min antes hoy.")

with tab2:
    st.subheader("📋 Historial de Registros Anteriores")
    data = load_data()
    if not data:
        st.info("Aún no hay registros guardados. ¡Empieza en la pestaña de Registro Diario!")
    else:
        # Mostrar tabla limpia con los datos
        st.write("Aquí puedes ver todos tus registros guardados a largo plazo:")
        for d in reversed(data):
            with st.expander(f"📅 Fecha: {d['date']} — {d['hours']} horas dormidas"):
                st.write(f"• **Hora de acostarse:** {d.get('bedtime', 'No especificada')}")
                st.write(f"• **Nivel de estrés:** {d['stress']}/5")
                st.write(f"• **¿Usó pantallas?:** {'Sí' if d['screens'] else 'No'}")
                st.write(f"• **¿Tomó café/alcohol?:** {'Sí' if d['coffee'] else 'No'}")
                st.write(f"• **¿Tomó suplemento?:** {'Sí' if d.get('supplement', False) else 'No'}")

with tab3:
    st.subheader("📊 Tus Estadísticas de Sueño")
    data = load_data()
    if not data:
        st.info("Aún no hay datos suficientes para mostrar gráficos.")
    else:
        dates = [d["date"][-5:] for d in data[-10:]]
        hours = [d["hours"] for d in data[-10:]]
        
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(dates, hours, marker="o", color="#3498db", linewidth=2.5, markersize=7)
        ax.set_title("Evolución de tus Horas de Sueño", color="white", pad=10)
        ax.set_ylabel("Horas", color="white")
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.grid(True, linestyle="--", alpha=0.3)
        st.pyplot(fig)

with tab4:
    st.subheader("💡 Pautas Profesionales contra el Insomnio")
    st.markdown("""
    * **Regla de los 20 minutos:** Si llevas más de 20 minutos en la cama sin poder dormir, levántate y ve a otra habitación con luz tenue a leer algo aburrido.
    * **Control de temperatura:** Mantén tu dormitorio fresco (entre 18°C y 20°C). El cuerpo necesita bajar su temperatura interna para alcanzar el sueño profundo.
    * **Exposición solar matutina:** Intenta que te dé luz natural en la cara durante los primeros 30 minutos tras despertar para sincronizar tu reloj biológico.
    * **Cena ligera:** Evita cenas pesadas, alcohol o cafeína al menos 4 o 5 horas antes de irte a la cama.
    """)
