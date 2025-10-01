from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, auth

router = APIRouter(prefix="/reviews", tags=["reviews"])

# --------------------
# Client leaves a review
# --------------------
@router.post("/", response_model=schemas.ReviewOut)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("client"))
):
    tattoo = db.query(models.TattooSession).filter(models.TattooSession.id == review.tattoo_id).first()
    if not tattoo:
        raise HTTPException(status_code=404, detail="Tattoo not found")

    new_review = models.Review(
        tattoo_id=review.tattoo_id,
        client_id=current_user.id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# --------------------
# Get all reviews for a tattoo (public)
# --------------------
@router.get("/tattoo/{tattoo_id}", response_model=list[schemas.ReviewOut])
def get_tattoo_reviews(tattoo_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Review).filter(models.Review.tattoo_id == tattoo_id).all()

# --------------------
# Get reviews by client
# --------------------
@router.get("/my", response_model=list[schemas.ReviewOut])
def get_my_reviews(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("client"))
):
    return db.query(models.Review).filter(models.Review.client_id == current_user.id).all()
