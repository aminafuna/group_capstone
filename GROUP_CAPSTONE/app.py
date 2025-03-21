# sudo systemctl stop apache2

from connections.functions import *
from connections.database import *

app = Flask(__name__)

app.secret_key = "For_FInals_Capstone"

@app.route('/')
def Home():
    if 'email' in session:
        
        return render_template("index.html", session = session['email'])
    else: 
        return render_template("index.html")

@app.route("/about")
def About():
    return render_template("about.html")


@app.route("/login")
def Login():
    return render_template("signin.html")

@app.route("/signin")
def Signin():
    return render_template("signin.html")

@app.route("/product")
def Product():
    products = Products()
    return render_template("product.html", products = products)

@app.route("/contact")
def Contact():
    return render_template("contact.html")

@app.route("/cart")
def Cart():
    if "email" in session:
        user_data = Get_userid(session["email"])
        user_id = user_data['Cust_ID']
        
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = """
        SELECT Cart.cart_id, Cart.user_id, Cart.product_id, Cart.quantity, 
               Products.Product_Name, Products.price, Products.picture,
               (Cart.quantity * Products.price) as total_price
        FROM Cart
        JOIN Products ON Cart.product_id = Products.Product_ID
        WHERE Cart.user_id = %s
        """
        cursor.execute(sql, (user_id,))
        cart_items = cursor.fetchall()
        
        subtotal = sum(item['total_price'] for item in cart_items)
        shipping = 10 if cart_items else 0  
        total = subtotal + shipping
        
        cursor.close()
        conn.close()
        
        email = session['email']
        result = Display_All(email)
        return render_template("cart.html", cart_items=cart_items, 
                              subtotal=subtotal, shipping=shipping, 
                              total=total, result=result)
    else:
        return redirect(url_for("Login"))

@app.route("/update_cart_quantity", methods=["POST"])
def update_cart_quantity():
    if "email" not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    cart_id = request.form.get("cart_id")
    quantity = request.form.get("quantity")
    
    if not cart_id or not quantity:
        return jsonify({"error": "Missing parameters"}), 400
    
    try:
        cart_id = int(cart_id)
        quantity = int(quantity)
        
        if quantity < 1:
            return jsonify({"error": "Quantity must be at least 1"}), 400
            
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "UPDATE Cart SET quantity = %s WHERE cart_id = %s",
            (quantity, cart_id)
        )
        
        cursor.execute(
            """
            SELECT Cart.cart_id, Cart.quantity, Products.price, 
                  (Cart.quantity * Products.price) as total_price
            FROM Cart
            JOIN Products ON Cart.product_id = Products.Product_ID
            WHERE Cart.cart_id = %s
            """,
            (cart_id,)
        )
        updated_item = cursor.fetchone()
        
        cursor.execute(
            """
            SELECT SUM(Cart.quantity * Products.price) as subtotal
            FROM Cart 
            JOIN Products ON Cart.product_id = Products.Product_ID
            WHERE Cart.user_id = (SELECT user_id FROM Cart WHERE cart_id = %s)
            """,
            (cart_id,)
        )
        result = cursor.fetchone()
        
        subtotal = float(result['subtotal']) if result and result['subtotal'] else 0
        shipping = 10.0 if subtotal > 0 else 0.0
        total = subtotal + shipping
        item_total = float(updated_item['total_price']) if updated_item else 0
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "item_total": item_total,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    if "email" not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    cart_id = request.form.get("cart_id")
    
    if not cart_id:
        return jsonify({"error": "Missing cart_id"}), 400
    
    try:
        cart_id = int(cart_id)
        
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT user_id FROM Cart WHERE cart_id = %s", (cart_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Cart item not found", "success": False}), 404
        
        user_id = result['user_id']
        
        cursor.execute("DELETE FROM Cart WHERE cart_id = %s", (cart_id,))
        
        cursor.execute(
            """
            SELECT SUM(Cart.quantity * Products.price) as subtotal
            FROM Cart 
            JOIN Products ON Cart.product_id = Products.Product_ID
            WHERE Cart.user_id = %s
            """,
            (user_id,)
        )
        result = cursor.fetchone()
        
        subtotal = float(result['subtotal']) if result and result['subtotal'] else 0
        shipping = 10.0 if subtotal > 0 else 0.0
        total = subtotal + shipping
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@app.route("/profile")
def Profile():
    if 'email' in session:
        email = session['email']
        result = Display_All(email)
        return render_template("profile.html", result = result)
    else:
        return redirect(url_for('Login')) 

@app.route("/SIGNIN", methods=["GET", "POST"])
def SIGNIN():
    if request.method == "POST":
        First_Name = request.form.get("First_Name")
        Last_Name = request.form.get("Last_Name")
        UserName = request.form.get("UserName")
        Email = request.form.get("Email")
        Password = request.form.get("Password")
        Gender = request.form.get("Gender")
        Phone_number = request.form.get("Phone_number")
        
        result = Signin_Data(First_Name, Last_Name, UserName, Email, Password, Gender, Phone_number)
        print(UserName, Email, Password)
        return redirect(url_for('LOGIN'))
    else:
        return render_template("signin.html")


@app.route("/LOGIN", methods=["GET", "POST"])
def LOGIN():
    if request.method == "POST":
        Email = request.form.get("Email")
        Password = request.form.get("Password")

        print(Email, Password)

        login_result = Login_Data(Email, Password)

        if login_result == "Login successful!":
            session['email'] = Email 
            flash("Log in successfully~")
            return redirect(url_for("user_products"))
        elif login_result == "Admin":
            session['email'] = Email 
            results = Display_All(Email) 
            return redirect(url_for("Dashboard")) 
        else:
            flash("Invalid email or password.", "warning")
            return render_template("signin.html", error="Invalid email or password.")
    else:
        return render_template("signin.html")



@app.route("/logout")
def Logout():
    session.clear()  
    return redirect(url_for('Login'))


@app.route("/tables")
def Tables():
    if 'email' in session:
        result = Display_All(session['email'])
        return render_template("tables.html", username=session['email'], result=result)
    else:
        return redirect(url_for('Login')) 


@app.route("/save_contact")
def Save_contact():
    if 'email' in session:
        result = Display_All(session['email'])
        return render_template("charts.html", username=session['username'], result=result)
    else:
        return redirect(url_for('Login')) 


@app.route("/user_products")
def user_products():
    if 'email' in session:
        products = Products()
        email = session['email']
        result = Display_All(email)
        return render_template("shop.html", products=products, result = result)
    else:
        return redirect(url_for("Login"))
        

@app.route("/add_to_cart", methods = ['POST', 'GET'])
def add_to_cart():
    try:
        product_id = request.form.get("product_id")

        if not product_id:
            return jsonify({"error": "Missing product_id"}), 400

        try:
            product_id = int(product_id)
        except ValueError:
            return jsonify({"error": "Invalid product_id"}), 400

        user_data = Get_userid(session.get('email'))
        if not user_data:
            return jsonify({"error": "User not found"}), 401

        user_id = user_data['Cust_ID']

        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Cart (user_id, product_id, quantity) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + 1;
            """,
            (user_id, product_id, 1)
        )

        conn.commit()
        cursor.close()
        conn.close()
        flash("Product added to cart",category="success")
        return redirect(url_for("Cart"))

    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/checkout", methods = ['POST', 'GET'])
def checkout():
    if 'email' in session:
        return render_template("checkout.html")
    else:
        return redirect(url_for("LOGIN"))




if __name__ == "__main__":
    app.run(debug = True)