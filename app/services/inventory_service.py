from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.menu import Menu

def get_inventory(
    db: Session,
    menu_id: int
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.menu_id == menu_id
        )
        .first()
    )

    if inventory is None:
        raise ValueError(
            "Inventory record not found."
        )

    return inventory

def check_stock(
    db: Session,
    menu_id: int,
    quantity: int
):

    inventory = get_inventory(
        db,
        menu_id
    )

    if inventory.quantity_available < quantity:
        raise ValueError(
            "Insufficient stock."
        )

    return True

def reduce_stock(
    db: Session,
    menu_id: int,
    quantity: int
):

    inventory = get_inventory(
        db,
        menu_id
    )

    if inventory.quantity_available < quantity:
        raise ValueError(
            "Insufficient stock."
        )

    inventory.quantity_available -= quantity

    db.commit()

    db.refresh(inventory)

    return inventory

def increase_stock(
    db: Session,
    menu_id: int,
    quantity: int
):

    inventory = get_inventory(
        db,
        menu_id
    )

    inventory.quantity_available += quantity

    db.commit()

    db.refresh(inventory)

    return inventory

def restock_inventory(
    db: Session,
    menu_id: int,
    quantity: int
):

    return increase_stock(
        db,
        menu_id,
        quantity
    )

LOW_STOCK_LIMIT = 10
def is_low_stock(
    db: Session,
    menu_id: int
):

    inventory = get_inventory(
        db,
        menu_id
    )

    return (
        inventory.quantity_available
        <= LOW_STOCK_LIMIT
    )

def update_menu_availability(
    db: Session,
    menu_id: int
):

    inventory = get_inventory(
        db,
        menu_id
    )

    menu = (
        db.query(Menu)
        .filter(
            Menu.menu_id == menu_id
        )
        .first()
    )

    if menu is None:
        raise ValueError(
            "Menu item not found."
        )

    menu.is_available = (
        inventory.quantity_available > 0
    )

    db.commit()

    db.refresh(menu)

    return menu

def consume_inventory(
    db: Session,
    menu_id: int,
    quantity: int
):

    reduce_stock(
        db,
        menu_id,
        quantity
    )

    update_menu_availability(
        db,
        menu_id
    )