#!/usr/bin/env python3
"""Flask app"""

from config import app, db
from flask import redirect, render_template, request, url_for, session, flash
from model import Product, ProductSchema, ProductAddForm
from model import db


@app.route("/")
def show_homepage():
    products = db.session.query(Product).all()
    return render_template("displayproduct.html", products = products)

@app.route("/farmerdashboard")
def show_inventory():
    """Show animals in the DB"""
    inventory = db.session.query(Product).all()
    schema = ProductSchema(many=True)
    return render_template("index.html", inventory=schema.dump(inventory))

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Initialize the cart if it doesn't exist
    if "cart" not in session:
        session["cart"] = []

    # Check if the product is already in the cart
    cart = session["cart"]
    if product_id in cart:
        flash("Item already in cart!", "info")
    else:
        cart.append(product_id)
        session["cart"] = cart  # Update session
        flash("Item added to cart!", "success")

    return redirect(url_for("show_homepage"))


@app.route("/cart")
def view_cart():
    if "cart" not in session or not session["cart"]:
        return render_template("cart.html", cart_items=[], empty=True)

    # Fetch product details for items in the cart
    cart_items = Product.query.filter(Product.id.in_(session["cart"])).all()
    return render_template("cart.html", cart_items=cart_items, empty=False)

@app.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    if "cart" in session and product_id in session["cart"]:
        session["cart"].remove(product_id)
        session.modified = True  # Inform Flask that session has been modified
        flash("Item removed from cart!", "warning")

    return redirect(url_for("view_cart"))
@app.get("/add")
def view_add_form() -> str:
    """Display an add animal form"""
    return render_template("add_form.html", form=ProductAddForm())


@app.post("/add")
def handle_add_form():
    """Add an animal"""
    form = ProductAddForm(request.form)
    if not form.validate():
        return redirect(url_for("view_add_form"), 302)
    
    product = Product()
    product.name = form.name.data
    product.price = form.price.data
    product.description = form.description.data
    product.image_url = form.image_url.data
    product.availability = form.availability.data
    db.session.add(product)
    db.session.commit()
    return redirect(url_for("show_inventory"), 302)


@app.route("/delete/<int:product_id>", methods=["delete", "post"])
def delete_product(product_id: int):
    db.session.query(Product).filter_by(id=product_id).delete()
    db.session.commit()
    return redirect(url_for("show_inventory"), 302)

with app.app_context():
    db.create_all()