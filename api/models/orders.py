from ..utils import db 
from enum import Enum
from datetime import datetime
class Sizes(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE ='large'
    EXTRA_LARGE ='extra_large'

class OrderStatus(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'


class Order(db.Model):

    __tablename__='orders'
    id = db.Column(db.Integer(),primary_key=True)
    size = db.Column(db.Enum(Sizes),default =Sizes.SMALL)
    order_status = db.Column(db.Enum(OrderStatus),default = OrderStatus.PENDING)
    flavour = db.Column(db.String(),nullable=False)
    quantity = db.Column(db.Integer(),nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2),nullable = False)
    date_created = db.Column(db.DateTime(),default=datetime.utcnow)
    customer = db.Column(db.Integer(),db.ForeignKey('users.id'))


    def __str__(self):
        return f"<Order {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    # cls contain the model class Order here
    # we are passing parameter Model class Order and id to get_or_404(Entity=Order,primarykey=id) method.
    # by keeping method as class method.
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()