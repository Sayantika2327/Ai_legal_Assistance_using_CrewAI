# ⚖️ AI Legal Assistant using CrewAI

An intelligent multi-agent AI system that analyzes legal problems and automatically generates:

- Relevant IPC sections
- Supporting legal precedents
- Structured legal complaint draft
- Context-aware chatbot assistance

This project makes legal knowledge accessible to everyone using AI.

---

## 🚀 Features

✅ Multi-Agent Legal Workflow (CrewAI)  
✅ RAG-based IPC Section Retrieval (LangChain + ChromaDB)  
✅ Real-time Legal Precedent Search (Tavily API)  
✅ Automated Legal Document Drafting  
✅ Context-aware Chatbot (Groq LLaMA 3.3)  
✅ Interactive Streamlit Web Interface  

---

## 🧠 System Architecture

User Input  
⬇  
Case Intake Agent  
⬇  
IPC Section Agent (RAG Search)  
⬇  
Legal Precedent Agent (Tavily Search)  
⬇  
Document Drafting Agent  
⬇  
Final Legal Report + Chatbot Assistance

---

## 🤖 AI Agents Used

### 1️⃣ Case Intake Agent
Extracts structured legal details from user input.

### 2️⃣ IPC Section Agent
Retrieves relevant IPC sections using vector similarity search.

### 3️⃣ Legal Precedent Agent
Finds real-world court judgments using Tavily Search API.

### 4️⃣ Legal Drafting Agent
Generates a structured legal complaint document.

---

## 🛠️ Tech Stack

- CrewAI
- LangChain
- ChromaDB
- Tavily API
- Groq LLaMA 3.3
- Streamlit
- Python

---

## 📂 Project Structure

AI-legal-Assistance/
│
├── agents/
├── tasks/
├── tools/
├── chroma_vectordb/
├── app.py
├── crew.py
├── ipc.json
├── requirements.txt
└── .env

---

## ⚙️ Installation

Clone the repository:

git clone https://github.com/Sayantika2327/Ai_legal_Assistance_using_CrewAI.git

Move into project directory:

cd Ai_legal_Assistance_using_CrewAI

Install dependencies:

pip install -r requirements.txt

---

## 🔑 Environment Variables

Create a `.env` file and add:

GROQ_API_KEY=your_key_here  
TAVILY_API_KEY=your_key_here

---

## ▶️ Run the Application

streamlit run app.py

---

## 🎬 Demo Video

(Add your demo video link here)

Example:

https://youtu.be/your-demo-video-link

---

## 📊 Example Workflow

User enters:

"My employer has not paid my salary for 3 months."

System returns:

✔ Applicable IPC sections  
✔ Supporting legal precedents  
✔ Draft complaint document  
✔ Chatbot explanation support  

---

## 🔮 Future Improvements

- Multi-jurisdiction support
- Voice-based legal query input
- Lawyer verification layer
- Mobile app deployment
- Fine-tuned legal LLM

---

## 👩‍💻 Authors

Sayantika Chowdhury  
Ishita Shrivastava
