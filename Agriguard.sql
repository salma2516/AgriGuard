CREATE DATABASE agriguard;

USE agriguard;

CREATE TABLE farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_name VARCHAR(100),
    phone_number VARCHAR(20) UNIQUE,
    password VARCHAR(255),
    language VARCHAR(20),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT,
    disease VARCHAR(100),
    confidence FLOAT,
    health_score INT,
    fertilizer TEXT,
    water_status TEXT,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id)
    REFERENCES farmers(id)
    ON DELETE CASCADE
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT,
    message TEXT,
    notification_type VARCHAR(20),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id)
    REFERENCES farmers(id)
    ON DELETE CASCADE
);
