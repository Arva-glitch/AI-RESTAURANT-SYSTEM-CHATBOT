from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.customer import Customer
from app.schemas.customers import CustomerCreate, CustomerUpdate


# def create_customer(
#     db: Session,
#     customer: CustomerCreate
# ):

#     db_customer = Customer(**customer.model_dump())

#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)

#     return db_customer

def create_customer(db: Session, customer: CustomerCreate):

    existing_customer = (
        db.query(Customer)
        .filter(
            or_(
                Customer.email == customer.email,
                Customer.phone == customer.phone
            )
        )
        .first()
    )

    if existing_customer:
        return None

    db_customer = Customer(**customer.model_dump())

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_customer(db: Session, customer_id: int):

    return (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )


def get_all_customers(
        db: Session,
        skip: int = 0,
        limit: int = 100
):

    return (
        db.query(Customer)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_customer(
        db: Session,
        customer_id: int,
        customer: CustomerUpdate
):

    db_customer = get_customer(db, customer_id)

    if not db_customer:
        return None

    update_data = customer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(
        db: Session,
        customer_id: int
):

    db_customer = get_customer(db, customer_id)

    if not db_customer:
        return None

    db.delete(db_customer)
    db.commit()

    return db_customer
