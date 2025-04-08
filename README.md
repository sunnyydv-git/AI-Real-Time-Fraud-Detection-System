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

A[Kafka Producer] --> B[Kafka Topic: fraud_data]
B --> C[Spark Structured Streaming]
C --> D[Azure PostgreSQL]
D --> E[Azure Data Factory ETL]
E --> F[Azure ML REST Endpoint]
F --> G[Predicted Fraud Stored in PostgreSQL]
