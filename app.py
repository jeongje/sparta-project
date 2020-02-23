from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent.db'
db = SQLAlchemy(app)

class Tenants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tenant_memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Tenants %r>' % str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tenants')
def tenants():
    return render_template('tenants.html')


if __name__ == "__main__":
    app.run(debug=True)