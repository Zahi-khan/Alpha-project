import re

COMMON_MERCHANTS = {
    "starbucks": "Starbucks",
    "amazon": "Amazon",
    "uber": "Uber",
    "zomato": "Zomato",
    "swiggy": "Swiggy",
    "netflix": "Netflix",
}


def normalize_description(description: str) -> str:
    description = description.strip()
    description = re.sub(r"\s+", " ", description)
    return description


def normalize_merchant(description: str) -> str:
    text = description.lower()

    for keyword, merchant in COMMON_MERCHANTS.items():
        if keyword in text:
            return merchant

    return description.title()