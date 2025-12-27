from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging

from ..ai_generator import generate_challenge_with_ai
from ..database.db import (
    get_challenge_quota,
    create_challenge,
    create_challenge_quota,
    reset_quota_if_needed,
    get_user_challenges,
)
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


class ChallengeRequest(BaseModel):
    difficulty: str

    class Config:
        json_schema_extra = {"example": {"difficulty": "easy"}}


@router.post("/generate-challenge")
async def generate_challenge(
    request: ChallengeRequest,
    request_obj: Request,
    db: Session = Depends(get_db),
):
    try:
        # Autenticación
        user_details = authenticate_and_get_user_details(request_obj)
        user_id = user_details.get("user_id")

        # Cuota
        quota = get_challenge_quota(db, user_id)
        if not quota:
            quota = create_challenge_quota(db, user_id)

        quota = reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota exhausted")

        # Generar reto con la IA
        challenge_data = generate_challenge_with_ai(request.difficulty)

        # Guardar reto en la base de datos (sin guardar el code)
        new_challenge = create_challenge(
            db=db,
            difficulty=request.difficulty,
            created_by=user_id,
            title=challenge_data["title"],
            options=json.dumps(challenge_data["options"]),
            correct_answer_id=challenge_data["correct_answer_id"],
            explanation=challenge_data["explanation"],
        )

        quota.quota_remaining -= 1
        db.commit()

        # Devolver también el campo "code" al frontend
        return {
            "id": new_challenge.id,
            "difficulty": request.difficulty,
            "title": new_challenge.title,
            "code": challenge_data.get("code", ""),
            "options": json.loads(new_challenge.options),
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp": new_challenge.date_created.isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error generating challenge with AI")
        raise HTTPException(status_code=500, detail="Error generating challenge with AI")


@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    # Solo retos creados por este usuario
    challenges = get_user_challenges(db, user_id)

    serialized = []
    for ch in challenges:
        serialized.append(
            {
                "id": ch.id,
                "difficulty": ch.difficulty,
                "title": ch.title,
                "options": json.loads(ch.options),
                "correct_answer_id": ch.correct_answer_id,
                "explanation": ch.explanation,
                "timestamp": ch.date_created.isoformat(),
            }
        )

    return {"challenges": serialized}



@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    quota = get_challenge_quota(db, user_id)
    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now(),
        }

    quota = reset_quota_if_needed(db, quota)
    return quota
