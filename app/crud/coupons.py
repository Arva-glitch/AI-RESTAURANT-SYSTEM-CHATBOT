from sqlalchemy.orm import Session

from app.models.coupons import Coupon
from app.schemas.coupons import CouponCreate, CouponUpdate


def create_coupon(db: Session, coupons: CouponCreate):

    db_coupon = Coupon(**Coupon.model_dump())

    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)

    return db_coupon


def get_coupon(db: Session, coupon_id: int):

    return (
        db.query(Coupon)
        .filter(Coupon.coupon_id == coupon_id)
        .first()
    )


def get_all_coupons(db: Session):

    return db.query(Coupon).all()


def update_coupon(db: Session, coupon_id: int, coupon: CouponUpdate):

    db_coupon = get_coupon(db, coupon_id)

    if not db_coupon:
        return None

    update_data = coupon.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_coupon, key, value)

    db.commit()
    db.refresh(db_coupon)
    return db_coupon


def delete_coupon(db: Session, coupon_id: int):

    db_coupon = get_coupon(db, coupon_id)

    if not db_coupon:
        return None

    db.delete(db_coupon)
    db.commit()

    return db_coupon
