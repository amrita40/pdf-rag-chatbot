from vectorstore.build_index import build_vectorstore
from graph.build_graph import get_graph

# First time: build index
print("Building PDF vectorstore...")
build_vectorstore()

# Run RAG
graph = get_graph()

question = input("Ask a question: ")
result = graph.invoke({"question": question})

print("\n✅ Final Answer:\n", result.get("answer", "No answer returned."))
