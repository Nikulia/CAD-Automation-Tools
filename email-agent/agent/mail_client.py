import re
from email import message_from_bytes
from email.header import decode_header
from email.message import Message
import imaplib
from typing import List, Dict, Optional


class EmailClient:
    """Handles secure IMAP communication and non-destructive message parsing.

    Implements the Context Manager protocol (`with` statement) to guarantee
    proper socket cleanup and logout on completion or failure.
    """

    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def __enter__(self) -> "EmailClient":
        """Establishes an SSL-encrypted IMAP connection and selects the INBOX."""
        self.connection = imaplib.IMAP4_SSL(self.host)
        self.connection.login(self.username, self.password)
        self.connection.select("INBOX")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Safely closes the IMAP session upon exiting the context block."""
        if self.connection:
            self.connection.logout()

    @staticmethod
    def _decode_mime(raw_header: Optional[str]) -> str:
        """Decodes MIME-encoded email headers (e.g., UTF-8/Base64) into readable text."""
        if not raw_header:
            return ""
        fragments = decode_header(raw_header)
        decoded = []
        for fragment, encoding in fragments:
            if isinstance(fragment, bytes):
                decoded.append(fragment.decode(encoding or "utf-8", errors="replace"))
            else:
                decoded.append(fragment)
        return "".join(decoded)

    @staticmethod
    def _extract_content(msg: Message, max_length: int = 1000) -> tuple[str, List[str]]:
        """Extracts plain-text body snippet and a list of attached filenames."""
        body = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition", ""))
                filename = part.get_filename()

                if filename:
                    attachments.append(EmailClient._decode_mime(filename))
                elif content_type == "text/plain" and "attachment" not in disposition and not body:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        body = payload.decode(charset, errors="replace")
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                body = payload.decode(charset, errors="replace")

        cleaned = re.sub(r"\s+", " ", body).strip()
        return cleaned[:max_length], attachments

    def fetch_unread_emails(self, limit: int = 20) -> List[Dict[str, str]]:
        """Retrieves metadata and body snippets for unread messages without marking them read.

        Args:
            limit: Maximum number of recent unread emails to inspect.

        Returns:
            A list of dictionaries containing email ID, headers, and body snippet.
        """
        if not self.connection:
            raise RuntimeError("IMAP connection is not established.")

        _, messages = self.connection.search(None, "UNSEEN")
        # messages[0] contains a space-separated byte string of message sequence numbers
        mail_ids = messages[0].split()
        emails: List[Dict[str, str]] = []

        for mail_id in mail_ids[-limit:]:
            # BODY.PEEK[] fetches the message while preserving its \Unseen server flag
            _, data = self.connection.fetch(mail_id, "(BODY.PEEK[])")
            for part in data:
                if isinstance(part, tuple):
                    msg = message_from_bytes(part[1])
                    body_text, attachments = self._extract_content(msg)
                    emails.append({
                        "id": mail_id.decode(),
                        "from": self._decode_mime(msg["From"]),
                        "to": self._decode_mime(msg["To"]),
                        "subject": self._decode_mime(msg["Subject"]),
                        "body": body_text,
                        "attachments": attachments,
                    })
        return emails

    def mark_as_read(self, mail_id: str) -> None:
        """Sets the IMAP \\Seen flag on a specific message ID."""
        if not self.connection:
            raise RuntimeError("IMAP connection is not established.")
        self.connection.store(mail_id.encode(), "+FLAGS", "\\Seen")
