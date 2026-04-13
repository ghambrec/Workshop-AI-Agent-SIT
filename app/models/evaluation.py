from typing import List, Optional
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    # Field allows us to be explicit about the expected data
    expected_tool_calls: List[str] = Field(default_factory=list)


class EvalItem(BaseModel):
    question: str
    expected_output: str
    # Nested model for the metadata dictionary
    metadata: Optional[Metadata] = None


# To handle the top-level list
class EvalSuite(BaseModel):
    items: List[EvalItem]
