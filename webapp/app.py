# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'python123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(500), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(150), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)  # Normally, only store last 4 digits or use encryption
    expiry_date = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    billing_address = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes for static pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for bakery menu
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Route for checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Handle checkout logic here (e.g., creating an order)
        flash('Checkout completed successfully!', 'success')
        return redirect(url_for('billing'))
    return render_template('checkout.html')

# Route for billing page
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        # Payment processing data
        if 'card-name' in request.form:
            card_name = request.form['card-name']
            card_number = request.form['card-number']
            expiry_date = request.form['expiry-date']
            cvv = request.form['cvv']
            billing_address = request.form['billing-address']

            # Mask the card number (store only the last 4 digits)
            masked_card_number = f'**** **** **** {card_number[-4:]}'

            # Use a dummy user_id for demonstration; replace with actual user ID
            user_id = 1  

            # Save billing information to the database
            new_billing = Billing(
                card_name=card_name,
                card_number=masked_card_number,
                expiry_date=expiry_date,
                cvv=cvv,
                billing_address=billing_address,
                user_id=user_id
            )
            db.session.add(new_billing)
            db.session.commit()

            flash('Payment processed successfully!', 'success')
            return redirect(url_for('home'))
        
        # Item display data
        else:
            item_name = request.form['item-name']
            item_price = request.form['item-price']
            item_image = request.form['item-image']
            # Pass item details to render on billing page
            return render_template('billing.html', item_name=item_name, item_price=item_price, item_image=item_image)

    # Render billing page on a GET request
    return render_template('billing.html')

    return render_template('billing.html')

# User registration and listing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('register.html')

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

# Create the database and tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000, debug=True)