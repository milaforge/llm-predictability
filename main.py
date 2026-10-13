from typing import Literal

from fastapi import FastAPI, HTTPException
from ollama import AsyncClient
from pydantic import BaseModel, ConfigDict, Field, ValidationError

app = FastAPI()
llm = AsyncClient()


# Reject malformed input
class Ticket(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class Classification(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    # Restrict possible categories
    category: Literal["bug", "feature", "question", "other"]


@app.post("/classify")
async def classify(ticket: Ticket) -> Classification:
    response = await llm.chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": "Classify the support ticket."},
            {"role": "user", "content": ticket.text},
        ],
        # Constraint model generation
        format=Classification.model_json_schema(),
        # Reduce randomness, not a determinism guarantee
        options={"temperature": 0},
    )

    try:
        # Independently validate LLM output
        return Classification.model_validate_json(response.message.content)
    except ValidationError:
        # Signal invalid model output
        raise HTTPException(502, "Invalid LLM output")
