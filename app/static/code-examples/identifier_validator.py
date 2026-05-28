import re

CURP_REGEX = re.compile(
    r"^[A-Z][AEIOU][A-Z]{2}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]\d$",
    re.IGNORECASE
)

RFC_REGEX = re.compile(
    r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$",
    re.IGNORECASE
)

def validate_identifier(value: str) -> dict:
    clean_value = value.strip().upper().replace(" ", "")

    return {
        "input": value,
        "normalized": clean_value,
        "is_curp": bool(CURP_REGEX.match(clean_value)),
        "is_rfc": bool(RFC_REGEX.match(clean_value)),
    }


if __name__ == "__main__":
    samples = [
        "OEPJ990906HHGRRN09",
        "XAXX010101000",
        "texto invalido"
    ]

    for sample in samples:
        print(validate_identifier(sample))
