import html
from typing import Dict, Any
import requests


class TelegramNotifier:
    """Delivers HTML-formatted priority alerts via the Telegram Bot API."""

    def __init__(self, bot_token: str, chat_id: str):
        self.api_url = f"https://telegram.org{bot_token}/sendMessage"
        self.chat_id = chat_id

    def notify_important_email(self, email_verdict: Dict[str, Any]) -> None:
        """Formats and dispatches an email summary to the user's Telegram chat.

        Args:
            email_verdict: Classification dictionary marked with is_important=True.

        Raises:
            requests.HTTPError: If the Telegram API rejects the payload.
        """
        # Escape angle brackets (<, >) commonly found in email headers (e.g., Name <mail@domain.com>)
        # to prevent Telegram HTML parser errors.
        safe_from = html.escape(str(email_verdict["from"]))
        safe_subject = html.escape(str(email_verdict["subject"]))
        safe_reason = html.escape(str(email_verdict["reason"]))

        message = (
            f"🔥 <b>Important Work Email</b>\n\n"
            f"<b>From:</b> {safe_from}\n"
            f"<b>Subject:</b> {safe_subject}\n"
            f"<b>AI Reasoning:</b> {safe_reason}"
        )
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
        }
        response = requests.post(self.api_url, json=payload, timeout=10)
        response.raise_for_status()
