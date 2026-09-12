from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate


def create_inventory_item(db: Session, inventory: InventoryCreate):

    db_inventory = Inventory(**Inventory.model_dump())

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory


def get_inventory_item(db: Session, inventory_id: int):

    return (
        db.query(Inventory)
        .filter(Inventory.inventory_id == inventory_id)
        .first()
    )


def get_all_inventory_items(db: Session):

    return db.query(Inventory).all()


def update_inventory_item(db: Session, inventory_id: int, inventory: InventoryUpdate):

    db_inventory = get_inventory_item(db, inventory_id)

    if not db_inventory:
        return None

    update_data = inventory.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_inventory, key, value)

    db.commit()
    db.refresh(db_inventory)

    return db_inventory


def delete_inventory_item(db: Session, inventory_id: int):

    db_inventory = get_inventory_item(db, inventory_id)

    if not db_inventory:
        return None

    db.delete(db_inventory)
    db.commit()

    return db_inventory
