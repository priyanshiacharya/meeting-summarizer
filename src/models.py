from pydantic import BaseModel, Field
from typing import List, Optional

class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    due_date: Optional[str] = None

class MeetingSummary(BaseModel):
    title: Optional[str] = None
    key_decisions: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    summary: str
