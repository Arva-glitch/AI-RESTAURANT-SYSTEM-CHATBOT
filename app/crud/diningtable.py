from sqlalchemy.orm import Session

from app.models.dining_table import Diningtable
from app.schemas.diningtable import DiningtableCreate, DiningtableUpdate


def create_table(db: Session, table: DiningtableCreate):

    db_table = Diningtable(**table.model_dump())

    db.add(db_table)
    db.commit()
    db.refresh(db_table)

    return db_table


def get_table(
        db: Session,
        table_id: int
):

    return (
        db.query(Diningtable)
        .filter(Diningtable.table_id == table_id)
        .first()
    )


def get_all_tables(db: Session):

    return db.query(Diningtable).all()


def update_table(
        db: Session,
        table_id: int,
        table: DiningtableUpdate
):

    db_table = get_table(db, table_id)

    if not db_table:
        return None

    update_data = table.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_table, key, value)

    db.commit()
    db.refresh(db_table)

    return db_table


def delete_table(
        db: Session,
        table_id: int
):

    db_table = get_table(db, table_id)

    if not db_table:
        return None

    db.delete(db_table)
    db.commit()

    return db_table
