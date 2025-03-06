# streamlit_app.py

import streamlit as st
import requests
import os
st.title("Evidence-Based AI Research Assistant (EBARA)")

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

question = st.text_input("Introduce your question about diseases, treatments or pharmaceuticals:", value="Search articles about lung cancer published after 2020")

if st.button("Search evidence"):
    if question.strip() != "":
        with st.spinner("Searching evidence and generating response..."):
            try:
                response = requests.post(f"{backend_url}/query", json={"question": question})
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
