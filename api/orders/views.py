from flask_restx import Resource,Namespace,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from ..utils import db

order_namespace = Namespace('orders',description="Namespace for orders")

order_model =order_namespace.model(
    'Order',{
        'id':fields.Integer(description="An ID"),
        'size':fields.String(description="Size of order",required =True,
        enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']
        ),
        'order_status':fields.String(description="The status of the Order",
        required=True, eum =['PENDING','IN_TRANSITE','DELIVERED']
        ),
        # 'price':fields.String(description="The Price", required =True)
    }
)

order_staus_model = order_namespace.model(
    'OrderStatus',{
        'order_status': fields.String(required=True, description='Order Status',
        enum=['PENDING','IN_TRANSIT','DELIVERD'])
    }
)
order_place_or_update_model = order_namespace.model(
    'OrderPlaceOrUpdate',{
        'id':fields.Integer(description="An ID"),
        'size': fields.String(description ="Size of Order",required=True,
        enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']),
        'quatity': fields.String(description ="Quantity of the Order", required=True),
        'flavour': fields.Integer(description="Flaour of Order",required=True),
        'price': fields.Integer(description="Price of the item")
    }
)
@order_namespace.route('/order')
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description ="Retrieve all Orders"
    )
    @jwt_required()
    def get(self):
        """ get all orders"""
        
        orders = Order.query.all()

        return orders,HTTPStatus.OK
    
    @order_namespace.expect(order_place_or_update_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description="Place an Order"
    )
    @jwt_required()
    def post(self):
        """ Place new Order"""
        
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload

        new_order = Order(
            size=data['size'],
            quantity = data['quantity'],
            flavour = data['flavour'],
            price = data['price']
        )

        new_order.user = current_user
        new_order.save()
        return new_order, HTTPStatus.CREATED

@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description="Retrive an Order by ID",
        params={
            "order_id":"An ID for a given order"
        }

    )
    @jwt_required()
    def get(self,order_id):
        """
            Retrive order of specific id
        """
        order = Order.get_by_id(order_id)
        return order,HTTPStatus.OK

    @order_namespace.expect(order_place_or_update_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description="Update Order By ID",
        params={
            "order_id":"An ID for a given order"
        }
    )
    @jwt_required()
    def put(self,order_id):
        """
            Update order by id
        """
        order_to_update = Order.get_by_id(order_id)
        data = order_namespace.payload

        order_to_update.quantity = data['quantity']
        order_to_update.size = data['size']
        order_to_update.flavour = data['flavour']
        order_to_update.price = data['price']
        db.session.commit()

        return order_to_update, HTTPStatus.OK

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Delete Specific Order By Id",
        params={
            "order_id":"An ID for a given order"
        }
    )
    @jwt_required()
    def delete(self,order_id):
        """
            Delete order by id
        """
        order_id_delete = Order.get_by_id(order_id)
        order_id_delete.delete()
        return order_id_delete, HTTPStatus.OK
    
@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description="User Specifice Order",
        params={
            "user_id":"An User ID",
            "order_id":"An ID for a given order"
        }
    )
    @jwt_required()
    def get(self,user_id,order_id):
        """
            Get user specific order.
        """
        user = User.get_by_id(user_id)

        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()

        return order, HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):

    @order_namespace.marshal_list_with(order_model)
    @order_namespace.doc(
        description="Get all Order by Specific Username",
        params={
            "user_id":"An User ID"
        }
    )
    def get(self,user_id):
        """
            Get all Order By Specific User.
        """
        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK

@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):

    @order_namespace.expect(order_staus_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description="Update Delivery Status of the Order",
        params={
            "order_id":"An ID for a given order"
        }
    )
    @jwt_required()
    def patch(self,order_id):
        """
            Update an Order Status.
        """
        data = order_namespace.payload

        order_to_update = Order.get_by_id(order_id)

        order_to_update.order_status = data['order_status']
        
        db.session.commit()

        return order_to_update, HTTPStatus.OK




