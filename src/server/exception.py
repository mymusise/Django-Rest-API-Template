from rest_framework.views import exception_handler
from rest_framework import exceptions, status
from rest_framework.views import Response
from .logger import exception_logger


def format_ValidationError(exc):
    details = exc.get_full_details()
    messages = []

    for key, error_messages in details.items():
        error_detail = []
        if isinstance(error_messages, dict):
            for v in error_messages.values():
                if isinstance(v, list):
                    error_detail += v
                else:
                    error_detail.append(v)
        else:
            error_detail = error_messages
        for message_item in error_detail:
            messages.append(f"{key}:{message_item.get('message')}")
    full_error_message = " ".join(messages)
    return full_error_message


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # custom exception processing
    if response is None:
        response = Response({"detail": str(exc)})
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc, exceptions.ValidationError):
            detail = format_ValidationError(exc)
            response.data = {"detail": detail, "code": "ValidationError"}
        else:
            response.data = {
                "detail": str(exc),
                "code": exc.detail.code,
            }
    else:
        exception_logger.exception(exc)
        response.status_code = int(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


class ObjectNotFoundException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "找不到对象."
    default_code = "object_not_found"


class ObjectPermissionDeniedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "没有权限访问这个对象."
    default_code = "no_permission_of_object"


class ServerCanProcessException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "收到请求但是服务器无法处理."
    default_code = "server_cant_process"


class ValueException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "输入有误."
    default_code = "value_error"


class UnauthorizedException(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "用户未登录或登录已失效"
    default_code = "Unauthorized"


class BizException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
