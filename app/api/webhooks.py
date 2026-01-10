from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.webhook_service import handle_webhook_event

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/{data_source_id}")
async def receive_webhook(
    data_source_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.json()

    result = handle_webhook_event(
        db=db,
        data_source_id=data_source_id,
        payload=payload,
    )

    if not result:
        raise HTTPException(status_code=404, detail="Invalid data source")

    return {
        "status": "accepted",
        "event_id": result["event_id"],
        "project_id": result["project_id"],
    }
