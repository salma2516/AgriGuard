import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password"="YOUR_DATABASE_PASSWORD",
    "database": "agriguard"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def create_database():

    try:

        # Connect without database first
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_DATABASE_PASSWORD"
        )

        cursor = conn.cursor()

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS agriguard"
        )

        print("Database Created Successfully")

        cursor.close()
        conn.close()

    except Exception as e:

        print("Database Error")
        print(e)


def create_tables():

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # Farmers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers(

            id INT AUTO_INCREMENT PRIMARY KEY,

            farmer_name VARCHAR(100),

            phone_number VARCHAR(20) UNIQUE,

            password VARCHAR(255),

            language VARCHAR(50),

            country VARCHAR(100),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Predictions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(

            id INT AUTO_INCREMENT PRIMARY KEY,

            farmer_id INT,

            disease VARCHAR(255),

            confidence FLOAT,

            health_score INT,

            fertilizer TEXT,

            water_status TEXT,

            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (farmer_id)
            REFERENCES farmers(id)
            ON DELETE CASCADE
        )
        """)

        # Notifications Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications(

            id INT AUTO_INCREMENT PRIMARY KEY,

            farmer_id INT,

            message TEXT,

            notification_type VARCHAR(50),

            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (farmer_id)
            REFERENCES farmers(id)
            ON DELETE CASCADE
        )
        """)

        conn.commit()

        print("All Tables Created Successfully")

        cursor.close()
        conn.close()

    except Exception as e:

        print("Table Creation Error")
        print(e)


def test_connection():

    try:

        conn = get_connection()

        print("MySQL Connected Successfully")

        conn.close()

    except Exception as e:

        print("Connection Failed")
        print(e)


if __name__ == "__main__":

    create_database()

    test_connection()

    create_tables()
