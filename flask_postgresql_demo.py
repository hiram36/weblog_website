from flask import Flask  
from flask.ext.admin import Admin  
from flask.ext.admin import BaseView  
from flask.ext.admin import expose  
from flask.ext.sqlalchemy import SQLAlchemy  
from flask.ext.admin.contrib.sqla import ModelView  
  
  
app = Flask(__name__)  
  
app.config['SECRET_KEY'] = '123456790'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://weblogadmin:pgsql123@localhost:1921/weblogdb'  
  
db = SQLAlchemy(app)  
  
  
admin = Admin(app)  
  
class MyView(BaseView):  
    @expose('/')  
    def index(self):  
        return self.render('index.html')  
  
class Cars(db.Model):  
      
    can_create = False  
      
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(64))  
    price = db.Column(db.String(64))  
      
admin.add_view(MyView(name='Hello'))  
admin.add_view(ModelView(Cars, db.session))  
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=8080,debug=True)  
