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
    image = sa.Column(sa.String(), default="https://image.freepik.com/free-vector/flat-404-error-template_23-2147745731.jpg", nullable=False, comment="Картинка еды")
    price = sa.Column(sa.BigInteger(), nullable=False, comment="Цена еды")

    
# class User(BaseModel):
#     __tablename__ = "users"
    
#     id = sa.Column(
#         sa.BigInteger(), primary_key=True, autoincrement=True, comment="Идентификатор пользователя"
#     )
#     name = sa.Column(sa.String(), nullable=False, comment="Имя пользователя")
#     pfp = sa.Column(sa.String(), default="", nullable=True, comment="Аватар пользователя")
#     gender = sa.Column(sa.String(), nullable=False, comment="Пол пользователя")
#     email = sa.Column(sa.String(), nullable=False, comment="Эл. почта пользователя")
#     username = sa.Column(sa.String(), nullable=False, comment="Юзернейм пользователя")
#     password = sa.Column(sa.String(), nullable=False, comment="Пароль пользователя")
#     cart = 
# #     favorites = relationship("User")
    

# class Cart(BaseModel):
#     user_id = sa.Column(sa.ForeignKey("users.id"), primary_key=False, nullable=False, comment="Идентификатор пользователя")
#     food_id = sa.Column(sa.ForeignKey("foods.id", ondelete="CASCADE"), primary_key=False, nullable=False, comment="Идентификатор еды")
