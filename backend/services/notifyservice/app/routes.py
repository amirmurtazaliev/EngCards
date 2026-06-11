from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any

from app.service import send_message
from app.schemas import MessageData

router = APIRouter(
    prefix="/api",
    tags=["notif-service"]
)

@router.post("/sendmsg")
def send_msg(
    message_data: MessageData,
    background_tasks: BackgroundTasks
):
    
    if not message_data.recipient_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipient email is required"
        )
    
    if not message_data.message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required"
        )
    
    try:
        background_tasks.add_task(
            send_message,
            message_data.sender_name,
            message_data.recipient_email,
            message_data.message
        )

        ret_data = {
            "success": True,
            "message": "Message queued for sending",
            "recipient": message_data.recipient_email   
        }
        
        return JSONResponse(
            content=ret_data,
            status_code=200
        )
        
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service unavailable"
        )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )