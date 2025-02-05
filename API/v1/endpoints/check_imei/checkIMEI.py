import requests
import structlog
from fastapi import APIRouter, Request, HTTPException, status

from v1.functiontools import handle_401_response

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import IMEICheckScheme, to_imei_check
from settings import server_host, api_base_path, api_version, imei_check_api_token

check_imei_router = APIRouter()

DEFAULT_SERVICE_ID = 1


class Methods:
    POST = 'POST'
    GET = 'GET'


@check_imei_router.get('/', response_model=IMEICheckScheme)
async def check_imei(request: Request):
    logger.info(
        'Handle GET request to API for check device IMEI',
        request_headers=request.headers,
        request_body=await request.json(),
    )
    
    request_headers = request.headers
    request_body = await request.json()
    
    handle_401_response(request_headers)
    
    url = f'{server_host}{api_base_path}{api_version}/check-imei/'
    imei_check_url = 'https://api.imeicheck.net/v1/checks'
    imei: str = request_body.get('imei')
    server_response: requests.Response
    imei_check_response: requests.Response
    imei_check_headers: dict = {
        'Authorization': f'Bearer {imei_check_api_token}'
    }
    imei_check_body: dict = {
        'deviceId': imei,
        'serviceId': DEFAULT_SERVICE_ID,
    }
    
    api_headers: dict = {
        'Authorization': request_headers.get('authorization'),
    }
    api_body: dict = {
        'imei': imei,
    }
            
    server_response = requests.get(
        url=url,
        headers=api_headers,
        json=api_body,
    )

    return to_imei_check(imei_check_response.json())


def request_imei_check(request: Request):
    pass


def handle_server_GET_request(url: str, headers: dict, body: dict) -> requests.Response:
    debug_log_text = 'Get data from bot`s request and trying to Send GET request to server`s REST to get info about device from database'
    handle_request(url, headers, body, Methods.GET, debug_log_text)


def handle_server_POST_request(url: str, headers: dict, body: dict) -> requests.Response:
    debug_log_text = 'Sending data to server by POST request to save entry about device'
    handle_request(url, headers, body, Methods.POST, debug_log_text)


def handle_imei_check_request(url: str, headers: dict, body: dict) -> requests.Response:
    dedug_log_text = 'Get data from bot`s request and trying to Send POST request to get info about device'
    handle_request(url, headers, body, Methods.POST, dedug_log_text)


def handle_request(
    url: str, 
    headers: dict, 
    body: dict,
    method: Methods,
    debug_log_txt: str
) -> requests.Response:
    response: requests.Response
    try:
        logger.debug(
            debug_log_txt,
            endpoint=url,
            headers=headers,
            body=body,
        )
        
        if method == Methods.GET:
            response = requests.get(
                url=imei_check_url,
                headers=headers,
                json=body,
            )
            
        elif method == Methods.POST:
            response = requests.post(
                url=imei_check_url,
                headers=headers,
                json=body,
            )
            
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=imei_check_url,
            headers=headers,
            body=body,
        )

        raise HTTPException(
            status_code=http_exception.status_code,
            detail=http_exception.detail,
        )

    except Exception as exception:
        logger.error(
            'Exception occurred',
            exc_info=exception,
            endpoint=url,
            headers=headers,
            body=body,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )
        
    if response.status_code != status.HTTP_200_OK:
        logger.error(
            'Failed to get data about device by IMEI',
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
            imei=imei,
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
        
    return response
