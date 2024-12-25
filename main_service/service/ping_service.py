from models.monitoring_service_models import PingRequest, PingResponse
from rpc_client.rpc_client import get_ping_rpc_client

def ping(request: PingRequest) -> PingResponse:
    '''
        Ping database or storage depends on request
        Choose minio or pg in PingRequest field
    '''

    search_function_name = "ping"
    result = get_ping_rpc_client().send_task(search_function_name, request)

    if not result:
        return PingResponse(
            service_type=None,
            pong=None,
            success=False,
        )
    
    result = PingResponse(**result)
    return result