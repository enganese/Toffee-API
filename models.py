import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa
from config import DB_URL


engine = sa.create_engine(DB_URL, echo=False)

SqlAlchemyBase = dec.declarative_base()


class BaseModel(SqlAlchemyBase):
    __abstract__ = True

    def __repr__(self):
        return "<class '{}' id:{}>".format(self.__class__.__name__, self.id)


class Food(BaseModel):
    __tablename__ = "foods"

    id = sa.Column(
        sa.BigInteger(), primary_key=True, autoincrement=True, comment="Идентификатор еды"
    )
    title = sa.Column(sa.String(), nullable=False, comment="Название еды")
    description = sa.Column(sa.String(), nullable=True, comment="Описание еды")
    amount = sa.Column(sa.BigInteger(), default=0, nullable=True, comment="Количество еды")
    price = sa.Column(sa.BigInteger(), nullable=False, comment="Цена еды")