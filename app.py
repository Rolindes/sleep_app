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

st.title("🌙 SleepArchitect - Tu Asistente de Sueño")
st.write("Registra tus hábitos diarios para mejorar tu descanso.")

tab1, tab2, tab3 = st.tabs(["📝 Registro Diario", "📊 Estadísticas", "💡 Pautas"])

with tab1:
    st.subheader("¿Cómo ha ido tu noche?")
    horas = st.slider("Horas de sueño:", 1.0, 12.0, 7.5, 0.5)
    estres = st.selectbox("Nivel de estrés antes de dormir (1-5):", [1, 2, 3, 4, 5])
    pantallas = st.checkbox("¿Usé pantallas tarde (-30 min)?")
    cafe = st.checkbox("¿Tomé café o alcohol por la tarde?")
    
    if st.button("Guardar Registro"):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hours": horas,
            "stress": estres,
            "screens": pantallas,
            "coffee": cafe
        }
        data = load_data()
        data = [d for d in data if d["date"] != entry["date"]]
        data.append(entry)
        save_data(data)
        st.success("¡Guardado con éxito! Revisa la pestaña de estadísticas.")

with tab2:
    st.subheader("Tus Estadísticas")
    data = load_data()
    if not data:
        st.info("Aún no hay registros. ¡Haz tu primer registro en la pestaña anterior!")
    else:
        dates = [d["date"][-5:] for d in data[-7:]]
        hours = [d["hours"] for d in data[-7:]]
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(dates, hours, marker="o", color="#3498db", linewidth=2.5)
        ax.set_title("Evolución de tus Horas de Sueño", color="white")
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        st.pyplot(fig)

with tab3:
    st.subheader("Pautas contra el Insomnio")
    st.markdown("""
    * **Regla de los 20 minutos:** Si no duermes, levántate a otra habitación con luz tenue a leer algo aburrido.
    * **Temperatura:** Mantén la habitación fresca (18°C - 20°C) para ayudar a tu cuerpo a relajarse.
    * **Luz solar:** Toma luz natural en la cara los primeros 30 minutos tras despertar.
    """)
