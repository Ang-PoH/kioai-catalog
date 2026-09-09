from datetime import datetime, timezone
from pathlib import Path
import json
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LEADS_FILE = DATA_DIR / "leads.json"
GALLERY_DIR = BASE_DIR / "static" / "gallery"

app = FastAPI(
    title="KIOAI Catalog MVP",
    description="Catálogo web interactivo para KIOAI con FastAPI, HTML, CSS y JavaScript Vanilla.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., min_length=5, max_length=180)
    company: str | None = Field(default=None, max_length=160)
    message: str = Field(..., min_length=8, max_length=1200)
    source: str | None = Field(default="kioai-catalog-mvp", max_length=120)


def ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not LEADS_FILE.exists():
        LEADS_FILE.write_text("[]", encoding="utf-8")


def read_leads() -> list[dict]:
    ensure_storage()

    try:
        content = LEADS_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError:
        return []


def write_leads(leads: list[dict]) -> None:
    ensure_storage()
    LEADS_FILE.write_text(
        json.dumps(leads, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


CATALOG = {
    "services": [
        {
            "icon": "⚙️",
            "title": "Automatización de procesos",
            "description": "Flujos inteligentes para reducir tareas repetitivas, conectar herramientas y acelerar operaciones internas.",
            "benefit": "Menos trabajo manual, más velocidad operativa.",
        },
        {
            "icon": "🤖",
            "title": "Bots con IA",
            "description": "Bots conversacionales para WhatsApp, web, atención, captura de datos, seguimiento y soporte.",
            "benefit": "Atención más rápida sin saturar al equipo.",
        },
        {
            "icon": "📱",
            "title": "Social Media con IA",
            "description": "Calendarios de contenido, ideas, copies, captions, guiones, campañas y piezas para redes sociales.",
            "benefit": "Contenido constante, estratégico y más rápido de producir.",
        },
        {
            "icon": "🎨",
            "title": "Diseño gráfico con IA",
            "description": "Creativos para anuncios, posts, mockups, branding, presentaciones y material comercial asistido por IA.",
            "benefit": "Diseño visual más ágil sin perder intención comercial.",
        },
        {
            "icon": "📈",
            "title": "Estrategia de marketing",
            "description": "Embudos, mensajes comerciales, campañas, benchmarking, análisis competitivo y propuesta de valor.",
            "benefit": "Marketing con dirección, no solo publicaciones bonitas.",
        },
        {
            "icon": "🧩",
            "title": "Personalización de soluciones",
            "description": "Sistemas hechos a la medida según industria, proceso, equipo, objetivo comercial y herramientas existentes.",
            "benefit": "Soluciones adaptadas al negocio, no plantillas genéricas.",
        },
        {
            "icon": "📊",
            "title": "Dashboards y reportes",
            "description": "Reportes ejecutivos, tableros operativos y consolidación automática de datos desde múltiples fuentes.",
            "benefit": "Decisiones con datos visibles y accionables.",
        },
        {
            "icon": "📄",
            "title": "Procesamiento documental",
            "description": "OCR, clasificación, validación y extracción de datos desde PDFs, imágenes, comprobantes y documentos.",
            "benefit": "Documentos convertidos en datos útiles.",
        },
        {
            "icon": "🔌",
            "title": "Integraciones API",
            "description": "Conexión entre CRMs, formularios, WhatsApp, bases de datos, webhooks y servicios backend.",
            "benefit": "Herramientas conectadas en un mismo sistema.",
        },
        {
            "icon": "🕸️",
            "title": "Scraping y extracción de datos",
            "description": "Extracción estructurada de información pública, validaciones y monitoreo de fuentes digitales.",
            "benefit": "Información clave sin captura manual.",
        },
    ],
    "projects": [
        {
            "id": "pizarra-concursal",
            "icon": "⚖️",
            "name": "Pizarra Concursal",
            "summary": "Servicio FastAPI para consulta, scraping, evidencias y respuesta estructurada de información concursal.",
            "problem": "El proceso requería consultar información pública, validar coincidencias y entregar evidencia sin depender de revisión manual repetitiva.",
            "solution": "Se construyó un servicio con endpoints, scraping controlado, Playwright para evidencias y salida JSON lista para integrarse con n8n u otros sistemas.",
            "technologies": ["FastAPI", "Python", "Scraping", "Playwright", "APIs"],
            "categories": ["api", "automation", "data"],
            "videos": [
                "/static/videos/pizarra-demo-1.mp4",
                "/static/videos/pizarra-demo-2.mp4"
            ],
        },
        {
            "id": "repuve",
            "icon": "🚗",
            "name": "REPUVE",
            "summary": "Automatización para procesamiento masivo de vehículos, consultas por lotes y manejo de escenarios con CAPTCHA.",
            "problem": "Las consultas manuales por vehículo eran lentas, difíciles de escalar y sensibles a bloqueos o validaciones externas.",
            "solution": "Se diseñó una arquitectura por batches para procesar listas de vehículos, registrar resultados y manejar errores de forma controlada.",
            "technologies": ["Automatización", "Batches", "n8n", "APIs", "Procesamiento masivo"],
            "categories": ["automation", "data", "api"],
        },
        {
            "id": "swartz",
            "icon": "🧾",
            "name": "Swartz",
            "summary": "Asistente contable con IA para recepción, validación documental y soporte por WhatsApp.",
            "problem": "Los usuarios necesitaban enviar documentos fiscales y recibir orientación clara sin saturar al equipo contable.",
            "solution": "Se diseñó un flujo con WhatsApp, OCR, validación documental, clasificación de archivos y respuestas basadas en reglas de negocio.",
            "technologies": ["WhatsApp", "OCR", "OpenAI", "n8n", "Validación documental"],
            "categories": ["ai", "automation", "data"],
        },
        {
            "id": "riviera-smart",
            "icon": "🏝️",
            "name": "Riviera Smart",
            "summary": "Sistema para matching inmobiliario, generación de propuestas patrimoniales y documentos personalizados.",
            "problem": "El equipo necesitaba convertir información inmobiliaria dispersa en propuestas claras, visuales y personalizadas para prospectos.",
            "solution": "Se planteó un flujo de matching con IA, extracción de datos, generación de HTML/PDF y entrega automatizada de propuestas.",
            "technologies": ["IA", "Matching", "PDF", "Google Drive", "Automatización"],
            "categories": ["ai", "automation", "data"],
        },
        {
            "id": "bot-educativo",
            "icon": "🎓",
            "name": "Bot Educativo",
            "summary": "Bot educativo por Telegram con IA, planes de suscripción y control de acceso mediante registros.",
            "problem": "Los estudiantes necesitaban un asistente académico accesible con límites por plan y validación sencilla de pagos.",
            "solution": "Se diseñó un bot con registro en Sheets, referencias de pago, validación manual y activación automática según estatus.",
            "technologies": ["Telegram", "OpenAI", "Google Sheets", "Suscripciones", "Automatización"],
            "categories": ["ai", "automation"],
        },
        {
            "id": "ki-os",
            "icon": "🫀",
            "name": "Ki OS",
            "summary": "Laboratorio interno para experimentar con voz, memoria, modelos locales y experiencias persistentes de IA.",
            "problem": "Se requería un espacio experimental para probar interacción por voz, memoria persistente y arquitectura de asistente personal.",
            "solution": "Se creó un laboratorio interno conectado a microservicios, modelos locales y servicios de IA para prototipar capacidades avanzadas.",
            "technologies": ["Voz", "Memoria", "OpenAI", "FastAPI", "Modelos locales"],
            "categories": ["ai", "api"],
        },
    ],
    "technologies": [
        "OpenAI",
        "FastAPI",
        "Docker",
        "n8n",
        "Make",
        "PostgreSQL",
        "Python",
        "WhatsApp",
        "Google Sheets",
        "AWS",
        "GitHub",
    ],
    "process": [
        {
            "title": "Descubrimiento",
            "description": "Entendemos el proceso, los dolores operativos y el objetivo comercial.",
        },
        {
            "title": "Diseño",
            "description": "Mapeamos arquitectura, datos, herramientas, riesgos y experiencia del usuario.",
        },
        {
            "title": "Desarrollo",
            "description": "Construimos el MVP con código limpio, flujos claros e integraciones mantenibles.",
        },
        {
            "title": "Pruebas",
            "description": "Validamos errores, casos reales, respuestas, tiempos y rutas alternativas.",
        },
        {
            "title": "Implementación",
            "description": "Dejamos la solución corriendo en entorno local, cloud o herramienta operativa.",
        },
        {
            "title": "Soporte",
            "description": "Ajustamos, documentamos y mejoramos según uso real del negocio.",
        },
    ],
}


@app.on_event("startup")
def startup_event() -> None:
    ensure_storage()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "kioai-catalog",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/catalog")
def get_catalog():
    return CATALOG


@app.get("/api/leads")
def get_leads():
    return {
        "count": len(read_leads()),
        "items": read_leads(),
    }


@app.get("/api/gallery")
def get_gallery():
    return {
        "count": len(get_gallery_items()),
        "items": get_gallery_items(),
    }


@app.post("/api/leads", status_code=201)
def create_lead(payload: LeadCreate):
    if "@" not in payload.email:
        raise HTTPException(status_code=400, detail="El correo no parece válido.")

    leads = read_leads()

    lead = {
        "id": str(uuid.uuid4()),
        "name": payload.name.strip(),
        "email": payload.email.strip().lower(),
        "company": payload.company.strip() if payload.company else None,
        "message": payload.message.strip(),
        "source": payload.source or "kioai-catalog-mvp",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    leads.append(lead)
    write_leads(leads)

    return {
        "success": True,
        "message": "Lead guardado correctamente.",
        "lead": lead,
    }


def get_gallery_items() -> list[dict]:
    gallery_dir = BASE_DIR / "static" / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)

    allowed_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    items: list[dict] = []

    for file in sorted(gallery_dir.iterdir()):
        if not file.is_file():
            continue

        if file.suffix.lower() not in allowed_extensions:
            continue

        file_stem = file.stem.lower()
        label = "Código" if any(word in file_stem for word in ["code", "codigo", "script", "api"]) else "Workflow"

        items.append(
            {
                "filename": file.name,
                "label": label,
                "url": f"/static/gallery/{file.name}",
            }
        )

    return items


def get_code_examples() -> list[dict]:
    examples_dir = BASE_DIR / "static" / "code-examples"
    examples_dir.mkdir(parents=True, exist_ok=True)

    items: list[dict] = []

    for file in sorted(examples_dir.iterdir()):
        if file.is_file() and file.suffix.lower() == ".py":
            title = file.stem.replace("_", " ").replace("-", " ").title()
            preview = file.read_text(encoding="utf-8")[:1400]

            items.append(
                {
                    "filename": file.name,
                    "title": title,
                    "language": "Python",
                    "url": f"/static/code-examples/{file.name}",
                    "preview": preview,
                }
            )

    return items


@app.get("/api/code-examples")
def code_examples():
    return {
        "count": len(get_code_examples()),
        "items": get_code_examples(),
    }


@app.get("/catalog", response_class=HTMLResponse)
def catalog_page(request: Request):
    return templates.TemplateResponse(request=request, name="catalog.html", context={})


MOMENTS_DEMOS = {
    "ivory",
    "midnight",
    "elan",
    "aura",
    "film",
    "maison",
}


@app.get("/moments", response_class=HTMLResponse)
def moments_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="moments.html",
        context={},
    )


@app.get("/moments/demo/{slug}", response_class=HTMLResponse)
def moments_demo(request: Request, slug: str):
    normalized_slug = slug.strip().lower()

    if normalized_slug not in MOMENTS_DEMOS:
        raise HTTPException(
            status_code=404,
            detail="La experiencia solicitada no existe.",
        )

    return templates.TemplateResponse(
        request=request,
        name="moments/demo.html",
        context={
            "demo_slug": normalized_slug,
        },
    )
