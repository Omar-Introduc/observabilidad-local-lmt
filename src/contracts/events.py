"""
Contratos de Observabilidad

modelos de Pydantic para Logs, Métricas y Trazas,
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, Literal, Dict
import json

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]



class LogEvent(BaseModel):
    id: UUID
    timestamp: datetime
    service: str = Field(..., min_length=1)
    level: LogLevel
    message: str = Field(..., min_length=1)
    details: Optional[Dict[str, str]] = None



class MetricEvent(BaseModel):
    id: UUID
    timestamp: datetime
    service: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, pattern=r"^[a-z0-9_.]+$")
    value: float
    tags: Dict[str, str]

    @field_validator('value')
    @classmethod
    def validate_value_is_not_negative(cls, v: float) -> float:
        """Valida que el valor de la métrica no sea negativo."""
        if v < 0:
            raise ValueError(
                f"El valor de la métrica ('{v}') no puede ser negativo."
            )
        return v

    @field_validator('name')
    @classmethod
    def validate_name_format(cls, v: str) -> str:
        """Valida que el nombre no empiece o termine con un punto."""
        if v.startswith('.') or v.endswith('.'):
            raise ValueError(
                "El nombre de la métrica no puede empezar o terminar con '.'"
            )
        return v



class TraceEvent(BaseModel):
    id: UUID
    timestamp: datetime
    service: str = Field(..., min_length=1)
    trace_id: UUID
    span_id: UUID
    parent_span_id: Optional[UUID] = None
    name: str = Field(..., min_length=1)
    duration: float
    tags: Dict[str, str]

    @field_validator('duration')
    @classmethod
    def validate_duration_is_positive(cls, v: float) -> float:
        """Valida que la duración de la traza sea un número positivo."""
        if v < 0:
            raise ValueError(
                f"La duración ('{v}') no puede ser un número negativo."
            )
        return v