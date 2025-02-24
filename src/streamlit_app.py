# streamlit_app.py

import streamlit as st
import requests

st.title("Evidence-Based AI Research Assistant (EBARA)")

question = st.text_input("Introduce your question about diseases, treatments or pharmaceuticals:")

if st.button("Search evidence"):
    if question.strip() != "":
        with st.spinner("Searching evidence and generating response..."):
            try:
                response = requests.post("http://localhost:8000/query", json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### Generated Response:")
                    st.write(data["response"])
                    st.markdown("### References:")
                    for title in data["references"]:
                        st.write(f"- {title}")
                else:
                    st.error("Error in the query: " + response.text)
            except Exception as e:
                st.error("Error connecting to the server: " + str(e))
    else:
        st.warning("Please, enter a question.")
