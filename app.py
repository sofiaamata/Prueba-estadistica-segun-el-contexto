import streamlit as st
import json
import requests

# ------------------------------------------------------
#  https://raw.githubusercontent.com/sofiaamata/Prueba-estadistica-segun-el-contexto/refs/heads/main/items.json
# ------------------------------------------------------
url_json = "https://raw.githubusercontent.com/sofiaamata/Prueba-estadistica-segun-el-contexto/refs/heads/main/items.json"

# ------------------------------------------------------
#   Cargar items desde JSON online
# ------------------------------------------------------
@st.cache_data
def cargar_items(url):
    response = requests.get(url)
    return json.loads(response.text)

items = cargar_items(url_json)

# ------------------------------------------------------
#   Inicializar estado
# ------------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "mostrar_feedback" not in st.session_state:
    st.session_state.mostrar_feedback = False
if "respuesta_usuario" not in st.session_state:
    st.session_state.respuesta_usuario = None

# ------------------------------------------------------
#   Interfaz
# ------------------------------------------------------

st.title("📊 Evaluación: Selección de Pruebas Estadísticas")

# Fin del cuestionario
if st.session_state.indice >= len(items):
    st.success(f"¡Has terminado! Tu puntaje final es: **{st.session_state.puntaje} / {len(items)}** 🎉")
    st.balloons()
    st.stop()

pregunta = items[st.session_state.indice]

st.write(f"### Pregunta {st.session_state.indice + 1} de {len(items)}")
st.write(pregunta["pregunta"])

respuesta = st.radio(
    "Selecciona una opción:",
    pregunta["opciones"],
    key=f"op_{st.session_state.indice}"
)

if st.button("Responder"):
    st.session_state.respuesta_usuario = respuesta
    st.session_state.mostrar_feedback = True

# Retroalimentación inmediata
if st.session_state.mostrar_feedback:
    correcta = pregunta["correcta"]
    opcion_correcta = pregunta["opciones"][correcta]

    if respuesta == opcion_correcta:
        st.success("✔️ ¡Correcto!")
        st.session_state.puntaje += 1
    else:
        st.error(f"❌ Incorrecto. La respuesta correcta es: **{opcion_correcta}**")

    st.info(f"**Explicación:** {pregunta['explicacion']}")

    if st.button("Siguiente"):
        st.session_state.indice += 1
        st.session_state.mostrar_feedback = False
        st.session_state.respuesta_usuario = None
        st.rerun()
