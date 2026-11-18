import json
from typing import List, Dict, Any
from google import genai
from google.genai import types
from agent.config import AgentConfig


class EmailTriageBrain:
    """LLM-powered reasoning engine using Google Gemini to classify email relevance."""

    def __init__(self, api_key: str, model_name: str = "gemini-3.1-flash-lite"):
        """Initializes the Gemini SDK client."""
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def evaluate_emails(self, emails: List[Dict[str, str]], config: AgentConfig) -> List[Dict[str, Any]]:
        """Analyzes a batch of emails against user role rules and returns structured verdicts.

        Args:
            emails: List of extracted email dictionaries from EmailClient.
            config: Active AgentConfig containing user role and colleague context.

        Returns:
            Parsed JSON list of classification decisions from the LLM.
        """
        colleagues_str = ", ".join(config.priority_colleagues) or "Not specified"

        # Construct domain-specific prompt with strict JSON schema enforcement
        prompt = f"""
                You are my personal executive AI assistant for filtering work emails.
                My role: Design Engineer / CAD Drafter (working with drawings, shop drawings / КМД, as-built documentation / ИД, method statements / ППР, technical specifications / ТЗ).
                My direct email: {config.yandex_email}
                My name and aliases: {config.user_name}
                Key colleagues: {colleagues_str}

                DECISION-MAKING ALGORITHM (evaluate strictly from top to bottom!):

                STEP 1. UNCONDITIONALLY IMPORTANT (is_important = true).
                If AT LEAST ONE of the following conditions is met, set true and DO NOT evaluate Step 2:
                - The 'to' field directly contains my personal email ({config.yandex_email}) AND at the same time:
                  a) the email has attached files (the 'attachments' list is not empty), OR
                  b) the email body is empty (""), OR
                  c) the body contains only a greeting (e.g., "Привет", "Добрый день"), informal chat, friendly banter, or complaints (colleagues often send work files this way or write directly on point).
                - The email is sent by one of my key colleagues ({colleagues_str}) directly to me ({config.yandex_email} is in 'to').
                - It is a scan or message from a scanner/printer (the sender or subject contains keywords like scan, scanner, printer, xerox, kyocera, hp, canon, мфу, скан).
                - The subject or body directly addresses me by name ({config.user_name}).
                - The email relates to drawings, shop drawings (КМД), as-built docs (ИД), method statements (ППР), bills of materials/specifications, structural technical details, or technical specs (ТЗ).

                STEP 2. NOISE / NOT MY RESPONSIBILITY (is_important = false).
                Apply ONLY IF none of the rules in Step 1 were triggered:
                - General group threads (even with management participating) where I am not listed in the direct 'to' recipients, not mentioned by name, and the topic is unrelated to engineering design (e.g., assembly, door delivery, installation/монтаж, logistics).
                - General department emails ("Коллеги") sharing sales leads or client contacts intended for sales managers.
                - Commercial quote requests (КП), cost estimates, tenders, marketing newsletters, and automated system notifications (excluding scanners/printers!).

                INPUT EMAILS:
                {json.dumps(emails, ensure_ascii=False, indent=2)}

                Return the response STRICTLY as a JSON array of objects with the following fields:
                - "id": string
                - "from": string
                - "subject": string
                - "is_important": boolean
                - "reason": string (a brief explanation in Russian specifying which exact rule triggered the decision)
                """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            # Enforce structured JSON output directly at the API level
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(response.text)
