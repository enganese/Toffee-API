from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa
from config import DB_URL
import sqlalchemy.ext.declarative as dec


engine = sa.create_engine(DB_URL, echo=False)

SqlAlchemyBase = dec.declarative_base()


class BaseModel(SqlAlchemyBase):
    __abstract__ = True

    def __repr__(self):
        return "<class '{}' id:{}>".format(self.__class__.__name__, self.id)


class BaseModelForCart(SqlAlchemyBase):
    __abstract__ = True

    def __repr__(self):
        return f"<class '{self.__class__.__name__}' food_id:{self.food_id}>"


class Food(BaseModel):
    __tablename__ = "foods"

    id = sa.Column(
        sa.BigInteger(), primary_key=True, autoincrement=True, comment="Идентификатор еды"
    )
    title = sa.Column(sa.String(), nullable=False, comment="Название еды")
    description = sa.Column(sa.String(), nullable=True, comment="Описание еды")
    ingredients = sa.Column(sa.String(), nullable=True, comment="Ингредиенты еды")
    image = sa.Column(sa.String(), default="https://image.freepik.com/free-vector/flat-404-error-template_23-2147745731.jpg", nullable=False, comment="Картинка еды")
    price = sa.Column(sa.BigInteger(), nullable=False, comment="Цена еды")
    saved = relationship("Cart", backref=backref("food", cascade="all, delete"))


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(
        sa.BigInteger(), primary_key=True, autoincrement=True, comment="Идентификатор пользователя"
    )
    name = sa.Column(sa.String(), nullable=False, comment="Имя пользователя")
    pfp = sa.Column(sa.String(), default="", nullable=True, comment="Аватар пользователя")
    gender = sa.Column(sa.String(), nullable=False, comment="Пол пользователя")
    email = sa.Column(sa.String(), nullable=False, comment="Эл. почта пользователя")
    phone_number = sa.Column(sa.String(), nullable=False, comment="Номер телефона пользователя")
    password = sa.Column(sa.String(), nullable=False, comment="Пароль пользователя")
    saved = relationship("Cart", backref=backref("user", cascade="all, delete"))
#     favorites = relationship("User")


class Cart(BaseModelForCart):
    __tablename__ = "saved_foods"

    food_id = sa.Column(sa.ForeignKey("foods.id"), nullable=False, primary_key=True)

    user_id = sa.Column(sa.ForeignKey("users.id"), nullable=False, primary_key=True)

    food_qty = sa.Column(sa.BigInteger(), nullable=False, default=1)


# if __name__ == "__main__":
#     BaseModel.metadata.create_all(engine)
