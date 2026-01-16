# AI Automation Hub 🚀

**Multi-tenant AI Automation Platform with RAG, Background Workers & n8n**

AI Automation Hub is a **production-grade backend + minimal admin frontend** for building **AI-powered automation workflows**.
It combines **RAG (Retrieval-Augmented Generation)**, **project-scoped knowledge bases**, and **workflow orchestration (n8n)** into a clean, scalable architecture.

This repository contains **both backend and frontend** in a single mono-repo for easier development and deployment.

---

## 🧠 What This Platform Does

- Multi-tenant AI automation (Organizations → Projects)
- Upload documents and build **project-specific knowledge bases**
- Ask AI questions grounded strictly in uploaded files (RAG)
- Trigger AI workflows via **webhooks, email, or n8n**
- Run heavy AI tasks asynchronously using **Redis workers**
- Provide a **minimal admin UI** for configuration (no Postman required)

---

## 🏗️ Repository Structure

```
ai-automation-hub/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/             # REST endpoints
│   │   ├── core/            # config, auth, redis, queue
│   │   ├── db/              # models, session
│   │   ├── rag/             # chunking, prompts
│   │   ├── services/        # RAG, storage, embeddings
│   │   └── workers/         # Redis background tasks
│   └── requirements.txt
│
├── ai-automation-hub-ui/     # Next.js minimal admin frontend
│   ├── app/
│   │   ├── login/
│   │   ├── orgs/
│   │   ├── projects/
│   │   └── layout.tsx
│   └── lib/
│       ├── api.ts
│       ├── auth.ts
│       └── supabase.ts
│
└── README.md                # You are here
```

---

## 🔑 Core Architecture

```
Frontend (Next.js)
   ↓
FastAPI Backend
   ↓
Supabase (Auth + Storage + Postgres + pgvector)
   ↓
Redis Queue → Background Workers
   ↓
OpenAI (Embeddings + LLM)
   ↓
n8n (Automation Execution)
```

**Key principle:**

- Backend = intelligence & security
- n8n = execution
- Frontend = configuration only

---

## ⚙️ Backend (Python / FastAPI)

### Features

- Supabase Auth (JWT + JWKS)
- Organizations & Projects (multi-tenancy)
- Data Sources (webhook, email, file)
- File uploads with Supabase Storage
- RAG pipeline:

  - Text extraction
  - Chunking
  - Embeddings (pgvector)
  - Semantic search
  - Grounded answers

- Redis + RQ background workers
- Webhook contracts for n8n

### Tech Stack

- FastAPI
- SQLAlchemy
- Supabase (Postgres + Storage)
- pgvector
- OpenAI
- Redis + RQ

### Run Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🖥️ Frontend (Next.js – Minimal Admin UI)

### Purpose

The frontend is intentionally **minimal** and acts as a **control panel**, not a full product UI.

### Features

- Supabase login
- Organization selection
- Project creation
- Data source creation (copy webhook IDs)
- File upload & processing status
- RAG testing UI (ask questions)
- No Postman required

### Tech Stack

- Next.js (App Router)
- TypeScript
- Supabase Auth
- Fetch-based API client

### Run Frontend

```bash
cd ai-automation-hub-ui
npm install
npm run dev
```

---

## 🔌 n8n Integration (One-Time Setup)

- A **single n8n instance** is reused for all projects
- Each project has unique `data_source_id`
- n8n workflows call:

  ```
  POST /webhooks/{data_source_id}
  ```

- Backend resolves org/project automatically

No per-project n8n setup required beyond pasting the webhook URL once.

---

## 📌 Typical Use Cases

- AI-powered email triage
- Knowledge-based customer support bots
- Lead qualification & routing
- Internal document Q&A
- Workflow-driven AI automation for clients

---

## 🚀 Status

✅ Backend complete
✅ Frontend complete (admin scope)
✅ RAG implemented
✅ Background workers enabled
⏳ n8n workflows (next step / client-specific)

---

## 🎯 Philosophy

This project is built to be:

- **Client-ready**
- **Freelancer-friendly**
- **Scalable without overengineering**
- **Easy to demo**
- **Easy to extend**

---

## 📄 License

MIT (or your preferred license)

---

Built as a **production-grade AI automation platform** with a focus on real-world usage, not demos.
