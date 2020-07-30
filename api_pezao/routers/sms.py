"""
SMS router
"""
from typing import List

from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from .. import sms_utils
from ..deps import get_db

router = APIRouter()


@router.post("/sms_sweep")
def sms_sweep(
    background_tasks: BackgroundTasks,
    hospitals: List[str] = None,
    db: Session = Depends(get_db),
):
    """
    Envia todos os SMSs pendentes
    """
    background_tasks.add_task(sms_utils.sms_intermediary, hospitals, db)
    return {"message": "SMSs scheduled"}
