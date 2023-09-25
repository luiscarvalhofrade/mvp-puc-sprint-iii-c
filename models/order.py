from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models import Base

class Order(Base):
    """
        Cria um Pedido

        Arguments:
            quantity: quantidade que se espera comprar daquele produto
            created_at: data de quando o pedido foi inserido à base
        """
    __tablename__ = 'order'

    id = Column("pk_order", Integer, primary_key=True)
    quantity = Column(Integer)
    value = Column(Float)
    title = Column(String)
    price = Column(Float)
    description = Column(String)
    category = Column(String)
    image = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, quantity:int, value:float,
                 title:str, price:float, description:str, 
                 category:str, image:str,
                 created_at:Union[DateTime, None] = None):
        """
        Cria uma Pedido

        Arguments:
            quantidade: quantidade do produto no pedido
            created_at: data de quando o pedido foi inserido à base
        """
        self.quantity = quantity
        self.title = title
        self.price = price
        self.description = description
        self.category = category
        self.image = image
        self.value = value

        # se não for informada, será o data exata da inserção no banco
        if created_at:
            self.created_at = created_at