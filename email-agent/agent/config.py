import os
import datetime
from dataclasses import dataclass, field
from typing import List
import pytz


@dataclass
class AgentConfig:
    """Configuration container loaded securely from environment variables.

    Attributes:
        yandex_email: Target Yandex email address.
        yandex_password: IMAP application-specific password.
        gemini_api_key: API key for Google Gemini LLM.
        telegram_token: Bot token obtained from @BotFather.
        telegram_chat_id: Numeric Telegram user ID for receiving alerts.
        user_name: User's primary name and informal aliases for context matching.
        timezone: IANA timezone string for schedule enforcement.
        work_start_hour: Start of the working day (24-hour format, inclusive).
        work_end_hour: End of the working day (24-hour format, exclusive).
        priority_colleagues: List of email addresses belonging to management or key teammates.
    """
    yandex_email: str
    yandex_password: str
    gemini_api_key: str
    telegram_token: str
    telegram_chat_id: str
    user_name: str = "Andrey"
    timezone: str = "Asia/Tbilisi"
    work_start_hour: int = 9
    work_end_hour: int = 19
    priority_colleagues: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Factory method to instantiate configuration from OS environment variables.

        Raises:
            KeyError: If any mandatory environment secret is missing.
        """
        # Parse comma-separated colleague emails into a clean list
        colleagues_raw = os.environ.get("PRIORITY_COLLEAGUES", "")
        colleagues = [c.strip() for c in colleagues_raw.split(",") if c.strip()]

        return cls(
            yandex_email=os.environ["YANDEX_EMAIL"],
            yandex_password=os.environ["YANDEX_APP_PASSWORD"],
            gemini_api_key=os.environ["GEMINI_API_KEY"],
            telegram_token=os.environ["TELEGRAM_BOT_TOKEN"],
            telegram_chat_id=os.environ["TELEGRAM_CHAT_ID"],
            user_name=os.environ.get("USER_NAME", "Andrey"),
            timezone=os.environ.get("TIMEZONE", "Asia/Tbilisi"),
            priority_colleagues=colleagues,
        )


class WorkScheduleGuard:
    """Ensures the agent executes strictly during defined working hours."""

    def __init__(self, timezone_str: str, start_hour: int, end_hour: int):
        """Initializes the schedule guard with timezone and hour boundaries."""
        self.tz = pytz.timezone(timezone_str)
        self.start_hour = start_hour
        self.end_hour = end_hour

    def is_working_time(self) -> bool:
        """Checks whether the current local time falls within Monday–Friday working hours.

        Returns:
            True if it is a weekday and within working hours, False otherwise.
        """
        now = datetime.datetime.now(self.tz)
        is_weekday = now.weekday() < 5  # Monday is 0, Sunday is 6
        is_work_hour = self.start_hour <= now.hour < self.end_hour
        return is_weekday and is_work_hour
