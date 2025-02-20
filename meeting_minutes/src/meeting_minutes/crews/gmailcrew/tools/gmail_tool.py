from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .gmail_utility import authenticate_gmail, create_message, create_draft
from agentops import record_tool


class GmailToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    body: str = Field(..., description="The body of the email to send.")

@record_tool("GmailTool")
class GmailTool(BaseTool):
    name: str = "Gmail Tool"
    description: str = (
        "Send an email to the client with the meeting minutes using the provided body."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body: str) -> str:
        try:
            service = authenticate_gmail()
            sender = "nessarsolutions@gmail.com"
            to = "dhrubojyoti21@gmail.com"
            subject = "Meeting Minutes"
            message_text = body

            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)

            return "Email sent successfully"
        
        except Exception as e:
            return f"Error sending email: {e}"
