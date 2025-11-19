from configs.config_limiter import limiter
from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
import logging

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)


@router.get(
    path="/github-status",
    name="github-status",
    include_in_schema=True,
)
# Improved rate limiting - more restrictive
@limiter.limit("10/minute")
def get_github_status(
    request: Request,
) -> JSONResponse:
    """
    Endpoint to get the GitHub status. The GitHub status page is `https://www.githubstatus.com/api/v2/status.json`.
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "FastAPI-App/1.0",  # Identify our application
    }
    
    # Set request timeout for better resource management
    timeout = 30  # 30 seconds timeout
    
    try:
        response = requests.get(
            url="https://www.githubstatus.com/api/v2/status.json",
            headers=headers,
            verify=True,  # Enable SSL verification for security
            timeout=timeout,
        )
        
        if response.ok:
            return JSONResponse(
                content=jsonable_encoder(response.json()),
                media_type="application/json",
                status_code=response.status_code,
            )
        else:
            # Log error for debugging without exposing sensitive data
            logger.error(f"GitHub API request failed: {response.status_code}")
            
            return JSONResponse(
                content=jsonable_encoder(
                    {
                        "message": "Failed to get GitHub status",
                        "status_code": response.status_code,
                        # Don't expose raw error details in response
                    }
                ),
                media_type="application/json",
                status_code=response.status_code,
            )
    
    except requests.exceptions.Timeout as error:
        logger.error(f"Request timed out: {str(error)}")
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "message": "Request timed out",
                    "type": "timeout_error",
                }
            ),
            media_type="application/json",
            status_code=status.HTTP_GATEWAY_TIMEOUT,
        )
    
    except requests.exceptions.ConnectionError as error:
        logger.error(f"Connection error: {str(error)}")
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "message": "Connection error",
                    "type": "connection_error",
                }
            ),
            media_type="application/json",
            status_code=status.HTTP_BAD_GATEWAY,
        )
    
    except requests.exceptions.RequestException as error:
        # Generic request exception handling
        logger.error(f"Request exception: {str(error)}")
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "message": "Failed to get GitHub status",
                    "type": "request_error",
                }
            ),
            media_type="application/json",
            status_code=status.HTTP_INTERNAL_SERVER_ERROR,
        )
