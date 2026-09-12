from sqlalchemy.orm import Session

from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate


def create_staff(db: Session, staff: StaffCreate):

    db_staff = Staff(**staff.model_dump())

    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)

    return db_staff


def get_staff(db: Session, staff_id: int):

    return (
        db.query(Staff)
        .filter(Staff.staff_id == staff_id)
        .first()
    )


def get_all_staff(db: Session):

    return db.query(Staff).all()


def update_staff(db: Session, staff_id: int, staff: StaffUpdate):

    db_staff = get_staff(db, staff_id)

    if not db_staff:
        return None

    update_data = staff.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_staff, key, value)

    db.commit()
    db.refresh(db_staff)

    return db_staff


def delete_staff(db: Session, staff_id: int):

    db_staff = get_staff(db, staff_id)

    if not db_staff:
        return None

    db.delete(db_staff)
    db.commit()

    return db_staff
