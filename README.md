Voice-enabled Property Price Assistant (Lucknow)

Author
Aryan Yadav
B.Tech Student

Overview
This project is a backend system that works as a voice-enabled property price assistant for Lucknow. The goal is to allow users to ask natural Hinglish queries like “gomti nagar me shop rate kya hai” and get accurate, structured responses based strictly on a predefined dataset.

The system is not a general chatbot. It is a controlled AI system that combines retrieval (FAISS), memory (MongoDB), and an LLM (DeepSeek) only for formatting responses. The main focus is correctness, not creativity.

The assistant name is “Aryan” and it responds in a polite, human-like Hinglish style.

Problem Statement
People often struggle to find correct property rates for specific local areas. Most sources are either outdated, static, or unreliable. There is no conversational system that understands local Hinglish queries and provides structured answers.

This project solves that problem by building a backend that can:

* Understand natural queries
* Retrieve correct data from a trusted dataset
* Maintain conversation context
* Respond in a simple human-like way

Key Features
The system supports Hinglish queries and can handle real conversational flow. It does not depend on LLM hallucination and always uses data as the source of truth.

Main capabilities include:

* Hinglish query support
  Example: gomti nagar me shop rate kya hai

* Context understanding
  Example:
  User: gomti nagar rate
  User: uska office rate kya hai

* FAISS-based retrieval
  Fast and relevant search over dataset

* MongoDB chat memory
  Last 5 conversations are stored and reused

* Intent detection
  greeting, help, memory, exit, property query

* Strict RAG pipeline
  LLM cannot generate fake data

* S3-based dataset loading
  PDF is fetched from cloud dynamically

System Architecture

User Query
→ FastAPI endpoint
→ Intent Detection
→ MongoDB Memory Fetch
→ FAISS Retrieval
→ LLM Formatting (DeepSeek via NVIDIA API)
→ Response
→ Save to MongoDB

Tech Stack

Backend
FastAPI

Database
MongoDB

Vector Database
FAISS

Embeddings
Sentence Transformers (all-MiniLM-L6-v2)

LLM
DeepSeek via NVIDIA API

Cloud Storage
AWS S3

Libraries
LangChain (community modules), boto3, pypdf

Dataset

The system uses a PDF file stored in S3.
This PDF contains circle rate data for different locations.

Data includes:

* location
* shop rate
* office rate
* warehouse rate
* road width rates
* agricultural rates

The dataset acts as the only source of truth.
No external or generated data is used.

How the System Works

1. User sends query (Hinglish or English)
2. Intent is detected using rule-based logic
3. Last 5 chats are fetched from MongoDB
4. Query is passed to FAISS retriever
5. Relevant chunks are selected
6. LLM formats the answer using strict prompt
7. Response is returned
8. Chat is saved in MongoDB

Intent Detection

The system uses simple keyword matching.

Supported intents:

* Greeting
* Help
* Memory
* Exit
* Property Query (default)

This avoids unnecessary LLM usage and keeps system fast.

Memory System

Chat history is stored per user_id.

Each record includes:

* query
* response
* timestamp

Last 5 chats are used as context for follow-up queries.

Example:

User: gomti nagar rate
User: uska office rate kya hai

System understands “uska” using memory.

RAG Design

This system uses strict Retrieval-Augmented Generation.

Important rules:

* LLM cannot invent data
* Only retrieved context is used
* If data not found → system clearly says “data available nahi hai”

This ensures reliability.

PDF → FAISS Pipeline

1. PDF is downloaded from S3
2. Text is extracted using PyPDFLoader
3. Text is split into chunks
4. Embeddings are created
5. FAISS index is built
6. Index is saved locally

On next run:

* FAISS is loaded directly (no rebuild)

S3 Integration

The dataset is stored in AWS S3.

Flow:

* Server starts
* Checks if FAISS exists
* If not → downloads PDF from S3
* Builds FAISS

This makes system cloud-ready and scalable.

Docker Setup

The project is containerized using Docker.

Flow:

* Build image
* Run container
* Pass .env file
* Service runs on port 8000

FAISS is built at runtime, not at build time.

API Endpoint

POST /chat

Request:

{
"user_id": "123",
"query": "gomti nagar me shop rate kya hai"
}

Response:

{
"response": "Aryan here. Gomti Nagar me shop rate ₹X per sqm hai..."
}

Design Principles

* Simple and readable code
* No unnecessary abstraction
* Production mindset
* Clear separation of services
* Controlled AI behavior
* No hallucination

Limitations

* Data limited to provided PDF
* No real-time updates
* Basic intent detection (rule-based)
* PDF parsing may introduce noise

Future Improvements

* Better entity extraction (location + property type)
* Redis caching for faster retrieval
* Speech-to-text and text-to-speech integration
* Multi-city support
* Frontend dashboard
* Real-time data integration

Deployment

The system can be deployed on:

* Render
* Railway
* AWS EC2

Environment variables must be configured for:

* MongoDB
* NVIDIA API
* AWS S3

Conclusion

This project is a production-style backend system that combines structured data, retrieval systems, and controlled AI to solve a real-world problem.

It is not just a chatbot but a reliable property intelligence assistant that focuses on correctness, simplicity, and practical deployment.

The system demonstrates how to build real-world AI applications without overcomplicating the architecture.
