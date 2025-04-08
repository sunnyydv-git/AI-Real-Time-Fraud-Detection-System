# 🚨 Real-Time AI Fraud Detection System
![Status](https://img.shields.io/badge/status-deployed-brightgreen)  
![License](https://img.shields.io/badge/license-MIT-blue)  
![Python](https://img.shields.io/badge/python-3.9+-blue)


A scalable, end-to-end real-time fraud detection pipeline powered by **Apache Kafka**, **Apache Spark Streaming**, **Azure PostgreSQL**, **Azure Data Factory**, and **Azure ML Studio**. This project detects fraudulent transactions in real-time and stores the predictions back into a cloud-based database for immediate action.

---

## 📌 Table of Contents

- [⚙️ Architecture](#️-architecture)  
- [🧠 ML Model](#-ml-model)  
- [🚀 Pipeline Flow](#-pipeline-flow)  
- [🛠️ Tech Stack](#️-tech-stack)  
- [📁 Project Structure](#-project-structure)  
- [📦 Setup & Run](#-setup--run)  
- [📡 REST API for Prediction](#-rest-api-for-prediction)  
- [📊 Results & Insights](#-results--insights)  
- [📎 Related Links](#-related-links)  

---

## ⚙️ Architecture

- A[Kafka Producer] --> B[Kafka Topic: fraud_data]  
- B --> C[Spark Structured Streaming]  
- C --> D[Azure PostgreSQL]  
- D --> E[Azure Data Factory ETL]  
- E --> F[Azure ML REST Endpoint]  
- F --> G[Predicted Fraud Stored in PostgreSQL]  

---

## 🧠 ML Model

- Algorithm: **Random Forest Classifier**    
- Trained in Azure ML Studio Notebooks  
- Real-time predictions via Azure ML REST Endpoint  
- Model endpoint: **fraud_detection_rf_model:1**    

---

## 🚀 Pipeline Flow

- 🧾 **Transaction data** is pushed to **Kafka topic**  
- 🔥 **Spark Streaming** consumes and writes to **Azure PostgreSQL**  
- 🧬 **Azure Data Factory** performs ETL on stored stream data  
- 🧠 Cleaned data is sent to **Azure ML endpoint**  
- ✅ **Fraud prediction** returned and stored in PostgreSQL (fraudpredictions table)  

---

## 🛠️ Tech Stack

- **Python** (Pandas, PySpark, Scikit-learn, Numpy)  
- **Apache Kafka** (KRaft Mode)  
- **Apache Spark** Structured Streaming  
- **Azure PostgreSQL**  
- **Azure Data Factory**  
- **Azure ML Studio (Notebook + Endpoint)**    
- **Docker** (for Kafka setup)  
- **VS Code** (for development)  

---

## 📁 Project Structure

AI-Real-Time-Fraud-Detection-System/  
├── notebooks/  
│   └── fraud_detection_system.ipynb  
├── data/  
│   └── frauds_data.csv  
├── kafka/  
│   └── producer.py  
│   └── consumer_spark.py  
├── etl/  
│   └── etl_pipeline_adf.png  
├── model/  
│   └── fraud_detection_rf_model.pkl  
├── api/  
│   └── call_endpoint.py  
├── README.md  
└── .gitignore  

---

## 📡 REST API for Prediction

- **ENDPOINT URL :** http://343ae727-f835-45f0-a8e3-16e6f2bb1a08.centralindia.azurecontainer.io/score
- **Sample Payload :** {  
  "transaction_id": "T123",  
  "user_id": "U456",  
  "amount": 10500,  
  "transaction_type": "international",  
  "status": "success",  
  "device_id": "dev001",  
  "ip_address": "192.168.1.5",  
  "is_foreign_transaction": true,  
  "num_chargebacks": 2  
}  

---

## 📊 Results & Insights

-  ✅ Accuracy: ~94%  
- 🕒 Real-time fraud prediction within milliseconds  
- 🔄 Continuous streaming and learning pipeline  
- 📈 Scalable and production-ready architecture  

---

## 📎 Related Links

- Kafka Setup in Docker  
- Spark Consumer Script  
- Azure ML Notebook  
- ADF ETL Flow  

---
