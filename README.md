# YouTube RAG Chat Assistant

## Demo

<video src="https://github.com/user-attachments/assets/33031f60-6fcc-4190-afef-d349cc5d4f39" controls width="100%"></video>

- A Chrome side-panel assistant that lets users chat with any YouTube video using transcript, visual frame, screenshot, watchtime, and notes context.

- Built with React, FastAPI, Supabase/pgvector, CLIP embeddings, and Gemini tool-calling so answers are grounded in retrieved video evidence instead of a raw URL.

## Frontend: What It Does

The frontend is a Chrome extension side panel built with React, TypeScript, and Vite. It opens beside YouTube, detects the current video, shows the chat UI, tracks watchtime, captures screenshots, and lets users create or attach notes.

```text
YouTube video
    |
    v
Chrome side panel
    |
    |-- chat with video
    |-- capture screenshot
    |-- show watchtime
    |-- create notes
    `-- attach saved notes
```

## Frontend: How It Works

The extension keeps browser-specific work outside React. `content.js` reads the YouTube page, `background.js` handles Chrome APIs, and React renders the side panel state.

```text
content.js
    |-- gets video_id, title, channel
    |-- listens to current watchtime
    `-- sends updates to background.js

background.js
    |-- stores current video
    |-- opens side panel
    `-- captures screenshots

React app
    |-- AuthContext: Supabase session
    |-- VideoContext: video, screenshot, watchtime, chat state
    `-- ChatPage: user questions and AI answers
```

## Backend: What It Does

The backend is a FastAPI service that processes YouTube videos and answers questions using multimodal RAG. It extracts transcripts, samples frames, stores embeddings, retrieves relevant context, and asks Gemini to generate grounded answers.

```text
User question
    |
    v
FastAPI backend
    |
    |-- verify user
    |-- load chat history
    |-- retrieve transcript chunks
    |-- retrieve video frames
    `-- generate answer with Gemini
```

## Backend: How It Works

When a video is processed, the backend creates searchable text and image evidence. When the user asks a question, it searches that evidence with pgvector and sends the best context to Gemini.

```text
YouTube URL
    |
    v
Extract transcript + sample frames
    |
    v
Chunk transcript + create CLIP embeddings
    |
    v
Store in Supabase Postgres + Storage + pgvector
    |
    v
Retrieve matching transcript/frame context
    |
    v
Gemini returns grounded answer
```

Main backend pieces:

```text
/core/v1/video   -> video status and processing
/core/v1/chat    -> chat, history, screenshot, watchtime
/core/v1/notes   -> create, search, and update notes

Supabase Auth     -> user login and JWT verification
Supabase Storage  -> sampled frames and screenshots
Postgres/pgvector -> transcript, frame, note embeddings
Gemini            -> final answer generation
```

## Running

```bash
# backend
cd yt-rag-frontend/backend
pip install -e .
uvicorn core.main:app --reload --app-dir src --port 8000

# frontend
cd yt-rag-frontend/frontend
npm install
npm run dev
npm run build
```
