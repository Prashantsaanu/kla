from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, auth

router = APIRouter(prefix="/tattoos", tags=["tattoos"])

# --------------------
# Create a tattoo (artist only)
# --------------------
@router.post("/", response_model=schemas.TattooOut)
def create_tattoo(
    tattoo: schemas.TattooCreate,
    current_user: models.User = Depends(auth.require_role("artist")),
    db: Session = Depends(database.get_db)
):
    new_tattoo = models.TattooSession(
        title=tattoo.title,
        description=tattoo.description,
        price=tattoo.price,
        artist_id=current_user.id
    )
    db.add(new_tattoo)
    db.commit()
    db.refresh(new_tattoo)
    return new_tattoo

# --------------------
# Get all tattoos (public)
# --------------------
@router.get("/", response_model=list[schemas.TattooOut])
def get_all_tattoos(db: Session = Depends(database.get_db)):
    return db.query(models.TattooSession).all()

# --------------------
# Get artist's own tattoos
# --------------------
@router.get("/my", response_model=list[schemas.TattooOut])
def list_my_tattoos(
    current_user: models.User = Depends(auth.require_role("artist")),
    db: Session = Depends(database.get_db)
):
    return db.query(models.TattooSession).filter(models.TattooSession.artist_id == current_user.id).all()

# --------------------
# Get tattoo by ID (public)
# --------------------
@router.get("/{tattoo_id}", response_model=schemas.TattooOut)
def get_tattoo(tattoo_id: int, db: Session = Depends(database.get_db)):
    tattoo = db.query(models.TattooSession).filter(models.TattooSession.id == tattoo_id).first()
    if not tattoo:
        raise HTTPException(status_code=404, detail="Tattoo not found")
    return tattoo

# --------------------
# Update tattoo (artist only)
# --------------------
@router.put("/{tattoo_id}", response_model=schemas.TattooOut)
def update_tattoo(
    tattoo_id: int,
    tattoo_data: schemas.TattooCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("artist"))
):
    tattoo = db.query(models.TattooSession).filter(
        models.TattooSession.id == tattoo_id,
        models.TattooSession.artist_id == current_user.id
    ).first()
    if not tattoo:
        raise HTTPException(status_code=404, detail="Tattoo not found or unauthorized")

    tattoo.title = tattoo_data.title
    tattoo.description = tattoo_data.description
    tattoo.price = tattoo_data.price
    db.commit()
    db.refresh(tattoo)
    return tattoo

# --------------------
# Delete tattoo (artist only)
# --------------------
@router.delete("/{tattoo_id}")
def delete_tattoo(
    tattoo_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("artist"))
):
    tattoo = db.query(models.TattooSession).filter(
        models.TattooSession.id == tattoo_id,
        models.TattooSession.artist_id == current_user.id
    ).first()
    if not tattoo:
        raise HTTPException(status_code=404, detail="Tattoo not found or unauthorized")

    db.delete(tattoo)
    db.commit()
    return {"detail": "Tattoo deleted successfully"}
