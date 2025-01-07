from pydantic import BaseModel, Field
from typing import List


class Appointment(BaseModel):
    description: str = Field(..., description="Descrição do prazo judicial ou evento.")
    start_date: str = Field(..., description="Data e hora de início do prazo judicial no formato ISO 8601 (YYYY-MM-DDTHH:MM).")
    end_date: str | None = Field(None, description="Data e hora de término do compromisso no formato ISO 8601 (YYYY-MM-DDTHH:MM).")


class AppointmentExtraction(BaseModel):
    appointments: List[Appointment] = Field(..., description="Lista de prazos judiciais extraídos do texto fornecido.")
    abstract: str = Field(..., description="Um resumo com os principais pontos sobre a publicacao.")
