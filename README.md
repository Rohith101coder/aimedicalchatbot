# Medical Chatbot

A Django web application for medical-information conversations. It includes
user registration, administrator approval of accounts, chat history, and
responses generated with a Hugging Face language model.

> **Prototype notice:** This project is not a clinically validated medical
> tool. Do not use it to diagnose, treat, or make urgent medical decisions.

## What is implemented

- User registration and login with waiting, active, and blocked account states.
- Demo administrator pages to list users and activate, block, unblock, or
  delete accounts.
- A browser-based chatbot with multiple saved conversations and persisted
  user/bot messages.
- Direct text generation through Hugging Face Transformers, PyTorch, and
  LangChain.
- A PDF extraction and text-chunking helper.

### Model and project-title clarification

The active chatbot uses **`microsoft/phi-2`** by default. The source code
inspected does not implement Gamma LLM V2 or a BERT model comparison.

`sentence-transformers/all-mpnet-base-v2` is configured as an optional
embedding model, but the active chat request does not initialize it or use
vector search. Likewise, the supplied medical PDF and PDF chunking helper
are not connected to chatbot responses. The current chat flow sends a user's
message directly to the language model; it is not retrieval-augmented
generation (RAG).

## Technology stack

- **Backend:** Python, Django 5.2.1, Django templates and sessions
- **Language model:** Hugging Face Transformers, Hugging Face Hub, PyTorch
- **LLM integration:** LangChain and `langchain-community`
- **Database:** SQLite with Django ORM
- **Frontend:** HTML, CSS, JavaScript, Django template language, Tailwind CSS
  (CDN on the chat page)
- **Document helper:** PyPDF2 and LangChain text splitting

The dependency file is named [`requirment.txt`](./requirment.txt). It also
lists packages not necessarily used by the active chat path. For example,
Django REST Framework is installed as a dependency, but the inspected routes
do not expose a DRF API.

## Local model details

| Purpose | Model | Status |
| --- | --- | --- |
| Chat text generation | `microsoft/phi-2` | Loaded by the active chatbot |
| Text embeddings | `sentence-transformers/all-mpnet-base-v2` | Configured helper; not used by active chat |
| Gamma LLM V2 / BERT comparison | Not identified in the active app code | Not implemented in the inspected flow |

The model is loaded in the Django server process. Hugging Face model files
may be downloaded and cached locally the first time the server starts; model
loading can take time and inference can require substantial memory. The
source selects float16 when CUDA is available and float32 otherwise.

Optional model configuration can be set in a local `.env` file:

```dotenv
MODEL_NAME=microsoft/phi-2
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

The embedding setting only affects the optional embedding initializer; it
does not add retrieval to the chat flow.

## Requirements

- Windows, macOS, or Linux
- Python environment compatible with the pinned packages in
  `requirment.txt`
- Enough disk space and memory for the model and its dependencies
- A compatible CUDA GPU is optional; CPU inference may be slower
- Internet access may be needed initially to download model files and
  templates' external frontend assets

Project notes disagree about the Python version: one specifies Python 3.11.3,
another says Python 3.10.2. Python 3.11.x is the more recent project note, but
confirm compatibility with your environment and the pinned PyTorch wheel
before installing.

## Run locally on Windows

Open PowerShell in the directory containing `manage.py` and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\requirment.txt
python manage.py migrate
python manage.py runserver
```

If PowerShell does not recognize `py -3.11`, install a compatible Python
release and use its `python` command to create the virtual environment.

Open <http://127.0.0.1:8000/> in your browser. Register a user, then activate
the account through the demo administrator pages before trying the chatbot.
The demo administrator credentials in the current view are `admin` / `admin`;
they are insecure and must never be used for a public deployment.

The LLM is initialized when the chatbot view module loads, so startup may
download model files or take longer than a normal Django application.

## Main project structure

```text
manage.py                    Django management entry point
medicalchatbot/              Project settings, URL routing, ASGI/WSGI
users/                       User, chat, message, and chatbot functionality
users/utility/llm_setup.py   Hugging Face model and embedding initialization
users/utility/pdf_processor.py
                             PDF text extraction and chunking helper
admins/                      Demo administrator account management
templates/                   Django HTML templates
media/                       Included medical reference PDF
db.sqlite3                   Local SQLite database (created/updated locally)
requirment.txt               Pinned Python dependencies
PROJECT_OVERVIEW.txt         Detailed inspected project and resume notes
```

## Configuration and security

The checked-in settings are for local development, not deployment. Before
deploying:

- Replace the insecure `SECRET_KEY`, set `DEBUG=False`, configure
  `ALLOWED_HOSTS`, and use environment variables for secrets.
- Replace the hard-coded demo administrator login with proper authentication
  and authorization.
- Remove password printing from login diagnostics.
- Review CSRF protection, session settings, HTTPS, database backups, and
  logging for the target deployment.
- Do not commit `.env` files, API keys, local model files, virtual
  environments, or a database containing real user data.
- `users/utility/test.py` contains a hard-coded external-service credential.
  Revoke/rotate it and replace it with an environment variable before
  sharing or deploying the project.

## Known limitations

- The chatbot is a direct text-generation interface, not a medically
  validated decision-support system.
- No Gamma LLM V2 integration or BERT comparison was found in the active
  application flow.
- The optional embedding model and PDF processing helper are not wired into
  chat retrieval.
- The project notes disagree on the supported Python version.
- `PyPDF2` is imported by the PDF helper but is not listed in
  `requirment.txt`; install it separately only if using that helper. The
  separate Pinecone test also has a dependency not listed in that file and
  is not required for normal chat usage.
- The `users` and `admins` test modules contain empty test scaffolding; the
  application features do not have meaningful automated test coverage in
  those files.

## Resume-ready summary

> Built a Django-based medical-information chatbot with account approval,
> persistent multi-conversation chat history, and local text generation using
> `microsoft/phi-2` via Hugging Face Transformers, PyTorch, and LangChain.

Suggested skills line: **Python, Django, SQLite, Hugging Face Transformers,
PyTorch, LangChain, HTML, CSS, JavaScript.**

Only claim Gamma LLM V2, BERT comparison, PDF-grounded answers, or RAG on a
resume if you implement and validate those features separately.
