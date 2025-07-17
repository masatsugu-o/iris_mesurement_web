from datetime import datetime
from apps.app import db

class Customer(db.Model):
    __tablename__ = "costomers"
    id = db.Column(db.Integer, primary_key=True)
    # user_idはusersテーブルのidカラムを外部キーとして設定する
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    customer_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    memo = db.Column(db.Text)
    result = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)