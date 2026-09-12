from decimal import Decimal
from sqlalchemy.orm import Session

from app.crud.bill import bill_crud
from app.schemas.bill import BillCreate

GST_PERCENTAGE = Decimal("5.00")


def calculate_tax(
    subtotal: Decimal
) -> Decimal:

    return (
        subtotal * GST_PERCENTAGE
    ) / Decimal("100")


def calculate_total(
    subtotal: Decimal,
    tax: Decimal,
    discount: Decimal
) -> Decimal:

    return subtotal + tax - discount


def generate_bill(
    db: Session,
    order_id: int,
    subtotal: Decimal,
    tax: Decimal,
    discount: Decimal,
    total: Decimal
):

    bill = BillCreate(

        order_id=order_id,

        subtotal=subtotal,

        tax_amount=tax,

        discount_amount=discount,

        total_amount=total,

        bill_status="Generated"
    )

    return bill_crud.create(
        db,
        bill
    )


def process_bill(
    db: Session,
    order_id: int,
    subtotal: Decimal,
    discount: Decimal = Decimal("0.00")
):
    tax = calculate_tax(
        subtotal
    )
    total = calculate_total(
        subtotal,
        tax,
        discount
    )
    bill = generate_bill(
        db,
        order_id,
        subtotal,
        tax,
        discount,
        total
    )

    return bill
