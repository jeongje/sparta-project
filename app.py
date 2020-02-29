from flask import Flask, render_template, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent.db'
# https://stackoverflow.com/questions/14853694/python-jsonify-dictionary-in-utf-8
app.config['JSON_AS_ASCII'] = False #jsonify에서 한글이 안넘어갈 때 처리
db = SQLAlchemy(app)

class Tenants(db.Model):

    __tablename__ = 'TENANTS'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tenant_memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    delete_col = db.Column(db.Boolean, default=False)

    contracts = db.relationship('Contracts', backref='tenants')


    def __repr__(self):
        return '<Tenants %r>' % str(self.id)


class Contracts(db.Model):

    __tablename__ = 'CONTRACTS'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('TENANTS.id'), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    deposit = db.Column(db.Integer, nullable=False)
    monthly = db.Column(db.Integer, nullable=False)
    management_fee = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    contract_memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    delete_col = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Contracts %r>' % str(self.id)


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
        return render_template('/tenant_edit.html', tenant=tenant)
        
#html date input을 datetime으로 바꾸는
#https://stackoverflow.com/questions/46468497/type-of-the-received-date-input-from-html-is-class-string
@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.method == 'POST':
        contract_tenant_id = request.form['tenant_id']
        contract_address = request.form['address']
        contract_deposit = request.form['deposit']
        contract_monthly = request.form['monthly']
        contract_management_fee = request.form['management_fee']
        contract_start_date = request.form['start_date']
        contract_end_date = request.form['end_date']
        contract_contract_memo = request.form['contract_memo']
        new_contract = Contracts(
            tenant_id=contract_tenant_id,
            address=contract_address,
            deposit=contract_deposit,
            monthly=contract_monthly,
            management_fee=contract_management_fee,
            start_date=datetime.strptime(contract_start_date, '%Y-%m-%d').date(), #db형태에 맞춰져 변환
            end_date=datetime.strptime(contract_end_date, '%Y-%m-%d').date(), #db형태에 맞춰져 변환
            contract_memo=contract_contract_memo,
            )
        try:
            db.session.add(new_contract)
            db.session.commit()
            return redirect('/contracts')
        except:
            return "new_contract add error"
    else:
        # Contracts테이블과 Tenants테이블 join후 묶어서 넘기기
        contracts_tenants = db.session.query(
            Contracts, Tenants           
            ).outerjoin(Tenants, Contracts.tenant_id == Tenants.id).all()
        return render_template('/contracts.html', contracts_tenants=contracts_tenants)


@app.route('/tenants/name_list', methods=['GET'])
def name_list():
    name_list = []
    tenants = Tenants.query.all()
    for tenant in tenants:
        name_list.append(tenant.name)
    return jsonify({'result':'success', 'name_list':name_list})



if __name__ == "__main__":
    app.run(debug=True)