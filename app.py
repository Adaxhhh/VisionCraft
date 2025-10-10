from flask import Flask, render_template

app = Flask(__name__)

# Example handicraft data
products = [
    {
        "id": 1,
        "name": "Terracotta Pot",
        "price": 299,
        "image": "images/pottery.jpg",
        "description": "Handmade terracotta pot from Rajasthan."
    },
    {
        "id": 2,
        "name": "Wooden Toy Elephant",
        "price": 499,
        "image": "images/wooden_toy.jpg",
        "description": "Carved wooden elephant from Karnataka."
    },
    {
        "id": 3,
        "name": "Bamboo Basket",
        "price": 349,
        "image": "images/basket.jpg",
        "description": "Eco-friendly bamboo basket from Assam."
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/ar/<int:product_id>')
def view_in_ar(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template('ar.html', product=product)


@app.route('/product/<int:product_id>')
def product_page(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
