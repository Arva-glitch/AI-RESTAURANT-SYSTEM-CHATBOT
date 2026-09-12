from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


def create_menu_item(db: Session, menu: MenuCreate):

    db_menu = Menu(**menu.model_dump())

    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    return db_menu


def get_menu_item(db: Session, menu_id: int):

    return (
        db.query(Menu)
        .filter(Menu.menu_id == menu_id)
        .first()
    )


def get_all_menu_items(db: Session):

    return db.query(Menu).all()


def update_menu_item(db: Session, menu_id: int, menu: MenuUpdate):

    db_menu = get_menu_item(db, menu_id)

    if not db_menu:
        return None

    update_data = menu.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_menu, key, value)

    db.commit()
    db.refresh(db_menu)

    return db_menu


def delete_menu_item(db: Session, menu_id: int):

    db_menu = get_menu_item(db, menu_id)

    if not db_menu:
        return None

    db.delete(db_menu)
    db.commit()

    return db_menu
