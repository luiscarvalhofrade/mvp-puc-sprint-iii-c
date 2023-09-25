from pydantic import BaseModel
from typing import List
from models.order import Order


class OrderSchema(BaseModel):
    """ Define como um novo pedido a ser inserido deve ser representado
    """
    product_id: int = 10
    quantity: int = 12


class OrderSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do pedido.
    """
    id: int = 10


class OrderListSchema(BaseModel):
    """ Define como uma listagem de pedidos será retornada.
    """
    order:List[OrderSchema]


def show_orders(orders: List[Order]):
    """ Retorna uma representação do pedido seguindo o schema definido em
        OrderViewSchema.
    """
    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "quantity": order.quantity,
            "value": order.value,
            "title": order.title,
            "price": order.price,
            "description": order.description,
            "category": order.category,
            "image": order.image
        })

    return {"orders": result}


class OrderViewSchema(BaseModel):
    """ Define como um pedido será retornado: pedido + produtos.
    """
    id: int = 1
    quantity: int = 12
    value: float = 12.50
    title: str = "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"
    price: float = 109.95
    description: str = "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday"
    category: str = "men's clothing"
    image: str = "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg"


class OrderDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

def show_order(order: Order):
    """ Retorna uma representação do pedido seguindo o schema definido em
        OrderViewSchema.
    """
    return {
        "id": order.id,
        "quantity": order.quantity,
        "value": order.value,
        "title": order.title,
        "price": order.price,
        "description": order.description,
        "category": order.category,
        "image": order.image
    }

def show_order_update(order: Order):
    return {
        "id": order.id,
        "quantity": order.quantity,
        "value": order.value
    }

class OrderUpdateSchema(BaseModel):
    id: int
    quantity: int
