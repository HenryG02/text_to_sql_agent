import streamlit as st

st.title("Text-to-SQL Agent")

st.header(
    "Ask a question (in Portuguese or in English) about Henry's Rubik's Cubes solves!"
)

if prompt := st.chat_input(""):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown("Lorem ipsum")
