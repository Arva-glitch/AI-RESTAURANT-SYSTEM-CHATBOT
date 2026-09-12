from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


def create_address(db: Session, address: AddressCreate):

    db_address = Address(**address.model_dump())

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address


def get_address(db: Session, address_id: int):

    return (
        db.query(Address)
        .filter(Address.address_id == address_id)
        .first()
    )


def get_addresses_by_customer(
        db: Session,
        customer_id: int
):

    return (
        db.query(Address)
        .filter(Address.customer_id == customer_id)
        .all()
    )


def update_address(
        db: Session,
        address_id: int,
        address: AddressUpdate
):

    db_address = get_address(db, address_id)

    if not db_address:
        return None

    update_data = address.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)

    return db_address


def delete_address(
        db: Session,
        address_id: int
):

    db_address = get_address(db, address_id)

    if not db_address:
        return None

    db.delete(db_address)
    db.commit()

    return db_address
