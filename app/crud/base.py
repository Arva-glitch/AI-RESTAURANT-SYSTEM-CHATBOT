from typing import Type, TypeVar, Generic

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):

        primary_key = list(self.model.__table__.primary_key)[0]

        return (
            db.query(self.model)
            .filter(primary_key == id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):

        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self,
        db: Session,
        obj
    ):

        db_obj = self.model(**obj.model_dump())

        db.add(db_obj)

        db.commit()

        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        id: int,
        obj
    ):

        db_obj = self.get(db, id)

        if db_obj is None:
            return None

        update_data = obj.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.commit()

        db.refresh(db_obj)

        return db_obj

    def delete(
        self,
        db: Session,
        id: int
    ):

        db_obj = self.get(db, id)

        if db_obj is None:
            return None

        db.delete(db_obj)

        db.commit()

        return db_obj
