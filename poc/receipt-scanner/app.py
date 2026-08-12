from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import easyocr
import re
import os
import uuid
import cv2


app = FastAPI(
    title="HisabDo AI Receipt Scanner",
    description="Day 12 application-ready AI Receipt Scanner API",
    version="1.2.0"
)


# ---------------------------------------------------------
# EasyOCR
# ---------------------------------------------------------

reader = easyocr.Reader(["en"], gpu=False)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg"
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ---------------------------------------------------------
# Amount Extraction
# ---------------------------------------------------------

def extract_amount(text: str):
    """
    Extract the receipt total amount from OCR text.
    """

    normalized = re.sub(r"\s+", " ", text)

    # Priority 1: TOTAL / GRAND TOTAL / NET TOTAL
    total_patterns = [
        r"\btotal\b\s*[:\-]?\s*(?:rs\.?|pkr|\$)?\s*([0-9]+(?:[.,][0-9]{1,2})?)",
        r"\bgrand\s*total\b\s*[:\-]?\s*(?:rs\.?|pkr|\$)?\s*([0-9]+(?:[.,][0-9]{1,2})?)",
        r"\bnet\s*total\b\s*[:\-]?\s*(?:rs\.?|pkr|\$)?\s*([0-9]+(?:[.,][0-9]{1,2})?)"
    ]

    for pattern in total_patterns:

        matches = re.findall(
            pattern,
            normalized,
            flags=re.IGNORECASE
        )

        if matches:
            try:
                amount = matches[-1].replace(",", ".")
                return float(amount)
            except ValueError:
                continue

    # Priority 2: Currency amounts
    currency_patterns = [
        r"(?:rs\.?|pkr|\$)\s*([0-9]+(?:[.,][0-9]{1,2})?)"
    ]

    for pattern in currency_patterns:

        matches = re.findall(
            pattern,
            normalized,
            flags=re.IGNORECASE
        )

        if matches:
            try:
                amounts = []

                for value in matches:
                    value = value.replace(",", ".")
                    amounts.append(float(value))

                if amounts:
                    return amounts[-1]

            except ValueError:
                continue

    return None


# ---------------------------------------------------------
# Subtotal and Tax Extraction
# ---------------------------------------------------------

def extract_subtotal_and_tax(text: str):
    """
    Extract subtotal and tax from OCR text.
    These values are used to validate the final amount.
    """

    normalized = re.sub(r"\s+", " ", text)

    subtotal = None
    tax = None

    subtotal_pattern = (
        r"\bsubtotal\b\s*[:\-]?\s*"
        r"(?:rs\.?|pkr|\$)?\s*"
        r"([0-9]+(?:[.,][0-9]{1,2})?)"
    )

    tax_pattern = (
        r"\btax\b\s*[:\-]?\s*"
        r"(?:rs\.?|pkr|\$)?\s*"
        r"([0-9]+(?:[.,][0-9]{1,2})?)"
    )

    subtotal_match = re.search(
        subtotal_pattern,
        normalized,
        flags=re.IGNORECASE
    )

    tax_match = re.search(
        tax_pattern,
        normalized,
        flags=re.IGNORECASE
    )

    if subtotal_match:
        subtotal = float(
            subtotal_match.group(1).replace(",", ".")
        )

    if tax_match:
        tax = float(
            tax_match.group(1).replace(",", ".")
        )

    return subtotal, tax


# ---------------------------------------------------------
# Amount Validation
# ---------------------------------------------------------

def validate_amount_with_totals(text: str, extracted_amount):
    """
    Validate the OCR total using:

    Subtotal + Tax = Expected Total

    If the OCR total is incorrect, the validated
    calculated total is used.
    """

    subtotal, tax = extract_subtotal_and_tax(text)

    if subtotal is not None and tax is not None:

        calculated_total = round(
            subtotal + tax,
            2
        )

        # If OCR did not find a total,
        # use the calculated total.
        if extracted_amount is None:
            return calculated_total

        # If OCR total differs from the calculated
        # total, prefer the validated value.
        if abs(extracted_amount - calculated_total) > 0.05:
            return calculated_total

    return extracted_amount


# ---------------------------------------------------------
# Expense Categorization
# ---------------------------------------------------------

def categorize_expense(text: str):
    """
    Basic rule-based expense categorization.
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


# ---------------------------------------------------------
# Response Validation
# ---------------------------------------------------------

def validate_response(
    extracted_text: str,
    amount,
    category: str
):
    """
    Validate the final structured response.
    """

    if not extracted_text.strip():
        raise ValueError(
            "No readable text was detected in the receipt."
        )

    if amount is not None:

        if amount < 0:
            raise ValueError(
                "Extracted amount cannot be negative."
            )

        if amount > 10_000_000:
            raise ValueError(
                "Extracted amount is outside the expected range."
            )

    allowed_categories = {
        "Food",
        "Transport",
        "Shopping",
        "Healthcare",
        "Utilities",
        "Other"
    }

    if category not in allowed_categories:
        raise ValueError(
            "Invalid expense category generated."
        )


# ---------------------------------------------------------
# OCR Helper
# ---------------------------------------------------------

def run_ocr(image_path: str):
    """
    Run EasyOCR on an image.
    """

    results = reader.readtext(image_path)

    text = "\n".join(
        result[1]
        for result in results
        if len(result) >= 2
    )

    return text.strip()


# ---------------------------------------------------------
# Image Preprocessing
# ---------------------------------------------------------

def preprocess_image(input_path: str, output_path: str):
    """
    Improve receipt image before OCR.
    """

    image = cv2.imread(input_path)

    if image is None:
        raise ValueError(
            "Unable to read the uploaded image."
        )

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Improve contrast
    gray = cv2.equalizeHist(gray)

    # Enlarge image
    gray = cv2.resize(
        gray,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # Reduce noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Adaptive threshold
    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    cv2.imwrite(
        output_path,
        processed
    )


# ---------------------------------------------------------
# Choose Best OCR Result
# ---------------------------------------------------------

def choose_best_text(
    original_text,
    processed_text
):
    """
    Choose the OCR result that provides
    better receipt information.
    """

    original_has_total = bool(
        re.search(
            r"\btotal\b",
            original_text,
            flags=re.IGNORECASE
        )
    )

    processed_has_total = bool(
        re.search(
            r"\btotal\b",
            processed_text,
            flags=re.IGNORECASE
        )
    )

    if processed_has_total and not original_has_total:
        return processed_text

    if original_has_total:
        return original_text

    if len(processed_text) > len(original_text):
        return processed_text

    return original_text


# ---------------------------------------------------------
# Home Endpoint
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "HisabDo AI Receipt Scanner is running",
        "status": "success",
        "version": "Day 12"
    }


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "HisabDo AI Receipt Scanner",
        "ocr": "EasyOCR"
    }


# ---------------------------------------------------------
# Receipt Scanner Endpoint
# ---------------------------------------------------------

@app.post("/scan-receipt")
async def scan_receipt(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # 1. Filename validation
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename was provided."
        )


    # -----------------------------------------------------
    # 2. File type validation
    # -----------------------------------------------------

    if file.content_type not in ALLOWED_TYPES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file type. "
                "Please upload a JPG, JPEG, or PNG image."
            )
        )


    # -----------------------------------------------------
    # 3. Read uploaded file
    # -----------------------------------------------------

    try:

        image_bytes = await file.read()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Unable to read the uploaded file."
        )


    # -----------------------------------------------------
    # 4. Empty file validation
    # -----------------------------------------------------

    if not image_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )


    # -----------------------------------------------------
    # 5. File size validation
    # -----------------------------------------------------

    if len(image_bytes) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 5 MB."
        )


    # -----------------------------------------------------
    # 6. Temporary file names
    # -----------------------------------------------------

    unique_id = uuid.uuid4().hex

    temp_file = f"temp_receipt_{unique_id}.jpg"

    processed_file = (
        f"processed_receipt_{unique_id}.png"
    )


    try:

        # -------------------------------------------------
        # Save uploaded image
        # -------------------------------------------------

        with open(temp_file, "wb") as f:
            f.write(image_bytes)


        # -------------------------------------------------
        # OCR original image
        # -------------------------------------------------

        original_text = run_ocr(
            temp_file
        )


        # -------------------------------------------------
        # Preprocess image
        # -------------------------------------------------

        preprocess_image(
            temp_file,
            processed_file
        )


        # -------------------------------------------------
        # OCR processed image
        # -------------------------------------------------

        processed_text = run_ocr(
            processed_file
        )


        # -------------------------------------------------
        # Choose best OCR result
        # -------------------------------------------------

        extracted_text = choose_best_text(
            original_text,
            processed_text
        )


        # -------------------------------------------------
        # OCR validation
        # -------------------------------------------------

        if not extracted_text:

            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text was detected. "
                    "Please upload a clearer receipt image."
                )
            )


        # -------------------------------------------------
        # Extract OCR amount
        # -------------------------------------------------

        amount = extract_amount(
            extracted_text
        )


        # -------------------------------------------------
        # Validate amount using subtotal + tax
        # -------------------------------------------------

        amount = validate_amount_with_totals(
            extracted_text,
            amount
        )


        # -------------------------------------------------
        # Categorize expense
        # -------------------------------------------------

        category = categorize_expense(
            extracted_text
        )


        # -------------------------------------------------
        # Validate final response
        # -------------------------------------------------

        try:

            validate_response(
                extracted_text,
                amount,
                category
            )

        except ValueError as validation_error:

            raise HTTPException(
                status_code=422,
                detail=str(validation_error)
            )


        # -------------------------------------------------
        # Return structured response
        # -------------------------------------------------

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "filename": file.filename,
                "extracted_text": extracted_text,
                "amount": amount,
                "category": category
            }
        )


    except HTTPException:

        raise


    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Receipt processing failed. "
                "Please try again with a clearer image."
            )
        )


    finally:

        # -------------------------------------------------
        # Remove temporary files
        # -------------------------------------------------

        for temporary_file in [
            temp_file,
            processed_file
        ]:

            if os.path.exists(temporary_file):

                try:
                    os.remove(temporary_file)

                except Exception:
                    pass