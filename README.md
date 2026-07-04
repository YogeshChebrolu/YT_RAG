# YT_RAG

A Retrieval-Augmented Generation (RAG) system over YouTube video content — extract transcripts and frames from videos, index them in a vector store, and chat with an LLM grounded in that content.

This is a monorepo containing both the backend and frontend.

## Structure

```
.
├── backend/    # Python RAG backend (FastAPI, vector store, transcript & frame extraction, LLM services)
└── frontend/   # React + TypeScript + Vite web/extension UI
```

## Backend

FastAPI service handling video processing, transcript extraction, frame extraction, embeddings/vector search, and chat. See [`backend/README.md`](backend/README.md) for setup and details.

```bash
cd backend
# create a .env with your keys (SUPABASE_URL, SUPABASE_KEY, LLM API keys, etc.)
pip install -r requirements.txt
python main.py
```

## Frontend

React + TypeScript + Vite app. See [`frontend/README.md`](frontend/README.md).

```bash
cd frontend
npm install
npm run dev
```

## Credits

- **Backend** — [Prahalad Reddy](https://github.com/Prahaladha-Reddy) ([original repo](https://github.com/Prahaladha-Reddy/YT_RAG))
- **Frontend** — [Yogesh Chebrolu](https://github.com/YogeshChebrolu)

> **Note:** Create your own `.env` files (in both `backend/` and `frontend/`) with your own credentials. No secrets are committed to this repo.
