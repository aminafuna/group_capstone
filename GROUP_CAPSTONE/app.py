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
        cart_items = Get_cart(user_id)
        email = session['email']
        result = Display_All(email)
        return render_template("cart.html", cart_items=cart_items, result = result)
    else:
        return redirect(url_for("Login"))

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
            return redirect(url_for("user_products"))
        elif login_result == "Admin":
            session['email'] = Email 
            results = Display_All(Email) 
            return redirect(url_for("Dashboard")) 
        else:
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
        



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        user_data = Get_userid(session['email'])
        user_id = user_data['id']
        product_id = int(data.get("product_id"))
        quantity = int(data.get("quantity", 1))

        if not isinstance(product_id, int) or not isinstance(quantity, int):
            return jsonify({"error": "product_id and quantity must be integers"}), 400

        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
            (user_id, product_id, quantity)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Product added to cart"}), 200

    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug = True)
    