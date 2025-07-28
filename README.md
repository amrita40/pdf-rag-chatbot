# PDF RAG Chatbot

A powerful, interactive chatbot that lets you ask questions about your PDF documents using Retrieval-Augmented Generation (RAG), OpenRouter LLMs, and a Streamlit frontend.

![PDF RAG Chatbot Banner](https://github.com/amrita40/pdf-rag-chatbot/blob/main/Screenshot%202025-07-29%20035747.png?raw=true) <!-- Replace with your banner or main screenshot -->

---

## 🚀 Features

- **Ask Anything:** Query your PDF documents in natural language.
- **RAG Pipeline:** Combines vector search and LLMs for accurate, context-aware answers.
- **OpenRouter Integration:** Uses OpenRouter API for cost-effective, flexible LLM access.
- **Streamlit UI:** Clean, modern web interface for instant Q&A.
- **Easy Deployment:** Run locally or deploy to Streamlit Cloud.
- **Multi-PDF Support:** Easily extend to multiple documents.
- **Web Search Augmentation:** (Optional) Integrate web search for even richer answers.

---

## 🧠 How It Works

1. **PDF Ingestion:** Your PDF(s) are split into chunks and embedded using HuggingFace models.
2. **Vectorstore:** Chunks are stored in a ChromaDB vectorstore for fast similarity search.
3. **RAG Pipeline:** When you ask a question, the system:
    - Retrieves relevant chunks from the vectorstore.
    - Optionally augments with web search results.
    - Passes context and your question to an LLM via OpenRouter.
    - Grades and refines the answer for accuracy.
4. **Frontend:** Streamlit provides a simple chat interface for interaction.

---

## 🖼️ Screenshots

| Ask a Question | 

| ![Ask](https://github.com/amrita40/pdf-rag-chatbot/blob/main/Screenshot%202025-07-29%20040203.png?raw=true) | 


|Get an Answer |
![Answer](https://github.com/amrita40/pdf-rag-chatbot/blob/main/Screenshot%202025-07-29%20000445.png?raw=true) |

---

## 🎬 Demo

[![Watch the demo](screenshots/demo_thumbnail.png)](https://youtu.be/YOUR_DEMO_VIDEO_LINK)  
*Click the image above to watch a demo video!*

---

## 🛠️ Tech Stack

- **Python 3.10+**
- [LangChain](https://github.com/langchain-ai/langchain) (RAG pipeline)
- [OpenRouter](https://openrouter.ai/) (LLM API)
- [Streamlit](https://streamlit.io/) (Frontend)
- [ChromaDB](https://www.trychroma.com/) (Vectorstore)
- [HuggingFace Transformers](https://huggingface.co/) (Embeddings)
- [Tavily](https://tavily.com/) (Optional: Web search)

---

## 🛠️ Setup & Usage

### 1. Clone the repo
```sh
git clone https://github.com/amrita40/pdf-rag-chatbot.git
cd pdf-rag-chatbot
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```

### 3. Add your `.env` file
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Add your PDF(s)
Place your PDF files in the appropriate folder (see project structure).

### 5. Build the vectorstore (first run only)
```sh
python main.py
```

### 6. Launch the Streamlit app
```sh
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📝 Project Structure

```
pdf-rag-chatbot/
│
├── adaptive_rag_pdf/
│   ├── graph/
│   │   ├── nodes.py
│   │   └── build_graph.py
│   ├── vectorstore/
│   │   └── build_index.py
│   └── main.py
├── streamlit_app.py
├── requirements.txt
├── .env
├── .gitignore
├── screenshots/
│   ├── banner.png
│   ├── ask.png
│   ├── answer.png
│   └── demo_thumbnail.png
└── README.md
```

---

## ⚙️ Customization

- **Change the LLM:** Edit the model name in `nodes.py` to use any OpenRouter-supported model.
- **Add More PDFs:** Place additional PDFs in your data folder and rebuild the vectorstore.
- **Web Search:** Enable or disable web search augmentation in the pipeline.
- **UI:** Customize the Streamlit interface for your branding or workflow.

---


## ❓ FAQ

**Q: Can I use this with any PDF?**  
A: Yes! Just add your PDF(s) and rebuild the vectorstore.

**Q: Is my data private?**  
A: All processing happens on your machine or server. Only LLM queries are sent to OpenRouter.

**Q: Can I use other LLMs?**  
A: Yes, any model supported by OpenRouter can be used.

**Q: How do I add authentication?**  
A: Use Streamlit’s [authentication recipes](https://docs.streamlit.io/knowledge-base/deploy/authentication) or deploy behind a secure proxy.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenRouter](https://openrouter.ai/)
- [Streamlit](https://streamlit.io/)
- [ChromaDB](https://www.trychroma.com/)
- [HuggingFace](https://huggingface.co/)



---

**Enjoy asking questions to your PDFs!**
