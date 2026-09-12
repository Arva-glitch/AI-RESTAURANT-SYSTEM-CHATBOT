from sqlalchemy.orm import Session

from app.models.offer import Offer
from app.schemas.offers import OfferCreate, OfferUpdate


def create_offer(db: Session, coupons: OfferCreate):

    db_offer = Offer(**Offer.model_dump())

    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)

    return db_offer


def get_offer(db: Session, offer_id: int):

    return (
        db.query(Offer)
        .filter(Offer.offer_id == offer_id)
        .first()
    )


def get_all_offers(db: Session):

    return db.query(Offer).all()


def update_offer(db: Session, offer_id: int, offer: OfferUpdate):

    db_offer = get_offer(db, offer_id)

    if not db_offer:
        return None

    update_data = offer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_offer, key, value)

    db.commit()
    db.refresh(db_offer)
    return db_offer


def delete_coupon(db: Session, offer_id: int):

    db_offer = get_offer(db, offer_id)

    if not db_offer:
        return None

    db.delete(db_offer)
    db.commit()

    return db_offer
