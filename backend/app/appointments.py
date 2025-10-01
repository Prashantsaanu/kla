from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from app.task import send_whatsapp_reminder
from app import celery_app


router = APIRouter(prefix="/appointments", tags=["appointments"])
rr = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/artist", response_model=list[schemas.AppointmentOut])
def get_my_appointments(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("artist"))
):
    return db.query(models.Appointment).join(models.TattooSession).filter(
        models.TattooSession.artist_id == current_user.id
    ).all()

@router.get("/client", response_model=list[schemas.AppointmentOut])
def get_client_appointments(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("client"))
):
    return db.query(models.Appointment).filter(
        models.Appointment.client_id == current_user.id
    ).all()

@router.post("/client/book", response_model=schemas.AppointmentOut)
def book_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("client"))
):
    tattoo = db.query(models.TattooSession).filter(models.TattooSession.id == appointment.tattoo_id).first()
    if not tattoo:
        raise HTTPException(status_code=404, detail="Tattoo not found")

    # Prevent double booking
    existing = db.query(models.Appointment).filter(
        models.Appointment.tattoo_id == appointment.tattoo_id,
        models.Appointment.date_time == appointment.date_time
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This time slot is already booked")

    new_appointment = models.Appointment(
        tattoo_id=appointment.tattoo_id,
        client_id=current_user.id,
        artist_id=tattoo.artist_id,
        date_time=appointment.date_time
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.get("/send-reminder")
def send_reminder(appointment_id: int):
    # Example: fetch client number from DB based on appointment_id
    client_number = "whatsapp:+91YOUR_NUMBER"
    message = f"Reminder for appointment #{appointment_id}"
    
    # Send asynchronously via Celery
    task = send_whatsapp_reminder.delay(client_number, message)
    
    return {"task_id": task.id, "status": "scheduled"}

@rr.get("/{task_id}")
def get_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,      # e.g., PENDING, STARTED, SUCCESS, FAILURE
        "result": task_result.result       # actual result (like message SID) if completed
    }