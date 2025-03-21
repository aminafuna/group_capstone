from connections.functions import *
import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ecommerce"
    )


def Signin_Data(First_Name, Last_Name, UserName, Email, Password, Gender, Phone_number):
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Users (First_Name, Last_Name, UserName, Email, Password, Gender, Phone_number) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
            (First_Name, Last_Name, UserName, Email, Password, Gender, Phone_number))
        
        conn.commit()
        return "User signed up successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def Login_Data(Email, Password):
    conn = db_connection()
    cursor = conn.cursor(buffered=True)
    
    try:
        cursor.execute("""
            SELECT Email, Password 
            FROM Users 
            WHERE Email = %s AND Password = %s
            """, (Email, Password))
        user = cursor.fetchone()
        
        if user:
            return "Login successful!"
        else:
            return "Invalid username or password."
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def Display_All(email):
    conn = db_connection()
    cursor = conn.cursor(buffered=True)

    try:
        cursor.execute("""
            SELECT First_Name, Last_Name, Email, Phone_number 
            FROM Users 
            WHERE Email = %s
            """, (email,))
        user = cursor.fetchone() 

        if user:
            return list(user)
        else:
            return []
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def Products():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, description, price, stock, picture FROM products")
        products = cursor.fetchall()
    
        for product in products:
            product["price"] = float(product["price"]) 
    
        return products

    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        cursor.close()
        conn.close()

def Get_userid(EmailSession):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        
        query = """
        SELECT Cust_ID from Users WHERE email = %s
        """
        cursor.execute(query, (EmailSession,))
        userid = cursor.fetchone()
        return userid
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        cursor.close()
        conn.close()

def Get_cart(user_id):
    conn = db_connection()
    cursor = conn.cursor()

    query = """
        SELECT p.Product_Name, p.picture, p.price, c.quantity, (p.price * c.quantity) AS total, p.Product_ID AS id
        FROM Cart c
        JOIN Products p ON c.product_id = p.Product_ID
        WHERE c.user_id = %s
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result 



def add_to_cart(user_id, product_id, quantity):
    conn = db_connection()
    cursor = conn.cursor()

    print("User ID:", user_id, "Product ID:", product_id, "Quantity:", quantity)   

    try:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
            (user_id, product_id, quantity)  
        )
        conn.commit()
        return {"success": True, "message": "Product added to cart"}
    except Exception as e:
        print("Database Error:", e)   
        return {"success": False, "message": str(e)}
    finally:
        cursor.close()
        conn.close()

def remove_from_cart(item_id):
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cart WHERE product_id = %s", (item_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            return {"success": True, "message": "Item removed from cart"}
        else:
            return {"success": False, "message": "Item not found"}
    except mysql.connector.Error as err:
        return {"success": False, "message": str(err)}
    finally:
        cursor.close()
        conn.close()

