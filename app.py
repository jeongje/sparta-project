from flask import Flask, render_template, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rent.db'
# https://stackoverflow.com/questions/14853694/python-jsonify-dictionary-in-utf-8
app.config['JSON_AS_ASCII'] = False  # jsonify에서 한글이 안넘어갈 때 처리
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Tenants(db.Model):

    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
    delete_col = db.Column(db.Boolean, default=False)

    contracts = db.relationship('Contracts', backref='tenants')
    deposit_history = db.relationship('DepositHistory', backref='tenants')

    def __repr__(self):
        return '<Tenants %r>' % str(self.id)


class Contracts(db.Model):

    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(
        'tenants.id'), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    deposit = db.Column(db.Integer, nullable=False)
    monthly = db.Column(db.Integer, nullable=False)
    management_fee = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
    delete_col = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Contracts %r>' % str(self.id)


class DepositHistory(db.Model):

    __tablename__ = 'deposit_history'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(
        'tenants.id'), nullable=False)
    depositor = db.Column(db.String(20), nullable=False)
    deposit_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
    delete_col = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<DepositHistory %r>' % str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tenants', methods=['GET', 'POST'])
def tenants():
    if request.method == 'POST':
        tenant_name = request.form['name']
        tenant_phone = request.form['phone']
        tenant_memo = request.form['memo']
        # 시간이 동일하게 출력되는 문제가 있었다. 이건 db에서 default지정의 의미를 이해 못해서 생긴 문제
        # db에서 default는 db가 호출되는 시간. 따라서 그 시간이 계속 저장된 새로 post요청 보낼 때 다시 시간을 입력해줘야 함
        tenant_created_at = datetime.utcnow()+timedelta(hours=9)
        new_tenant = Tenants(name=tenant_name, phone=tenant_phone,
                             memo=tenant_memo, created_at=tenant_created_at)

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
        tenant.memo = request.form['memo']

        try:
            db.session.commit()
            return redirect('/tenants')
        except:
            return "tenant edit error"

    else:
        return render_template('/tenant_edit.html', tenant=tenant)

# html date input을 datetime으로 바꾸는
# https://stackoverflow.com/questions/46468497/type-of-the-received-date-input-from-html-is-class-string
@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.method == 'POST':
        # 이름을 받아서 tenant_id로 변경 > 동명이인 처리 안됨
        tenant_name = request.form['tenant_name']
        tenant_id = Tenants.query.filter(
            Tenants.name == tenant_name).first().id
        # Contracts 테이블에 넣기
        contract_tenant_id = tenant_id
        contract_address = request.form['address']
        contract_deposit = request.form['deposit']
        contract_monthly = request.form['monthly']
        contract_management_fee = request.form['management_fee']
        contract_start_date = request.form['start_date']
        contract_end_date = request.form['end_date']
        contract_memo = request.form['memo']
        contract_created_at = datetime.utcnow()+timedelta(hours=9)

        new_contract = Contracts(
            tenant_id=contract_tenant_id,
            address=contract_address,
            deposit=contract_deposit,
            monthly=contract_monthly,
            management_fee=contract_management_fee,
            start_date=datetime.strptime(
                contract_start_date, '%Y-%m-%d').date(),  # db형태에 맞춰져 변환
            end_date=datetime.strptime(
                contract_end_date, '%Y-%m-%d').date(),  # db형태에 맞춰져 변환
            memo=contract_memo,
            created_at=contract_created_at,
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
        ).outerjoin(Tenants, Contracts.tenant_id == Tenants.id).order_by(Contracts.created_at).all()
        return render_template('/contracts.html', contracts_tenants=contracts_tenants)


@app.route('/tenants/name_list', methods=['GET'])
def name_list():
    name_list = []
    tenants = Tenants.query.all()
    for tenant in tenants:
        name_list.append(tenant.name)
    return jsonify({'result': 'success', 'name_list': name_list})


@app.route('/deposit_history', methods=['GET', 'POST'])
def deposit_histroy():
    if request.method == 'POST':
        # 이름을 받아서 tenant_id로 변경 > 동명이인 처리 안됨
        tenant_name = request.form['tenant_name']
        tenant_id = Tenants.query.filter(
            Tenants.name == tenant_name).first().id
        # DepositHistory 테이블에 넣기
        deposit_tenant_id = tenant_id
        deposit_depositor = request.form['depositor']
        deposit_deposit_date = request.form['deposit_date']
        deposit_amount = request.form['amount']
        deposit_memo = request.form['memo']
        deposit_created_at = datetime.utcnow()+timedelta(hours=9)

        new_deposit_history = DepositHistory(
            tenant_id=deposit_tenant_id,
            depositor=deposit_depositor,
            deposit_date=datetime.strptime(
                deposit_deposit_date, '%Y-%m-%d').date(),  # db형태에 맞춰져 변환
            amount = deposit_amount,
            memo=deposit_memo,
            created_at=deposit_created_at,
        )

        try:
            db.session.add(new_deposit_history)
            db.session.commit()
            return redirect('/deposit_history')
        except:
            return "new_deposit_history add error"
    else:
        # DepositHistory테이블과 Tenants테이블 join후 묶어서 넘기기 > 넘긴 뒤 두개를 분리해줘야 함 (여기서 나눠서 주는것도 가능할 듯)
        deposit_all_tenants = db.session.query(
            DepositHistory, Tenants
        ).outerjoin(Tenants, DepositHistory.tenant_id == Tenants.id).order_by(DepositHistory.created_at).all()
        return render_template('/deposit_history.html', deposit_all_tenants=deposit_all_tenants)


if __name__ == "__main__":
    # app.run('0.0.0.0',port=5000,debug=True) # 서버올릴 때는 이렇게
    app.run(debug=True)
