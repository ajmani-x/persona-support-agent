# Persona-Adaptive Customer Support Agent
Overview

This project implements a Persona-Adaptive AI Customer Support Agent designed to intelligently handle customer queries by:

Detecting customer persona

Extracting structured issue metadata

Retrieving relevant knowledge base content

Adapting response tone dynamically

Escalating to a human agent when necessary

The system demonstrates modular LLM orchestration, structured outputs, tone control, and escalation decision logic.

## 🎯 Key Features
1️⃣ Persona Detection

Classifies customers into one of the following categories:

Technical Expert

Frustrated User

Business Executive

Other

This classification influences tone, structure, and response style.

2️⃣ Structured Metadata Extraction

The system extracts:

Product Area

Urgency Level (low / medium / high)

Account ID (if mentioned)

Issue Summary

Sentiment (calm / frustrated / angry)

Customer Type

Escalation Requirement

Structured outputs ensure reliability and production readiness.

3️⃣ Knowledge Base Retrieval

A rule-based knowledge base retrieves relevant support information using keyword matching.

Example domains:

Refunds

Billing

API usage

Pricing

Login issues

The architecture is modular and can be extended to embedding-based RAG for semantic retrieval.

4️⃣ Persona-Based Tone Adaptation

Response style dynamically adapts:

Technical Expert → Detailed and precise

Frustrated User → Empathetic and calming

Business Executive → Concise and outcome-focused

Other → Professional and helpful

5️⃣ Escalation Logic

Escalation is triggered if:

Model predicts human intervention required

Sentiment is “angry”

High-risk keywords are detected (e.g., cancel, complaint)

When escalation is triggered, the response clearly indicates human specialist handoff.

## 🏗 System Architecture

User Input
↓
Persona Classification (Structured Output)
↓
Issue Metadata Extraction
↓
Knowledge Retrieval Layer
↓
Escalation Decision Logic
↓
Persona-Adaptive Response Generation

🛠 Tech Stack

Python

LangChain

Cohere LLM (command-a-03-2025)

Pydantic (Structured Output Validation)

🚀 How to Run

Install dependencies

Add your Cohere API key to a .env file

Run the script

python main.py

Type queries in the console.
Type quit to exit.

## 📈 Extensibility

This implementation is intentionally modular and can be extended to:

Vector database integration (FAISS / Chroma)

Embedding-based semantic retrieval (RAG)

Confidence scoring layer

Streamlit or web-based UI

Logging & analytics integration

CRM system handoff integration

🧠 Design Philosophy

The system prioritizes:

Structured outputs over free-form text

Modular architecture

Clear separation of classification, retrieval, and generation

Business-aware escalation handling

Production-ready decision layering

## 🎯 Relevance to AI Product Systems

This architecture aligns with real-world AI-driven automation platforms by demonstrating:

LLM orchestration

Controlled generation

Structured extraction

Decision-based escalation

Scalable system design

## Author
Aryan Ajmani