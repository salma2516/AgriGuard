from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from tensorflow.keras.models import load_model
from utils.whatsapp_service import send_whatsapp
from utils.weather_service import get_weather
from utils.translator_service import translate_text
from flask import jsonify

import numpy as np
import cv2
import os

import mysql.connector
# ==========================
# FLASK APP
# ==========================

app = Flask(__name__)

os.makedirs(
    "uploads",
    exist_ok=True
)

app.secret_key = "AGRIGUARD_SECRET_KEY"

model = load_model(
    "model/crop_model.h5"
)

# Disease Classes
classes = [

    "Pepper_Bacterial_Spot",
    "Pepper_Healthy",

    "Potato_Early_Blight",
    "Potato_Healthy",
    "Potato_Late_Blight",

    "Tomato_Bacterial_Spot",
    "Tomato_Early_Blight",
    "Tomato_Healthy",
    "Tomato_Late_Blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_Leaf_Spot",
    "Tomato_Spider_Mites",
    "Tomato_Target_Spot",
    "Tomato_Mosaic_Virus",
    "Tomato_Yellow_Leaf_Curl_Virus"
]


#Recommendation
recommendations = {

    "Pepper_Bacterial_Spot":
    "Apply copper spray treatment.",

    "Pepper_Healthy":
    "Crop is healthy. Continue normal cultivation.",

    "Potato_Early_Blight":
    "Apply fungicide and balanced NPK fertilizer.",

    "Potato_Healthy":
    "Crop is healthy. Continue normal cultivation.",

    "Potato_Late_Blight":
    "Apply protective fungicide.",

    "Tomato_Bacterial_Spot":
    "Apply copper-based spray treatment.",

    "Tomato_Early_Blight":
    "Apply Copper Fungicide and NPK fertilizer.",

    "Tomato_Healthy":
    "Crop is healthy. Continue regular watering and fertilization.",

    "Tomato_Late_Blight":
    "Apply Mancozeb fungicide and improve drainage.",

    "Tomato_Leaf_Mold":
    "Apply fungicide and improve ventilation.",

    "Tomato_Septoria_Leaf_Spot":
    "Apply Chlorothalonil fungicide.",

    "Tomato_Spider_Mites":
    "Use insecticide and maintain humidity.",

    "Tomato_Target_Spot":
    "Apply fungicide and remove infected leaves.",

    "Tomato_Mosaic_Virus":
    "Remove infected plants immediately.",

    "Tomato_Yellow_Leaf_Curl_Virus":
    "Control whiteflies and remove infected plants."
}



# ==========================
# MYSQL CONNECTION
# ==========================

def get_db():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_DATABASE_PASSWORD",
        database="agriguard"
    )

    return conn

# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    return redirect(
        url_for("login")
    )

# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        farmer_name = request.form.get("farmer_name")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        language = request.form.get("language")
        country = request.form.get("country")

        try:

            conn = get_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id
                FROM farmers
                WHERE phone_number=%s
                """,
                (phone_number,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                return render_template(
                    "register.html",
                    error="Phone Number Already Registered"
                )

            cursor.execute(
                """
                INSERT INTO farmers
                (
                    farmer_name,
                    phone_number,
                    password,
                    language,
                    country
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    farmer_name,
                    phone_number,
                    password,
                    language,
                    country
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            return redirect(
                url_for("login")
            )

        except Exception as e:

            return render_template(
                "register.html",
                error=str(e)
            )

    return render_template(
        "register.html"
    )

# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        phone_number = request.form.get(
            "phone_number"
        )

        password = request.form.get(
            "password"
        )

        conn = get_db()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM farmers
            WHERE phone_number=%s
            AND password=%s
            """,
            (
                phone_number,
                password
            )
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            session["farmer_id"] = user["id"]

            session["farmer_name"] = user[
                "farmer_name"
            ]

            session["phone_number"] = user[
                "phone_number"
            ]

            session["language"] = user[
                "language"
            ]

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "login.html",
            error="Invalid Phone Number or Password"
        )

    return render_template(
        "login.html"
    )

# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "farmer_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM predictions
        WHERE farmer_id=%s
        ORDER BY prediction_date DESC
        """,
        (
            session["farmer_id"],
        )
    )

    predictions = cursor.fetchall()

    cursor.close()
    conn.close()

    language = session["language"]

    texts = {

    "welcome":
    translate_text(
        "Welcome",
        language
    ),

    "weather":
    translate_text(
        "Weather",
        language
    ),

    "history":
    translate_text(
        "History",
        language
    ),

    "profile":
    translate_text(
        "Profile",
        language
    ),

    "logout":
    translate_text(
        "Logout",
        language
    ),

    "crop_detection":
    translate_text(
        "Crop Disease Detection",
        language
    ),

    "ai_assistant":
    translate_text(
        "AgriGuard AI Assistant",
        language
    )

}

    return render_template(

        "dashboard.html",

        farmer_name=session[
            "farmer_name"
        ],

        predictions=predictions,

        texts=texts

    )

# ==========================
# PROFILE
# ==========================

@app.route("/profile")
def profile():

    if "farmer_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "profile.html",
        farmer_name=session[
            "farmer_name"
        ],
        phone_number=session[
            "phone_number"
        ],
        language=session[
            "language"
        ]
    )

# ==========================
# HISTORY
# ==========================

@app.route("/history")
def history():

    if "farmer_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM predictions
        WHERE farmer_id=%s
        ORDER BY prediction_date DESC
        """,
        (
            session["farmer_id"],
        )
    )

    history_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        history_data=history_data
    )

# ==========================
# WEATHER
# ==========================

@app.route("/weather")
def weather():

    if "farmer_id" not in session:

        return redirect(
            url_for("login")
        )

    city = "Bangalore"

    weather_data = get_weather(city)

    return render_template(
        "weather.html",
        weather=weather_data
    )

# ==========================
# PREDICT
# ==========================
@app.route("/predict", methods=["POST"])
def predict():

    if "farmer_id" not in session:

        return redirect(
            url_for("login")
        )

    if "image" not in request.files:

        return redirect(
            url_for("dashboard")
        )

    file = request.files["image"]

    if file.filename == "":

        return redirect(
            url_for("dashboard")
        )

    filepath = os.path.join(
        "uploads",
        file.filename
    )

    file.save(filepath)

    img = cv2.imread(filepath)

    if img is None:

        return render_template(
            "dashboard.html",
            farmer_name=session["farmer_name"],
            predictions=[],
            error="Invalid Image File"
        )

    img = cv2.resize(
        img,
        (128, 128)
    )

    img = img.astype(
        "float32"
    ) / 255.0

    img = np.expand_dims(
        img,
        axis=0
    )

    prediction = model.predict(
        img,
        verbose=0
    )

    class_index = np.argmax(
        prediction
    )

    if class_index >= len(classes):

        disease = "Unknown Disease"

    else:

        disease = classes[
            class_index
        ]

    confidence = round(
        float(np.max(prediction)) * 100,
        2
    )

    fertilizer = recommendations.get(
        disease,
        "Consult Agricultural Expert"
    )

    if "Healthy" in disease:

        water_status = (
            "Normal Irrigation Required"
        )

        health_score = 100

    else:

        water_status = (
            "Moderate Irrigation Recommended"
        )

        health_score = round(
            confidence
        )

    farmer_message = f"""
🌱 AGRIGUARD FARM ALERT

Disease:
{disease}

Confidence:
{confidence}%

Health Score:
{health_score}%

Recommendation:
{fertilizer}

Water Requirement:
{water_status}

Thank you for using AgriGuard.
"""

    # ==========================
    # SAVE TO MYSQL
    # ==========================

    try:

        conn = get_db()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (
                farmer_id,
                disease,
                confidence,
                health_score,
                fertilizer,
                water_status
            )
            VALUES
            (%s,%s,%s,%s,%s,%s)
            """,
            (
                session["farmer_id"],
                disease,
                confidence,
                health_score,
                fertilizer,
                water_status
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:

        print(
            "Database Error:",
            e
        )

    # ==========================
    # SEND WHATSAPP
    # ==========================

    try:

        send_whatsapp(
            session["phone_number"],
            farmer_message
        )

    except Exception as e:

        print(
            "WhatsApp Error:",
            e
        )

    # ==========================
    # SHOW RESULT
    # ==========================

    return render_template(
        "result.html",
        disease=disease,
        confidence=confidence,
        fertilizer=fertilizer,
        water_status=water_status,
        health_score=health_score,
        farmer_message=farmer_message
    )

# ==========================
# VOICE ASSISTANT
# ==========================

@app.route(
    "/voice_assistant",
    methods=["POST"]
)
def voice_assistant():

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).lower()

    if "fertilizer" in question:

        answer = (
            "Use balanced NPK fertilizer for healthy crop growth."
        )

    elif "water" in question:

        answer = (
            "Water crops early in the morning and avoid over irrigation."
        )

    elif "weather" in question:

        answer = (
            "Check the weather page for temperature humidity and rainfall information."
        )

    elif "disease" in question:

        answer = (
            "Upload a crop image and I will detect the disease."
        )

    elif "tomato" in question:

        answer = (
            "Tomato crops require regular watering and disease monitoring."
        )

    elif "potato" in question:

        answer = (
            "Potato crops need well drained soil and balanced fertilization."
        )

    else:

        answer = (
            "Please ask about crops, fertilizer, irrigation, weather or plant diseases."
        )

    return jsonify(
        {
            "answer": answer
        }
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )