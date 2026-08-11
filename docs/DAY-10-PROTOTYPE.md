# Day 10 — AI Receipt Scanner Working Prototype

## 1. Objective

The objective of Day 10 is to move the AI Receipt Scanner from a basic proof-of-concept toward a working prototype.

The prototype accepts a receipt image, performs OCR using EasyOCR, extracts useful information from the receipt, and returns the processed information through a FastAPI endpoint.

---

## 2. Selected AI Feature

### AI Receipt Scanner & Smart Expense Processing

The selected feature allows users to upload a receipt image and automatically extract financial information that can later be used to create an expense record in HisabDo.

---

## 3. Input

The prototype accepts:

- Receipt image
- Supported image formats such as JPG and PNG

### Sample Input

```text
recpit.jpg