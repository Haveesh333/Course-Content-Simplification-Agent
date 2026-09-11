# CourseEase AI – Course Content Simplification Agent

A student-friendly AI web application that simplifies complex academic content using IBM Granite on watsonx.ai.

## Features
- Upload PDF or TXT course documents, or paste content directly
- Choose difficulty level: Beginner, Intermediate, or Advanced
- AI-generated simplified explanation
- Key points extracted from the content
- Difficult terms defined in simple language
- Relevant examples to reinforce understanding
- Auto-graded 5-question multiple-choice quiz

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript + Vite |
| Backend | Python 3.10+ + FastAPI |
| AI Model | IBM Granite (ibm/granite-3-3-8b-instruct) via watsonx.ai |
| HTTP Client | httpx (backend), axios (frontend) |
| PDF Parsing | PyMuPDF (fitz) |

## Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- An IBM Cloud account with a watsonx.ai project
- An IBM Cloud API key with watsonx.ai access

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd "CourseEase AI"
```

### 2. Backend setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```
Edit `backend/.env` and fill in your credentials:
- `WATSONX_API_KEY` — your IBM Cloud API key
- `WATSONX_PROJECT_ID` — your watsonx.ai project ID
- `WATSONX_MODEL_ID` — (optional) override the default model
- `WATSONX_URL` — (optional) override the region endpoint

### 4. Frontend setup
```bash
cd ../frontend
npm install
```

## Running the Application

### Start the backend
```bash
cd backend
python main.py
# Server starts at http://localhost:8000
```

### Start the frontend
```bash
cd frontend
npm run dev
# App opens at http://localhost:5173
```

## Usage
1. Open http://localhost:5173 in your browser
2. Upload a PDF/TXT file or paste course text
3. Select your difficulty level (Beginner / Intermediate / Advanced)
4. Click "Simplify"
5. Review the simplified explanation, key points, terms, and examples
6. Take the quiz and submit to see your score

## API Reference
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Health check |
| POST | /api/simplify | Simplify course content |

## Future Enhancements
- Lightweight RAG with FAISS for multi-document context
- Session history stored in browser localStorage
- Export results and quiz as PDF
- Multilingual output
- Text-to-speech for difficult terms
- Progress tracking across subjects
- Batch upload for multiple lecture files

## Project Structure

```
CourseEase AI/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── routers/
│   │   ├── __init__.py
│   │   └── simplify.py          # /api/simplify and /api/health endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_parser.py   # PDF / TXT extraction
│   │   ├── granite_service.py   # IBM Granite API calls + IAM token cache
│   │   └── prompt_builder.py    # Prompt construction per difficulty level
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic request/response models
│   ├── requirements.txt
│   ├── .env.example             # Environment variable template
│   └── .env                     # Your credentials (git-ignored)
│
├── frontend/
│   ├── index.html               # Vite entry HTML
│   ├── vite.config.ts           # Vite config with /api proxy
│   ├── tsconfig.json
│   ├── package.json
│   └── src/
│       ├── main.tsx             # React app entry point
│       ├── App.tsx              # Root component and layout
│       ├── components/
│       │   ├── UploadArea.tsx   # Drag-and-drop / file picker
│       │   ├── TextInput.tsx    # Paste-content textarea
│       │   ├── LevelSelector.tsx# Beginner / Intermediate / Advanced toggle
│       │   ├── SimplifyButton.tsx
│       │   ├── ResultsPanel.tsx # Simplified explanation + key points
│       │   ├── TermsPanel.tsx   # Difficult terms table
│       │   ├── ExamplesPanel.tsx
│       │   └── QuizPanel.tsx    # MCQ display + auto-grading
│       ├── hooks/
│       │   └── useSimplify.ts   # API call + loading/error state
│       ├── types/
│       │   └── index.ts         # Shared TypeScript interfaces
│       └── styles/
│           └── App.css          # Global styles
│
├── .gitignore
├── courseease-ai-plan.md
└── README.md
```
