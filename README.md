# todo-assistant

# TODO Application with AI & Telegram Integration

A modern task management (TODO) application featuring AI-powered command processing, a Telegram bot interface, and a microservices architecture.



## 🧱 System Interaction Scheme

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Web / TG Bot)
    participant Front as Frontend (Reflex / Bot)
    participant Back as Main Backend (FastAPI)
    participant DB as Database
    participant AI as AI Service
    participant LLM as LLM / Audio Model

    %% --- SCENARIO 1: CLEAN REQUESTS ---
    rect rgb(240, 248, 255)
        note right of User: Scenario 1: Standard (Clean) Request
        User->>Front: Action (e.g., Click "View Tasks", Check Checkbox)
        Front->>Back: API Call (GET /tasks, PATCH /tasks/id)
        Back->>DB: Query / Update Data
        DB-->>Back: Return Rows
        Back-->>Front: Render JSON Data
        Front-->>User: Update UI / Send Message
    end

    %% --- SCENARIO 2: SPECIAL AI REQUESTS ---
    rect rgb(255, 240, 245)
        note right of User: Scenario 2: Special AI Request (Text or Voice)
        User->>Front: Prompt Input (e.g., Send Voice Note / Command text)
        Front->>Back: POST /api/v1/ai/process (Text or Audio File)
        
        note over Back,AI: Backend acts as an Orchestrator
        Back->>AI: Forward Payload (POST /process-prompt)
        
        AI->>DB: Fetch Task Context / User History
        DB-->>AI: Return Context
        
        AI->>LLM: Send Payload for Processing
        LLM-->>AI: Return Processed Text / Result
        
        AI-->>Back: Return Validated Structured JSON
        
        Back->>DB: Save/Update Tasks based on AI response
        Back-->>Front: Return Final Response / Status
        Front-->>User: Show Structured Result (e.g., New Task Created)
    end
```

### Flow Breakdown

1. **Scenario 1 (Clean Requests):** When the user performs standard actions (e.g., viewing the task list, deleting a task, ticking a checkbox), the frontend clients (Reflex or Telegram Bot) communicate directly with the FastAPI backend. The AI Service remains idle, saving server resources and token costs.
2. **Scenario 2 (Special AI Requests):** When a user submits a voice note or a complex natural language command, the payload hits a specialized FastAPI endpoint. The backend acts as an orchestrator: it forwards the raw data to the AI Service, which pulls the necessary task context from the database, runs the data through the LLM/Audio model, and yields a validated structured JSON object. FastAPI then updates the primary database state and syncs the finalized results back to the user.




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
