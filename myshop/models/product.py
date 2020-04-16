import pendulum
import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db
from myshop.libs import file


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.String(100), nullable=False)
    
    price = db.Column(db.Integer, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, ForeignKey("users.id"), default=0)

    stok = db.Column(db.Integer, default=0)

    image = db.Column(db.String(50), default="")

    image_thumb = db.Column(db.String(50), default="")

    image_icon = db.Column(db.String(50), default="")

    video = db.Column(db.String(50), default="")

    total_view = db.Column(db.Integer, default=0)

    total_review = db.Column(db.Integer, default=0)

    created_on = db.Column(db.DateTime, default=0)

    is_deleted = db.Column(db.Integer, default=0)

    updated_on = db.Column(db.DateTime, default=0)

    user = relationship("Users", backref="products")

    def __init__(self, title, description, price, category, stok, user_id):
        """
        Args:
            title: nama produk
            price: harga produk
            category: kategori produk
        """
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.stok = stok
        self.user_id = user_id
        
        self.created_on = pendulum.now()

    def set_image(self, imagefile: str = None, filename: str = None):
        self.image = file.save(imagefile, 'products', filename)

    @property
    def image_url(self):
        return file.url(self.image, 'products')

    def set_image_thumb(self, imagefile: str = None, filename: str = None):
        self.image_thumb = file.save(imagefile, 'products_thumb', filename)

    @property
    def image_thumb_url(self):
        return file.url(self.image_thumb, 'products_thumb')

    def set_image_icon(self, imagefile: str = None, filename: str = None):
        self.image_icon = file.save(imagefile, 'products_icon', filename)

    @property
    def image_icon_url(self):
        return file.url(self.image_icon, 'products_icon')

    def set_video(self, videofile: str = None, filename: str = None):
        self.video = file.save(videofile, 'products_video', filename)

    @property
    def video_url(self):
        return file.url(self.video, 'products_video')

def get_by_id(product_id) -> Products:
    product = Products.query.filter_by(id=product_id, is_deleted=0).first()

    return product