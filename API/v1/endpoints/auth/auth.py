from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import structlog
import requests

logger = structlog.get_logger(__name__)

from settings import Settings
from v1.schemas.auth import TokenSchema, TelegramUserSchema, to_telegram_user

auth_router = APIRouter()


@auth_router.post(f'{Settings.API_URL_TAKE_TOKEN}', response_model=TokenSchema)
async def telegram_token_auth(from_user_data: dict):
    logger.info(
        'Handle POST request to API for Telegram token authentication with',
        data_from_user=from_user_data,
    )
    
    url = f'{Settings.SERVER_HOST.value}{Settings.API_BASE_PATH.value}{Settings.API_VERSION.value}{Settings.API_URL_TAKE_TOKEN.value}'
    telegram_user: TelegramUserSchema
    response: requests.Response
    try:
        telegram_user = to_telegram_user(from_user_data)
        
        logger.debug(
            'Successfully mapping user data to TelegramUserSchema and trying to send request to Django server REST API endpoint',
            telegram_user=telegram_user.dict(),
            endpoint=url
        )

        response = requests.post(
            url=url,
            data=telegram_user.dict(),
        )
    except ValidationError as validation_error:
        logger.error(
            'Validation error occurred',
            validation_error=validation_error.json(),
            endpoint=url,
            data_from_user=from_user_data,
        )
        
        return {
            'status_code' : 404,
            'detail': str(validation_error)
        }
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=url,
            data_from_user=from_user_data,
        )
        
        return {
            'status_code' : http_exception.status_code,
            'detail': str(http_exception)
        }
    except Exception as exception:
        logger.error(
            'Exception occurred in sync process', 
            exc_info=exception,
            endpoint=url,
            data_from_user=from_user_data,
        )
        
        return {
            'status_code' : 400,
            'detail': str(exception)
        }
    
    if response.status_code != 200:
        logger.error(
            'Failed to get token', 
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
        )
        
        return {
            'status_code' : response.status_code,
            'detail': result.get('error', 'Server error')
        }
        
    if 'token' and 'telegram_id' not in response.json():
        logger.error(
            'No token or telegram_id in response',
            response=response.json(),
        )
        
        return {
            status_code: 400,
            'detail': 'Invalid response from server'
        }
        
    return response.json()
