import streamlit as st

st.title("PDF Q&A Chatbot")
st.write("Ask questions about your PDF. Powered by your RAG pipeline.")

question = st.text_input("Ask a question:")

if st.button("Submit") and question:
    with st.spinner("Thinking..."):
        from graph.build_graph import get_graph  # Import here to avoid slow startup
        graph = get_graph()
        result = graph.invoke({"question": question})
        st.write("**Answer:**", result.get("answer", "No answer returned."))