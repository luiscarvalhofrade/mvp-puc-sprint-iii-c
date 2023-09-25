from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
import requests

from sqlalchemy.exc import IntegrityError

from models import Session, Order
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Order API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Doc", description="Doc selectin: Swagger, Redoc ou RapiDoc")
order_tag = Tag(name="Order", description="Addition, view and exclusion of orders")


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi, options of different kinds of docs.
    """
    return redirect('/openapi')


@app.post('/order', tags=[order_tag],
          responses={"200": OrderViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_order(form: OrderSchema):
    """Add new oredr in the db

    Return the order with all key values.
    """
    url = 'https://fakestoreapi.com/products/{product_id}'.format(product_id = form.product_id)
    fakeStoreApi = requests.get(url)
    data = fakeStoreApi.json()
    totalval = (data["price"] * form.quantity)

    order = Order(
        quantity=form.quantity,
        value=totalval,
        title = data["title"],
        price = data["price"],
        description = data["description"],
        category = data["category"],
        image = data["image"])
    logger.debug(f"Adicionando pedido de id: '{order.id}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(order)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pedido de id: '{order.id}'")
        return show_order(order), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pedido de mesmo id já salvo na base :/"
        logger.warning(f"Erro ao adicionar pedido '{order.id}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo pedido :/"
        logger.warning(f"Erro ao adicionar pedido '{order.id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/orders', tags=[order_tag],
         responses={"200": OrderListSchema, "404": ErrorSchema})
def get_orders():
    """Return all orders in the db

    Return a list of order.
    """
    logger.debug(f"Coletando pedidos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    orders = session.query(Order).all()

    if not orders:
        # se não há pedidos cadastrados
        return {"orders": []}, 200
    else:
        logger.debug(f"%d orders found" % len(orders))
        # retorna a representação de pedido
        print(orders)
        return show_orders(orders), 200


@app.get('/order', tags=[order_tag],
         responses={"200": OrderViewSchema, "404": ErrorSchema})
def get_order(query: OrderSearchSchema):
    """Return an specific order by a given id

    Return a specific order.
    """
    order_id = query.id
    logger.debug(f"Collecting data about order #{order_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        # se o pedido não foi encontrado
        error_msg = "Order not found!"
        logger.warning(f"Error searching order '{order_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Order found: '{order.id}'")
        # retorna a representação de produto
        return show_order(order), 200


@app.delete('/order', tags=[order_tag],
            responses={"200": OrderDelSchema, "404": ErrorSchema})
def del_produto(query: OrderSearchSchema):
    """Delete an order by a given id

    Return a message of success and the deleted order id.
    """
    order_id = query.id
    print(order_id)
    logger.debug(f"Deleting data from order #{order_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Order).filter(Order.id == order_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deleting order #{order_id}")
        return {"mesage": "Order deleted", "id": order_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Order not found!"
        logger.warning(f"Error deleting order #'{order_id}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.put('/order', tags=[order_tag],
          responses={"200": OrderViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_order(form: OrderUpdateSchema):
    """Update one order in the db

    Return the updated order.
    """
    order_id = form.id
    try:
        session = Session()
        order = session.query(Order).filter(Order.id == order_id)
        order.update(
            {
                Order.quantity:form.quantity,
                Order.value: Order.price * form.quantity
            }
        )
        session.commit()
        logger.debug(f"Atualizando pedido de id: '{order_id}'")
        return show_order_update(order), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pedido de mesmo id já salvo na base :/"
        logger.warning(f"Erro ao atualizar pedido '{order_id}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo pedido :/"
        logger.warning(f"Erro ao adicionar pedido '{order_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    
    