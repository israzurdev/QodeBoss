# backend/src/database/db.py

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from .models import Base, engine, Challenge, ChallengeQuota

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

MAX_QUOTA = 5
REFILL_EVERY_HOURS = 2


# --- QUOTA HELPERS --- #

def get_challenge_quota(db: Session, user_id: str):
  """Obtener la cuota de un usuario (o None si no existe)."""
  return (
      db.query(ChallengeQuota)
      .filter(ChallengeQuota.user_id == user_id)
      .first()
  )


def create_challenge_quota(db: Session, user_id: str):
  """Crear cuota inicial para un usuario (empieza con 5 retos)."""
  quota = ChallengeQuota(
      user_id=user_id,
      quota_remaining=MAX_QUOTA,
      last_reset_date=datetime.utcnow(),
  )
  db.add(quota)
  db.commit()
  db.refresh(quota)
  return quota


def reset_quota_if_needed(db: Session, quota: ChallengeQuota):
  """
  Regenera 1 reto cada 2 horas hasta un máximo de 5.
  Se ejecuta cada vez que se consulta la cuota o se genera un reto.
  """
  now = datetime.utcnow()

  if quota.last_reset_date is None:
      quota.last_reset_date = now
      db.commit()
      db.refresh(quota)
      return quota

  elapsed = now - quota.last_reset_date
  steps = elapsed // timedelta(hours=REFILL_EVERY_HOURS)

  if steps >= 1 and quota.quota_remaining < MAX_QUOTA:
      new_tokens = int(steps)
      if new_tokens > 0:
          quota.quota_remaining = min(
              MAX_QUOTA, quota.quota_remaining + new_tokens
          )
          quota.last_reset_date = quota.last_reset_date + steps * timedelta(
              hours=REFILL_EVERY_HOURS
          )
          db.commit()
          db.refresh(quota)

  return quota


# --- CHALLENGES HELPERS --- #

def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str,
):
  challenge = Challenge(
      difficulty=difficulty,
      created_by=created_by,
      title=title,
      options=options,
      correct_answer_id=correct_answer_id,
      explanation=explanation,
      date_created=datetime.utcnow(),
  )
  db.add(challenge)
  db.commit()
  db.refresh(challenge)
  return challenge


# backend/src/database/db.py

from sqlalchemy.orm import Session
from .models import Challenge

def get_user_challenges(db: Session, user_id: str):
    """Historial de retos del usuario autenticado."""
    return (
        db.query(Challenge)
        .filter(Challenge.created_by == user_id)  # <- SOLO los tuyos
        .order_by(Challenge.date_created.desc())
        .all()
    )

