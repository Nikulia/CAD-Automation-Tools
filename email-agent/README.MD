```markdown
# 🤖 Autonomous Email Triage AI Agent

An autonomous Python-based AI agent powered by **Google Gemini** that connects to an IMAP mailbox, evaluates incoming emails using semantic context and role-based rules, clears irrelevant noise, and forwards critical alerts to **Telegram**.

Built to eliminate inbox clutter for engineering and CAD drafting workflows without relying on rigid keyword filters.

## ✨ Key Features
- **Context-Aware Reasoning:** Evaluates sender-recipient relationships (`From` / `To`), user aliases, and domain-specific responsibilities rather than brittle regex rules.
- **Safe Non-Destructive Inspection:** Uses IMAP `BODY.PEEK[]` to analyze unread emails without prematurely altering their server-side status.
- **Autonomous Actions (Tool Execution):** Automatically flags non-relevant emails as `\Seen` on the mail server and dispatches HTML-escaped summaries via Telegram Bot API for high-priority tasks.
- **Zero-Cost Serverless Scheduling:** Configured to run strictly during working hours (Mon–Fri) via **GitHub Actions** cron workflows.
- **Clean Architecture:** Built with modular OOP principles, context managers, and environment-based secret management.

## 🏗️ Architecture
```text
[IMAP Mail Server] ──(BODY.PEEK)──▶ [EmailClient]
                                         │
                                         ▼
[Telegram Bot API] ◀──(Alert)──── [EmailTriageAgent] ◀──▶ [Gemini LLM Brain]
                                         │
                                         ▼
[IMAP Mail Server] ◀──(+FLAGS \Seen)─────┘
```

## 🚀 Setup & Deployment

### 1. Prerequisites
- Python 3.11+
- Google AI Studio API Key
- IMAP-enabled email account (with App Password)
- Telegram Bot Token & Chat ID

### 2. Local Installation
```bash
git clone https://github.com
cd YOUR_REPO_NAME
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Set the following environment variables locally or add them to your GitHub Repository Secrets (**Settings → Secrets and variables → Actions**):

| Variable | Description | Example |
| :--- | :--- | :--- |
| `YANDEX_EMAIL` | Target email address | `user@yandex.ru` |
| `YANDEX_APP_PASSWORD` | IMAP application password | `xxxx-xxxx-xxxx-xxxx` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSy...` |
| `TELEGRAM_BOT_TOKEN` | Token from `@BotFather` | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Your personal Telegram numeric ID | `987654321` |
| `USER_NAME` | Your name and aliases for context | `Andrey, Andryukha` |
| `PRIORITY_COLLEAGUES` | Comma-separated emails of key colleagues | `boss@company.ru, lead@company.ru` |
| `TIMEZONE` | Local timezone for schedule guard | `Asia/Tbilisi` |

### 4. Cloud Automation (GitHub Actions)
The included `.github/workflows/agent_schedule.yml` runs the agent every 30 minutes during working hours on weekdays. You can also trigger it manually via the **Actions** tab using `workflow_dispatch`.