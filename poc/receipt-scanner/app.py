from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import easyocr
import re
import os

app = FastAPI(
    title="HisabDo AI Receipt Scanner",
    description="Day 10 AI/ML Capstone POC",
    version="1.0.0"
)

# Initialize EasyOCR
reader = easyocr.Reader(["en"], gpu=False)


def extract_amount(text: str):
    """
    Extract the receipt total amount from OCR text.
    """

    # Look for amounts near words such as Total, Amount, Grand Total
    patterns = [
        r"(?:total|amount|grand\s*total|net\s*total)\s*[:\-]?\s*(?:Rs\.?|PKR|\$)?\s*(\d+(?:[.,]\d{1,2})?)",
        r"(?:Rs\.?|PKR|\$)\s*(\d+(?:[.,]\d{1,2})?)"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)

        if matches:
            try:
                amount = matches[-1].replace(",", "")
                return float(amount)
            except ValueError:
                pass

    return None


def categorize_expense(text: str):
    """
    Basic rule-based expense categorization for the POC.
    """

    text_lower = text.lower()

    categories = {
        "Food": [
            "restaurant",
            "food",
            "burger",
            "pizza",
            "cafe",
            "coffee",
            "grocery",
            "supermarket",
            "bakery"
        ],
        "Transport": [
            "uber",
            "careem",
            "fuel",
            "petrol",
            "diesel",
            "taxi",
            "transport"
        ],
        "Shopping": [
            "clothing",
            "shirt",
            "shoes",
            "mall",
            "shopping",
            "store"
        ],
        "Healthcare": [
            "pharmacy",
            "medicine",
            "hospital",
            "clinic",
            "doctor"
        ],
        "Utilities": [
            "electricity",
            "gas bill",
            "water bill",
            "internet",
            "utility"
        ]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category

    return "Other"


@app.get("/")
def home():
    return {
        "message": "HisabDo AI Receipt Scanner is running",
        "status": "success",
        "version": "Day 10 POC"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HisabDo AI Receipt Scanner"
    }


@app.post("/scan-receipt")
async def scan_receipt(file: UploadFile = File(...)):

    # Validate file type
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, JPEG, or PNG image."
        )

    try:
        # Read uploaded image
        image_bytes = await file.read()

        # Save temporarily
        temp_file = "temp_receipt.jpg"

        with open(temp_file, "wb") as f:
            f.write(image_bytes)

        # OCR
        results = reader.readtext(temp_file)

        # Combine OCR text
        extracted_text = "\n".join(
            result[1] for result in results
        )

        # Extract amount
        amount = extract_amount(extracted_text)

        # Categorize expense
        category = categorize_expense(extracted_text)

        # Delete temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

        return JSONResponse(
            content={
                "filename": file.filename,
                "extracted_text": extracted_text,
                "amount": amount,
                "category": category
            }
        )

    except Exception as e:

        if os.path.exists("temp_receipt.jpg"):
            os.remove("temp_receipt.jpg")

        raise HTTPException(
            status_code=500,
            detail=f"Receipt processing failed: {str(e)}"
        )