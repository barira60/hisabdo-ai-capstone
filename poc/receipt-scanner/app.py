from fastapi import FastAPI, File, UploadFile
import easyocr
import re

app = FastAPI(
    title="HisabDo AI Receipt Scanner",
    description="Day 9 POC for AI-powered receipt scanning",
    version="1.0.0"
)

# Initialize EasyOCR
reader = easyocr.Reader(["en"], gpu=False)


def extract_amount(text):
    """Extract the total amount from receipt text."""

    lines = text.splitlines()

    # Look specifically for a line containing Total
    for i, line in enumerate(lines):
        if "total" in line.lower():
            # Check the same line
            match = re.search(r"\d+(?:[.,]\d{1,2})?", line)

            if match:
                return float(match.group().replace(",", ""))

            # Check the next line
            if i + 1 < len(lines):
                match = re.search(
                    r"\d+(?:[.,]\d{1,2})?",
                    lines[i + 1]
                )

                if match:
                    return float(match.group().replace(",", ""))

    return None

    values = []

    for amount in amounts:
        try:
            values.append(float(amount.replace(",", "")))
        except ValueError:
            pass

    if values:
        return max(values)

    return None


def categorize_expense(text):
    """Basic rule-based expense categorization."""

    text = text.lower()

    if any(word in text for word in [
        "milk",
        "bread",
        "grocery",
        "groceries",
        "vegetable",
        "supermarket"
    ]):
        return "Groceries"

    if any(word in text for word in [
        "restaurant",
        "pizza",
        "burger",
        "biryani",
        "food",
        "cafe",
        "coffee"
    ]):
        return "Food"

    if any(word in text for word in [
        "uber",
        "careem",
        "petrol",
        "fuel",
        "taxi",
        "transport"
    ]):
        return "Transport"

    if any(word in text for word in [
        "electricity",
        "internet",
        "water bill",
        "gas bill",
        "utility"
    ]):
        return "Bills"

    if any(word in text for word in [
        "shirt",
        "shoes",
        "clothes",
        "shopping",
        "dress"
    ]):
        return "Shopping"

    return "Other"


@app.get("/")
def home():
    return {
        "message": "HisabDo AI Receipt Scanner is running",
        "status": "success"
    }


@app.post("/scan-receipt")
async def scan_receipt(file: UploadFile = File(...)):

    # Read uploaded receipt as bytes
    image_bytes = await file.read()

    # Send bytes directly to EasyOCR
    results = reader.readtext(
        image_bytes,
        detail=0
    )

    # Combine OCR results
    extracted_text = "\n".join(results)

    # Extract total amount
    amount = extract_amount(extracted_text)

    # Categorize expense
    category = categorize_expense(extracted_text)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "amount": amount,
        "category": category
    }