import json

from models.models import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse

from rpc_client.rpc_client import get_auth_rpc_client


def register_user(req: RegisterRequest) -> RegisterResponse:
    register_user_function_name = "register_user"
    rpc_client = get_auth_rpc_client()

    result = str(rpc_client.send_task(register_user_function_name, req))
    result = json.loads(result)
    result = RegisterResponse(**result)

    return result


def login_user(req: LoginRequest) -> LoginResponse:
    login_user_function_name = "login_user"
    rpc_client = get_auth_rpc_client()

    result = str(rpc_client.send_task(login_user_function_name, req))
    result = json.loads(result)
    result = LoginResponse(**result)

    return result
