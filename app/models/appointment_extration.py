from pydantic import BaseModel, Field
from typing import List


class Appointment(BaseModel):
    description: str = Field(..., description="Descrição do compromisso ou evento.")
    start_date: str = Field(..., description="Data e hora de início do compromisso no formato ISO 8601 (YYYY-MM-DDTHH:MM).")
    end_date: str | None = Field(None, description="Data e hora de término do compromisso no formato ISO 8601 (YYYY-MM-DDTHH:MM).")


class AppointmentExtraction(BaseModel):
    appointments: List[Appointment] = Field(..., description="Lista de compromissos extraídos do texto fornecido.")
