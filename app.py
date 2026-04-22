import streamlit as st
from db import init_db
from chain import run_pipeline
from dashboard import show_dashboard

st.set_page_config(page_title="Text to SQL", page_icon="🧠")
st.title("🧠 Text to SQL Query")
st.write("Ask a question in plain English and get SQL results!")

init_db()

query = st.text_input("💬 Ask your question:", placeholder="e.g. What is the total sales amount?")

if st.button("🚀 Run"):
    if not query:
        st.warning("Please enter a question!")
    else:
        with st.spinner("Thinking..."):
            sql, result = run_pipeline(query)

        st.subheader("📝 Generated SQL")
        st.code(sql, language="sql")

        st.subheader("📊 Result")
        if isinstance(result, str):
            st.error(f"Error: {result}")
        else:
            st.write(result)
            chart = show_dashboard(result)
            if chart:
                df, fig = chart
                st.subheader("📈 Chart")
                st.pyplot(fig)