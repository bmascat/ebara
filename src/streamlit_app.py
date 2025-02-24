# streamlit_app.py

import streamlit as st
import requests

st.title("Evidence-Based AI Research Assistant (EBARA)")

question = st.text_input("Introduce tu pregunta sobre enfermedades, tratamientos o fármacos:")

if st.button("Buscar evidencia"):
    if question.strip() != "":
        with st.spinner("Buscando evidencia y generando respuesta..."):
            try:
                response = requests.post("http://localhost:8000/query", json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### Respuesta Generada:")
                    st.write(data["response"])
                    st.markdown("### Referencias:")
                    for title in data["references"]:
                        st.write(f"- {title}")
                else:
                    st.error("Error en la consulta: " + response.text)
            except Exception as e:
                st.error("Error al conectar con el servidor: " + str(e))
    else:
        st.warning("Por favor, ingresa una pregunta.")
