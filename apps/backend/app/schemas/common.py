"""Standard API response contracts."""

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """Safe error details exposed to API clients."""

    code: str
    message: str
    request_id: str | None = None


class ApiResponse[DataT](BaseModel):
    """Common success and failure envelope."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"success": True, "data": {}}}
    )

    success: bool
    data: DataT | None = None
    error: ErrorDetail | None = None
    message: str | None = None


class HealthData(BaseModel):
    """Health component statuses."""

    status: str = Field(examples=["ok"])
    application: str = "ok"
    database: str = "ok"
    service: str = "ok"


class SystemInfo(BaseModel):
    """Non-sensitive system information."""

    name: str
    version: str
    environment: str
    debug: bool
