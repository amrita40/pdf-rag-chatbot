from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

from langchain_core.runnables import RunnableLambda, RunnableMap
from config import CHROMA_DIR

# Load environment variables
load_dotenv()
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))  # Remove or comment out after confirming

# Initialize LLM for OpenRouter endpoint (OpenAI-compatible)
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-4o",
    max_tokens=512  
)

# 1. Router
router = RunnableLambda(
    lambda x: {"next": "vectorstore"} if "pdf" in x["question"].lower() else {"next": "web_search"}
)

# 2. Vectorstore Retrieval
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory=CHROMA_DIR, embedding_function=embedding_model
)
retriever = vectorstore.as_retriever()

retrieval_node = RunnableMap({
    "docs": lambda x: retriever.invoke(x["question"]),
    "question": lambda x: x["question"]
})

# 3. Grade Document Relevance
retrieval_grader_prompt = ChatPromptTemplate.from_messages([
    ("system", "Are the docs relevant to the question? Answer yes or no."),
    ("human", "Q: {question}\nDocs:\n{docs}")
])

def check_relevance(x):
    response = llm.invoke(retrieval_grader_prompt.invoke({
        "question": x["question"],
        "docs": "\n".join(d.page_content for d in x["docs"])
    }))
    return {"relevance": "relevant" if "yes" in response.content.lower() else "irrelevant"}

grade_retrieval_node = RunnableLambda(check_relevance)

# 4. Rewrite Node (to improve retrieval)
rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system", "Rewrite the question to retrieve better context."),
    ("human", "{question}")
])
rewrite_node = rewrite_prompt | llm | (lambda x: {"question": x.content})

# 5. Web Search Node (Tavily)
web_tool = TavilySearch()
web_search_node = RunnableLambda(
    lambda x: {
        "docs": [r["content"] for r in web_tool.invoke({"query": x["question"]}) if "content" in r],
        "question": x["question"]
    }
)

# 6. Generate Answer
generation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Use the following documents to answer the question.\n\n{docs}"),
    ("human", "{question}")
])

def format_docs(docs):
    return "\n\n".join([
        d.page_content if hasattr(d, "page_content") else str(d)
        for d in docs
    ])

generate_answer = RunnableLambda(lambda x: {
    "answer": llm.invoke(generation_prompt.invoke({
        "docs": format_docs(x["docs"]),
        "question": x["question"]
    })).content,
    "question": x["question"],
    "docs": x["docs"]
})

# 7. Grade Answer
grade_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "Does the answer correctly answer the question? Yes or No."),
    ("human", "Q: {question}\nA: {answer}")
])

def check_answer_quality(x):
    response = llm.invoke(grade_answer_prompt.invoke({
        "question": x["question"],
        "answer": x["answer"]
    }))
    return {"answer_quality": "correct" if "yes" in response.content.lower() else "incorrect"}

grade_answer = RunnableLambda(check_answer_quality)