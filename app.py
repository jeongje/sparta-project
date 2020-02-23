from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent.db'
db = SQLAlchemy(app)

class Tenants(db.Model):

    __tablename__ = 'TENANTS'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tenant_memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    delete_col = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Tenants %r>' % str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tenants', methods=['GET', 'POST'])
def tenants():
    if request.method == 'POST':
        tenant_name = request.form['name']
        tenant_phone = request.form['phone']
        tenant_memo = request.form['tenant_memo']
        new_tenant = Tenants(name=tenant_name, phone=tenant_phone, tenant_memo=tenant_memo)
        
        try:
            db.session.add(new_tenant)
            db.session.commit()
            return redirect('/tenants')
        except:
            return "new_tenant add error"
    else:
        tenants = Tenants.query.order_by(Tenants.created_at).all()
        return render_template('tenants.html', tenants=tenants)

@app.route('/tenants/delete/<int:id>', methods=['GET'])
def tenant_delete(id):
    tenant = Tenants.query.get_or_404(id)
    tenant.delete_col = True

    try:
        db.session.commit()
    except:
        return "tenant delete error"
    
    tenants = Tenants.query.order_by(Tenants.created_at).all()
    return render_template('/tenants.html', tenants=tenants)


@app.route('/tenants/edit/<int:id>', methods=['GET', 'POST'])
def tenant_edit(id):
    tenant = Tenants.query.get_or_404(id)
    if request.method == 'POST':
        tenant.name = request.form['name']
        tenant.phone = request.form['phone']
        tenant.tenant_memo = request.form['tenant_memo']

        try:
            db.session.commit()
            return redirect('/tenants')
        except:
            return "tenant edit error"
        
    else:
        return render_template('/edit.html', tenant=tenant)
        

   



if __name__ == "__main__":
    app.run(debug=True)