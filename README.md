# todo-assistant

# TODO Application with AI & Telegram Integration

A modern task management (TODO) application featuring AI-powered command processing, a Telegram bot interface, and a microservices architecture.

## 🧱 Architecture Diagram

```mermaid
graph TD
    %% Frontend Components
    Reflex[Web Frontend: Reflex] 
    TGBot[Mobile Frontend: Telegram Bot]

    %% Core Backend
    FastAPI[Main Backend: FastAPI]
    DB[(Database: PostgreSQL/SQLite)]

    %% Dedicated AI Service
    AIService[AI Service]
    LLM[[LLM / Audio Model]]

    %% Interactions
    Reflex -->|1. User Request| FastAPI
    TGBot -->|1. User Request| FastAPI
    
    FastAPI -->|2. Forward Request| AIService
    
    AIService -->|3. Fetch Task Context| DB
    AIService <-->|4. Process Prompt / Voice| LLM
    AIService -->|5. Return Structured JSON| FastAPI
    
    FastAPI -->|6. Save Data| DB
    FastAPI -->|7. Update UI| Reflex
    FastAPI -->|7. Update Chat| TGBot

    style Reflex fill:#f9f,stroke:#333,stroke-width:2px
    style TGBot fill:#bbf,stroke:#333,stroke-width:2px
    style FastAPI fill:#dfd,stroke:#333,stroke-width:2px
    style AIService fill:#fdd,stroke:#333,stroke-width:2px
    style DB fill:#fff,stroke:#333,stroke-width:2px
```

---

## 🛠 Component Breakdown

### 1. Main Backend (`Backend`)
*   **Technology Stack:** FastAPI, SQLAlchemy / Tortoise ORM, PostgreSQL / SQLite.
*   **Role:** Acts as the central hub of the application. It handles core business logic, user authentication, direct database management, and exposes the primary REST API for all frontend clients.

### 2. Web Frontend (`Frontend`)
*   **Technology Stack:** Reflex (Python-only web framework).
*   **Role:** The main web user interface. It communicates directly with the FastAPI backend to render the dashboard, task lists, and settings seamlessly.

### 3. Telegram Bot (`TG Bot`)
*   **Technology Stack:** aiogram / telebot.
*   **Role:** An alternative, mobile-friendly frontend client. It allows users to manage their TODO tasks on the go through interactive buttons, text messages, and voice notes.

### 4. AI Service (`AI Service`)
*   **Technology Stack:** Python, LLM APIs (or local models).
*   **Role:** A dedicated microservice isolated from the main business logic. It handles heavy or complex intelligent tasks:
    *   **Direct Database Access:** Queries the database independently to gather relevant task context or user logs needed for the prompt.
    *   **Prompt Processing:** Interprets natural language inputs (text) or audio messages (voice).
    *   **Structured Output:** Guarantees strict validation and formats the final AI response into a clean JSON object before returning it to the main backend.

---

## 🧠 AI Capabilities & System Workflow

1. **Flexible Input:** The user submits a command via text or voice (e.g., *"Remind me to call John tomorrow at 5 PM"*) through either the web interface or the Telegram bot.
2. **Context Enrichment:** The request is routed to the AI Service, which pulls any necessary background data directly from the DB.
3. **Structured Response:** The AI model parses the input and returns a validated JSON structure containing clean fields like `task_title`, `due_date`, and `priority`.
4. **State Synchronization:** FastAPI processes this structured response, saves the new task to the database, and updates both frontends.
