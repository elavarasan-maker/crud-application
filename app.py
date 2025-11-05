from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_random_secret'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'instance', 'app.db')
os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False, default=0)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        try:
            quantity = int(quantity)
        except ValueError:
            flash('Quantity must be a number.','danger')
            return redirect(url_for('create'))
        item = Item(name=name, description=description, quantity=quantity)
        db.session.add(item)
        db.session.commit()
        flash('Item created successfully!','success')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        try:
            item.quantity = int(request.form['quantity'])
        except ValueError:
            flash('Quantity must be a number.','danger')
            return redirect(url_for('update', id=id))
        db.session.commit()
        flash('Item updated successfully!','success')
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!','success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
