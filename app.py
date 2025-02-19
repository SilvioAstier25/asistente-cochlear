import streamlit as st
import openai

import os
openai.api_key = os.getenv("OPENAI_API_KEY")  # Cargar clave desde variable de entorno

# 🖼️ Agregar el logotipo en la parte superior
st.image("logo_cochlear.png", width=250)

# Definir el contexto del asistente
contexto = "Eres un asistente especializado en implantes cocleares de Cochlear. Responde preguntas basándote en la información oficial de Cochlear, explicando sus productos y beneficios. Usa un tono informativo, confiable y alineado con la misión de Cochlear."

# 🎨 Estilos personalizados para mantener el look & feel correcto
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7D275;
        padding: 20px;
    }
    .title {
        text-align: center;
        color: #3A2D1E;
        font-size: 28px;
        font-weight: bold;
    }
    .response-box {
        background-color: #FCE8C6;
        padding: 10px;
        border-radius: 10px;
        font-size: 16px;
        color: #3A2D1E;
        margin-top: 10px;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        font-size: 16px;
        border: 2px solid #AF813F;
        border-radius: 10px;
        padding: 8px;
    }
    .stButton>button {
        font-size: 16px;
        background-color: #3A2D1E;
        color: white;
        padding: 10px;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #AF813F;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏷️ Título del asistente con leyenda sobre IA
st.markdown("<h1 class='title'>🦻 Asistente de Implantes Cocleares</h1>", unsafe_allow_html=True)
st.write("Este asistente utiliza **Inteligencia Artificial** para responder preguntas sobre implantes cocleares. Puedes escribir tu propia consulta o seleccionar una pregunta predefinida.")

# 📌 Inicializar variables de sesión correctamente
if "respuesta" not in st.session_state:
    st.session_state.respuesta = ""
if "pregunta_manual" not in st.session_state:
    st.session_state.pregunta_manual = ""
if "pregunta_predefinida" not in st.session_state:
    st.session_state.pregunta_predefinida = "Selecciona una pregunta predefinida (opcional)"
if "modo_predefinido" not in st.session_state:
    st.session_state.modo_predefinido = False  # Controla si el usuario está en modo preguntas predefinidas

# 📌 Preguntas predefinidas dentro del mismo input
preguntas_predefinidas = [
    "Selecciona una pregunta predefinida (opcional)",
    "¿Qué es un implante coclear?",
    "¿Cómo funciona un implante coclear?",
    "¿Cómo es la cirugía?",
    "¿Cuánto dura la recuperación?",
    "¿Cuáles son los beneficios?",
    "¿Quiénes pueden recibir un implante coclear?"
]

# 📌 Botón para activar preguntas predefinidas (limpia input manual)
if st.button("📝 Usar Preguntas Predefinidas"):
    st.session_state.pregunta_manual = ""  # Borra el input manual
    st.session_state.pregunta_predefinida = "Selecciona una pregunta predefinida (opcional)"
    st.session_state.modo_predefinido = True  # Activa modo predefinido

# 📌 Selector de preguntas predefinidas
pregunta_predefinida = st.selectbox("📌 Preguntas frecuentes:", preguntas_predefinidas, index=preguntas_predefinidas.index(st.session_state.pregunta_predefinida))

# 📌 Input manual de preguntas (se desactiva si se usa el selector)
pregunta_manual = st.text_input("✍ O escribe tu propia pregunta:", value=st.session_state.pregunta_manual)

# 📌 Función para obtener respuesta de GPT-3.5-Turbo
def obtener_respuesta(pregunta):
    if not pregunta.strip():
        return ""
    respuesta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": pregunta}
        ]
    )
    return respuesta.choices[0].message.content

# 📌 Lógica para alternar entre pregunta manual y predefinida sin conflictos
if pregunta_manual.strip():
    st.session_state.pregunta_predefinida = "Selecciona una pregunta predefinida (opcional)"
    st.session_state.modo_predefinido = False  # Desactiva modo predefinido
    st.session_state.pregunta_manual = pregunta_manual
elif pregunta_predefinida != "Selecciona una pregunta predefinida (opcional)":
    st.session_state.pregunta_manual = ""  # Borrar input manual
    st.session_state.modo_predefinido = True  # Activa modo predefinido
    st.session_state.pregunta_predefinida = pregunta_predefinida

# 📌 Botón para enviar la pregunta
if st.button("✅ Enviar"):
    if st.session_state.pregunta_manual.strip():
        st.session_state.respuesta = obtener_respuesta(st.session_state.pregunta_manual)
    elif st.session_state.pregunta_predefinida != "Selecciona una pregunta predefinida (opcional)":
        st.session_state.respuesta = obtener_respuesta(st.session_state.pregunta_predefinida)
    else:
        st.session_state.respuesta = "⚠️ Por favor, selecciona una pregunta o escribe una consulta."

# 📌 Mostrar respuesta siempre debajo del input
if st.session_state.respuesta:
    st.markdown(f"<div class='response-box'><b>Respuesta:</b><br>{st.session_state.respuesta}</div>", unsafe_allow_html=True)
