# 🚀 Day 11 — Realistic Data & Input Validation

## 1. Day 11 Objective

The objective of Day 11 is to improve the **AI Receipt Scanner & Smart Expense Processing** prototype developed during Day 10.

The Day 10 prototype demonstrated the basic OCR workflow using FastAPI and EasyOCR.

For Day 11, the focus is on making the prototype more suitable for realistic application scenarios by:

- Defining a structured input format
- Preparing realistic sample inputs
- Processing application-style receipt data
- Validating AI/OCR responses
- Handling invalid or incomplete input
- Defining realistic use cases
- Planning communication between the application, backend, and AI service

---

## 2. Selected AI Feature

### AI Receipt Scanner & Smart Expense Processing

The selected feature allows users to upload a receipt image and automatically extract useful financial information.

The prototype processes the receipt using OCR and returns structured information that can later be used to create an expense record in HisabDo.

The main information includes:

- Receipt filename
- Extracted receipt text
- Total amount
- Expense category

---

## 3. Required Input Data Structure

The primary input to the receipt scanner is a receipt image.

### Input

```text
Receipt Image
````

Example:

```text
filename: grocery_receipt.jpg
type: image/jpeg
```

The application sends the image to the backend API using a multipart form-data request.

### API Endpoint

```text
POST /scan-receipt
```

### Example Request

```text
POST http://127.0.0.1:8000/scan-receipt
```

The uploaded image is then passed to the OCR service for processing.

---

## 4. Realistic Sample Data

To make the prototype closer to a real application, different types of receipts can be used as sample inputs.

### Use Case 1 — Grocery Receipt

```text
Filename:
grocery_receipt.jpg

Purpose:
Testing grocery-related expenses.
```

Expected information:

```text
Merchant
Date
Purchased items
Total amount
Expense category
```

Expected category:

```text
Groceries
```

---

### Use Case 2 — Restaurant Receipt

```text
Filename:
restaurant_receipt.jpg

Purpose:
Testing restaurant and food expenses.
```

Expected information:

```text
Restaurant name
Date
Food items
Total amount
Expense category
```

Expected category:

```text
Food
```

---

### Use Case 3 — General Store Receipt

```text
Filename:
store_receipt.jpg

Purpose:
Testing general shopping expenses.
```

Expected information:

```text
Store name
Date
Items
Total amount
Expense category
```

Expected category:

```text
Shopping
```

---

## 5. Existing Day 10 Sample

The receipt used during Day 10 is kept as part of the project because it demonstrates the original working POC.

Example:

```text
Filename:
recpit.jpg
```

The Day 10 prototype successfully processed this receipt.

Example result:

```json
{
  "filename": "recpit.jpg",
  "amount": 84.8,
  "category": "Other"
}
```

The Day 10 receipt remains available for comparison when testing improvements made during Day 11.

---

## 6. Application-Style Input

In a real HisabDo application, the receipt scanner would receive an image from the website or mobile application.

The application-style flow is:

```text
User
  ↓
Capture / Upload Receipt
  ↓
Receipt Image
  ↓
Backend API
  ↓
AI Receipt Scanner
```

The backend receives the image and sends it to the OCR processing component.

---

## 7. AI Processing

The prototype uses:

### FastAPI

FastAPI provides the backend API and handles receipt image uploads.

### EasyOCR

EasyOCR performs Optical Character Recognition and extracts text from the receipt image.

### Python

Python handles the processing and extraction logic.

### Processing Flow

```text
Receipt Image
      ↓
FastAPI
      ↓
EasyOCR
      ↓
Extracted Text
      ↓
Information Processing
      ↓
Amount Extraction
      ↓
Category Processing
      ↓
Structured JSON Response
```

---

## 8. Response Processing and Validation

The AI/OCR response should be checked before being returned to the application.

The system should validate:

* Whether OCR produced text
* Whether an amount was detected
* Whether the amount is a valid number
* Whether a category was returned
* Whether the uploaded file is a valid image

### Valid Response

Example:

```json
{
  "filename": "grocery_receipt.jpg",
  "amount": 1250.50,
  "category": "Groceries"
}
```

This response can be passed back to the HisabDo application.

---

## 9. Invalid and Incomplete Input Handling

A real application cannot assume that every uploaded file will be a valid receipt.

The system should handle invalid input safely.

### Invalid File Type

Example:

```text
Input:
document.pdf
```

Expected response:

```json
{
  "error": "Invalid file type. Please upload an image."
}
```

---

### Missing File

If the user does not provide a receipt image:

```json
{
  "error": "Receipt image is required."
}
```

---

### Unsupported Image

If the uploaded image cannot be processed:

```json
{
  "error": "Unable to process the receipt image."
}
```

---

### OCR Failure

If no readable text is detected:

```json
{
  "error": "No readable text was detected on the receipt."
}
```

---

### Amount Not Detected

If OCR succeeds but no valid total amount can be identified:

```json
{
  "filename": "receipt.jpg",
  "amount": null,
  "category": "Other",
  "message": "Receipt text was extracted, but the total amount could not be identified."
}
```

This allows the application to ask the user to enter or confirm the missing information.

---

## 10. Sample Output

A successful application-style response can look like:

```json
{
  "filename": "grocery_receipt.jpg",
  "amount": 1250.50,
  "category": "Groceries"
}
```

Another example:

```json
{
  "filename": "restaurant_receipt.jpg",
  "amount": 2450.00,
  "category": "Food"
}
```

Another example:

```json
{
  "filename": "store_receipt.jpg",
  "amount": 3200.00,
  "category": "Shopping"
}
```

These examples represent the type of structured information that the HisabDo application could use when creating an expense record.

---

## 11. Three Realistic Use Cases

### Use Case 1 — Grocery Expense

A user purchases groceries and receives a printed receipt.

The user uploads the receipt to HisabDo.

The AI system:

1. Reads the receipt
2. Extracts the text
3. Identifies the total amount
4. Determines the expense category
5. Returns the result
6. Allows the user to confirm the expense

Example:

```text
Receipt
  ↓
OCR
  ↓
Amount: 1250.50
  ↓
Category: Groceries
  ↓
User Confirmation
  ↓
Expense Record
```

---

### Use Case 2 — Restaurant Expense

A user has a meal at a restaurant.

The user captures a picture of the restaurant receipt.

The system extracts the receipt information and identifies the expense as a food-related expense.

Example:

```text
Receipt
  ↓
OCR
  ↓
Amount: 2450.00
  ↓
Category: Food
  ↓
User Confirmation
  ↓
Expense Record
```

---

### Use Case 3 — General Shopping Expense

A user purchases products from a general store.

The user uploads the receipt to HisabDo.

The system extracts the receipt information and assigns a shopping-related category.

Example:

```text
Receipt
  ↓
OCR
  ↓
Amount: 3200.00
  ↓
Category: Shopping
  ↓
User Confirmation
  ↓
Expense Record
```

---

## 12. Integration Architecture

The planned integration architecture is:

```text
HisabDo Application
        ↓
Backend / API
        ↓
AI Receipt Scanner Service
        ↓
EasyOCR
        ↓
Text Extraction
        ↓
Information Processing
        ↓
Validation
        ↓
Structured Response
        ↓
HisabDo Application
```

### Complete Application Flow

```text
User
  ↓
HisabDo Website / Mobile App
  ↓
Upload or Capture Receipt
  ↓
Backend API
  ↓
Receipt Scanner Service
  ↓
EasyOCR
  ↓
Extract Receipt Information
  ↓
Validate Response
  ↓
Return JSON
  ↓
User Confirmation
  ↓
HisabDo Expense Record
```

---

## 13. Required Technologies

### External AI API

The current prototype does not require an external cloud AI API.

OCR is performed locally using EasyOCR.

### ML Model

The current prototype uses the EasyOCR model for text recognition.

A dedicated machine-learning classification model can be added later for more accurate expense categorization.

### Database

The current POC does not require a database.

In the future, the extracted expense information can be stored in the HisabDo database.

### Prompt Engineering

Prompt engineering is not required for the current OCR-based prototype because the system is not using an LLM.

If an LLM-based financial assistant or advanced receipt information extraction system is added later, prompt engineering may be required.

### Python Service

Python is used as the backend service through FastAPI.

### Background Processing

For small receipt images, processing can occur directly through the API.

For large numbers of receipts or more computationally expensive AI processing, background processing can be introduced in a future version.

---

## 14. Day 11 Improvements

The Day 11 prototype focuses on making the Day 10 solution more realistic and application-ready.

The improvements include:

* Structured input definition
* Realistic receipt scenarios
* Application-style API input
* Response validation
* Invalid input handling
* OCR failure handling
* Missing amount handling
* Integration planning
* Realistic use-case documentation

---

## 15. Future Improvements

The current prototype can be improved further by adding:

* Better receipt image preprocessing
* Improved OCR accuracy
* Merchant extraction
* Date extraction
* Item extraction
* Tax extraction
* Automatic category classification
* Confidence scores
* Currency detection
* User confirmation interface
* Database integration
* Mobile camera integration
* Website integration

A machine-learning-based expense categorization model can also be developed using a suitable labeled expense dataset.

---

## 16. Day 11 Conclusion

The Day 11 work improves the AI Receipt Scanner prototype by moving beyond a basic OCR demonstration toward a more realistic application workflow.

The system now has a defined input structure, realistic sample scenarios, response validation requirements, invalid-input handling, and an integration architecture.

The prototype provides a foundation for connecting receipt scanning with the HisabDo financial-management workflow in future development stages.

### Current Technology Stack

```text
Python
FastAPI
EasyOCR
JSON
```

### Selected Feature

```text
AI Receipt Scanner & Smart Expense Processing
```

### Main Flow

```text
Application
    ↓
Backend API
    ↓
AI/OCR Service
    ↓
Response Validation
    ↓
Structured Financial Data
    ↓
Application
```
