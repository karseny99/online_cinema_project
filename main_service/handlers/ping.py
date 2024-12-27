from fastapi import APIRouter, HTTPException, Response
from typing import Literal
from models.monitoring_service_models import PingRequest, PingResponse
import service.ping_service 
    
router = APIRouter()

@router.get("/ping", response_model=PingResponse)
def ping(service_type: Literal["minio", "pg"],):
    '''
        Ручка для пинга бд или minio
    '''
    ping = service.ping_service.ping(PingRequest(service_type=service_type))
    return ping