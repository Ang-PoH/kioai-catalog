def classify_lead(message: str) -> dict:
    text = message.lower()

    if any(word in text for word in ["precio", "cotización", "cotizacion", "llamada", "urgente"]):
        status = "hot"
        priority = "alta"
    elif any(word in text for word in ["información", "info", "me interesa", "automatizar"]):
        status = "warm"
        priority = "media"
    else:
        status = "nurturing"
        priority = "baja"

    return {
        "message": message,
        "status": status,
        "priority": priority,
        "next_action": "agendar llamada" if status == "hot" else "dar seguimiento",
    }


if __name__ == "__main__":
    print(classify_lead("Hola, quiero una cotización para automatizar WhatsApp"))
