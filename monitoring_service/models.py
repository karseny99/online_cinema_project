from pydantic import BaseModel, ValidationError, Field
from typing import Literal, Optional

class PingRequest(BaseModel):
    service_type: Literal["minio", "pg"]


class PingResponse(BaseModel):
    service_type: Optional[Literal["minio", "pg"]] = None
    pong: Optional[Literal["pong"]] = None
    success: bool