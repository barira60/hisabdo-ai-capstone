# 🚀 HisabDo AI/ML Capstone Project

## AI-Powered Financial Management

This project is the main AI/ML Capstone Project for the HisabDo Internship Program.

The objective is to analyze the existing HisabDo financial management application and identify practical opportunities where Artificial Intelligence and Machine Learning can improve the user experience.

The project will progressively move from research and planning to AI/ML implementation, API development, integration, testing, and deployment throughout the internship.

## 🔗 Existing Application

- Website: [https://hisabdo.app/](https://hisabdo.app/)
- Mobile Application: [https://play.google.com/store/apps/details?id=com.usman.hisabdo](https://play.google.com/store/apps/details?id=com.usman.hisabdo)

## 🎯 Project Objective

The main objective is to explore how AI and ML can improve:

- Financial record management
- Expense tracking
- Customer management
- Financial analytics
- Reports
- Voice-based interaction
- Budget planning
- Financial decision-making

The project focuses on enhancing existing HisabDo functionality rather than creating an unrelated standalone AI application.

## 🔍 Product Analysis

The existing HisabDo application provides functionality related to:

- Khata / Ledger
- Customer management
- Transactions
- Expenses
- Dashboard
- Analytics
- Reports and PDF export
- Voice entry
- Backup and restore
- Multi-language support
- Multi-currency support
- Built-in calculator

The analysis identified several opportunities for adding an AI intelligence layer to these existing features.

## 🤖 Proposed AI/ML Use Cases

1. AI Receipt Scanner & OCR
2. Smart Expense Categorization
3. AI Financial Assistant
4. AI Financial Insights
5. Smart Budget Recommendations
6. Predictive Expense Analytics
7. Smart Payment Reminders

## ⭐ Top 2 AI Features

### 1. AI Receipt Scanner & Smart Expense Processing

The system will allow users to capture a receipt and automatically extract:

- Merchant
- Date
- Amount
- Items
- Expense category

Possible technologies:

- OCR
- Computer Vision
- NLP
- Machine Learning

### 2. AI Financial Assistant

The AI assistant will allow users to ask questions about their financial information using natural language.

Examples:

- "How much did I spend this month?"
- "Who owes me the most money?"
- "What was my biggest expense?"
- "How much did I spend on transport?"

Possible technologies:

- LLM
- NLP
- Structured data retrieval
- RAG where appropriate
- Python/FastAPI backend

## 🏗️ Top 2 Architecture

### AI Receipt Scanner

```text
User
  ↓
HisabDo Mobile Application
  ↓
Receipt Image
  ↓
AI/OCR Service
  ↓
OCR Model
  ↓
Information Extraction
  ↓
Expense Categorization
  ↓
User Confirmation
  ↓
HisabDo Expense Record
````

### AI Financial Assistant

```text
User
  ↓
HisabDo Web/Mobile Application
  ↓
AI Assistant API
  ↓
Financial Data
  ↓
LLM / AI Model
  ↓
Response Generation
  ↓
AI Response
  ↓
User
```

## 🚀 Day 9 — AI Receipt Scanner POC

The primary AI feature selected for implementation is:

**AI Receipt Scanner & Smart Expense Processing**

A working proof-of-concept was developed using **FastAPI and EasyOCR**.

### 🔄 POC Workflow

```text
Receipt Image
      ↓
FastAPI Upload
      ↓
EasyOCR
      ↓
Text Extraction
      ↓
Total Amount Extraction
      ↓
Expense Categorization
      ↓
JSON Response
```

### 🛠️ Technology Used

* Python
* FastAPI
* EasyOCR
* Regular Expressions
* Rule-based Expense Categorization
* Swagger UI

### 📥 Input

The API accepts a receipt image through:

```text
POST /scan-receipt
```

### 📤 Output

The API returns:

* Filename
* Extracted receipt text
* Total amount
* Expense category

Example:

```json
{
  "filename": "recpit.jpg",
  "amount": 84.8,
  "category": "Other"
}
```

### 🧪 POC Test Result

The receipt scanner was successfully tested using FastAPI Swagger UI.

The system successfully:

* Accepted the receipt image
* Extracted text using EasyOCR
* Identified the total amount as `84.8`
* Generated an expense category

### 📸 POC Screenshot

The following screenshot shows the successful testing of the AI Receipt Scanner API using FastAPI Swagger UI.

![AI Receipt Scanner POC](./screenshots/receipt-scanner-result.png)

### 🔮 Integration Plan

The POC can later be integrated into:

* **Website:** Receipt upload interface connected to the AI API
* **Web Application:** Expense entry form with automatic receipt processing
* **Mobile Application:** Camera-based receipt capture connected to the backend API

> This is currently a proof-of-concept. Advanced ML categorization, improved information extraction, application integration, testing, and deployment will be developed in later stages.

## 👥 User Feedback

Five users were asked to explore the HisabDo application and provide feedback about usability, useful features, difficult workflows, and potential AI improvements.

The detailed results are documented in `docs/USER-FEEDBACK.md`.

## 📂 Repository Structure

```text
hisabdo-ai-capstone/
│
├── README.md
│
├── docs/
│   ├── AI-USE-CASE-DOCUMENT.md
│   ├── FEATURE-ANALYSIS.md
│   ├── USER-FEEDBACK.md
│   ├── ARCHITECTURE.md
│   └── DAY-9-FEATURE-SPECIFICATION.md
│
├── poc/
│   └── receipt-scanner/
│       ├── app.py
│       ├── requirements.txt
│       └── README.md
│
└── screenshots/
    └── receipt-scanner-result.png
```

## 🚧 Project Status

### Day 8 — Research & Planning

* [x] HisabDo website research
* [x] HisabDo mobile application research
* [x] Existing feature analysis
* [x] AI/ML opportunity identification
* [x] AI use cases identified
* [x] Top 2 features selected
* [x] Initial technical architecture prepared
* [x] Five-user feedback collected

### Day 9 — AI Feature Implementation

* [x] Primary AI feature selected
* [x] Feature workflow defined
* [x] Input and output identified
* [x] AI/OCR technology researched
* [x] Architecture defined
* [x] AI prototype developed
* [x] FastAPI backend/API developed
* [x] EasyOCR integrated
* [x] Receipt image tested
* [x] Total amount extraction implemented
* [x] Expense categorization implemented
* [x] API tested using Swagger UI
* [x] POC screenshot captured
* [x] Website/Web/Mobile integration plan defined
* [ ] Production application integration
* [ ] Advanced ML-based categorization
* [ ] Testing and evaluation
* [ ] Deployment

## 🔮 Future Development

The project will continue throughout the internship from Day 8 to Day 60.

Future stages will include:

1. Data collection
2. Data preprocessing
3. AI/ML model development
4. OCR improvement
5. Expense classification
6. Financial assistant development
7. API development
8. Application integration
9. Testing and evaluation
10. Deployment
11. Final documentation

## 📌 Conclusion

The research indicates that HisabDo already provides a strong financial-management foundation.

The proposed AI features aim to enhance existing workflows through:

* Automation
* Natural-language interaction
* Intelligent categorization
* Personalized insights
* Prediction
* Recommendation

The selected Top 2 features are:

1. AI Receipt Scanner & Smart Expense Processing
2. AI Financial Assistant

The Day 9 proof-of-concept demonstrates the initial implementation of the AI Receipt Scanner using FastAPI and EasyOCR.

The project will continue to evolve through the remaining internship stages with improved AI models, application integration, testing, and deployment.

```
```
