from agent.config import AgentConfig
from agent.mail_client import EmailClient
from agent.brain import EmailTriageBrain
from agent.notifier import TelegramNotifier


class EmailTriageAgent:
    """Coordinates the end-to-end email fetching, classification, and action pipeline."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.brain = EmailTriageBrain(api_key=config.gemini_api_key)
        self.notifier = TelegramNotifier(
            bot_token=config.telegram_token,
            chat_id=config.telegram_chat_id,
        )

    def run(self) -> None:
        """Executes a single triage cycle across unread inbox messages."""
        with EmailClient("imap.yandex.ru", self.config.yandex_email, self.config.yandex_password) as mail:
            unread_emails = mail.fetch_unread_emails(limit=20)
            if not unread_emails:
                print("No unread emails found. Inbox is clean.")
                return

            print(f"Analyzing {len(unread_emails)} unread email(s)...")
            verdicts = self.brain.evaluate_emails(unread_emails, self.config)

            # Execute tool actions based on LLM classification
            for item in verdicts:
                if item.get("is_important"):
                    self.notifier.notify_important_email(item)
                    print(f"[ALERT SENT] {item['subject']}")
                else:
                    mail.mark_as_read(item["id"])
                    print(f"[MARKED READ] {item['subject']}")
