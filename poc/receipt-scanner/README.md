# 🧾 HisabDo AI Receipt Scanner POC

This is the Day 9 Proof-of-Concept (POC) for the HisabDo AI/ML Capstone Project.

The POC demonstrates how a receipt image can be uploaded and processed automatically using OCR and basic expense processing.

## 🎯 Objective

The objective is to reduce manual expense entry by automatically extracting information from a receipt image.

The current POC extracts:

- Receipt text
- Total amount
- Expense category

## 🏗️ Workflow

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