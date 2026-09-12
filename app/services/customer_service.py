from datetime import date
from app.schemas.customers import CustomerCreate
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.crud.customer import (
    create_customer,
    get_customer,
    get_all_customers,
    update_customer,
    delete_customer
)

from app.models.customer import Customer
from app.schemas.customers import (
    CustomerCreate,
    CustomerUpdate
)

# -----------------------general functions-------------------------


def register_customer(
    db: Session,
    customer: CustomerCreate
):

    return create_customer(
        db,
        customer
    )


def fetch_customer(
    db: Session,
    customer_id: int
):

    return get_customer(
        db,
        customer_id
    )


def fetch_all_customers(
    db: Session
):

    return get_all_customers(
        db
    )


def modify_customer(
    db: Session,
    customer_id: int,
    customer: CustomerUpdate
):

    return update_customer(
        db,
        customer_id,
        customer
    )


def remove_customer(
    db: Session,
    customer_id: int
):

    return delete_customer(
        db,
        customer_id
    )

# -------------------------------------------------------------------------------------------

# ----------------------chatbot specific services--------------------------------------------


def get_customer_by_telegram_id(
    db: Session,
    telegram_id: int
):

    return (
        db.query(Customer)
        .filter(
            Customer.telegram_id == telegram_id
        )
        .first()
    )


def get_customer_by_email(
    db: Session,
    email: str
):

    return (
        db.query(Customer)
        .filter(
            Customer.email == email
        )
        .first()
    )


def get_customer_by_phone(
    db: Session,
    phone: str
):

    return (
        db.query(Customer)
        .filter(
            Customer.phone == phone
        )
        .first()
    )


def check_customer(
    db: Session,
    phone: str
):

    customer = get_customer_by_phone(
        db,
        phone
    )
    return {
        "exists": customer is not None,
        "customer": customer
    }


def link_existing_customer(
    db: Session,
    customer: Customer,
    telegram_id: int,
    username: str | None = None
):
    customer.telegram_id = telegram_id
    customer.username = username or customer.first_name

    db.commit()
    db.refresh(customer)

    return customer


def register_telegram_customer(
    db: Session,
    telegram_id: int,
    username: str | None,
    first_name: str,
    phone: str
):
    customer = Customer(
        telegram_id=telegram_id,
        username=username or "",
        first_name=first_name,
        last_name="",
        phone=phone,
        email=None,
        gender=None,
        date_of_birth=None,
        favourite_cuisine=None,
        spice_preference=None,
        dietary_preference=None,
        preferred_table_type=None,
        total_orders=0,
        total_members=1,
        created_at=date.today()
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer
