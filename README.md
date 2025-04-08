# 🚨 Real-Time AI Fraud Detection System

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

- Algorithm: **Random Forest Classifier  **  
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

