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
    description="CatÃ¡logo web interactivo para KIOAI con FastAPI, HTML, CSS y JavaScript Vanilla.",
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
            "icon": "âš™ï¸",
            "title": "AutomatizaciÃ³n de procesos",
            "description": "Flujos inteligentes para reducir tareas repetitivas, conectar herramientas y acelerar operaciones internas.",
            "benefit": "Menos trabajo manual, mÃ¡s velocidad operativa.",
        },
        {
            "icon": "ðŸ¤–",
            "title": "Bots con IA",
            "description": "Bots conversacionales para WhatsApp, web, atenciÃ³n, captura de datos, seguimiento y soporte.",
            "benefit": "AtenciÃ³n mÃ¡s rÃ¡pida sin saturar al equipo.",
        },
        {
            "icon": "ðŸ“±",
            "title": "Social Media con IA",
            "description": "Calendarios de contenido, ideas, copies, captions, guiones, campaÃ±as y piezas para redes sociales.",
            "benefit": "Contenido constante, estratÃ©gico y mÃ¡s rÃ¡pido de producir.",
        },
        {
            "icon": "ðŸŽ¨",
            "title": "DiseÃ±o grÃ¡fico con IA",
            "description": "Creativos para anuncios, posts, mockups, branding, presentaciones y material comercial asistido por IA.",
            "benefit": "DiseÃ±o visual mÃ¡s Ã¡gil sin perder intenciÃ³n comercial.",
        },
        {
            "icon": "ðŸ“ˆ",
            "title": "Estrategia de marketing",
            "description": "Embudos, mensajes comerciales, campaÃ±as, benchmarking, anÃ¡lisis competitivo y propuesta de valor.",
            "benefit": "Marketing con direcciÃ³n, no solo publicaciones bonitas.",
        },
        {
            "icon": "ðŸ§©",
            "title": "PersonalizaciÃ³n de soluciones",
            "description": "Sistemas hechos a la medida segÃºn industria, proceso, equipo, objetivo comercial y herramientas existentes.",
            "benefit": "Soluciones adaptadas al negocio, no plantillas genÃ©ricas.",
        },
        {
            "icon": "ðŸ“Š",
            "title": "Dashboards y reportes",
            "description": "Reportes ejecutivos, tableros operativos y consolidaciÃ³n automÃ¡tica de datos desde mÃºltiples fuentes.",
            "benefit": "Decisiones con datos visibles y accionables.",
        },
        {
            "icon": "ðŸ“„",
            "title": "Procesamiento documental",
            "description": "OCR, clasificaciÃ³n, validaciÃ³n y extracciÃ³n de datos desde PDFs, imÃ¡genes, comprobantes y documentos.",
            "benefit": "Documentos convertidos en datos Ãºtiles.",
        },
        {
            "icon": "ðŸ”Œ",
            "title": "Integraciones API",
            "description": "ConexiÃ³n entre CRMs, formularios, WhatsApp, bases de datos, webhooks y servicios backend.",
            "benefit": "Herramientas conectadas en un mismo sistema.",
        },
        {
            "icon": "ðŸ•¸ï¸",
            "title": "Scraping y extracciÃ³n de datos",
            "description": "ExtracciÃ³n estructurada de informaciÃ³n pÃºblica, validaciones y monitoreo de fuentes digitales.",
            "benefit": "InformaciÃ³n clave sin captura manual.",
        },
    ],
    "projects": [
        {
            "id": "pizarra-concursal",
            "icon": "âš–ï¸",
            "name": "Pizarra Concursal",
            "summary": "Servicio FastAPI para consulta, scraping, evidencias y respuesta estructurada de informaciÃ³n concursal.",
            "problem": "El proceso requerÃ­a consultar informaciÃ³n pÃºblica, validar coincidencias y entregar evidencia sin depender de revisiÃ³n manual repetitiva.",
            "solution": "Se construyÃ³ un servicio con endpoints, scraping controlado, Playwright para evidencias y salida JSON lista para integrarse con n8n u otros sistemas.",
            "technologies": ["FastAPI", "Python", "Scraping", "Playwright", "APIs"],
            "categories": ["api", "automation", "data"],
            "videos": [
                "/static/videos/pizarra-demo-1.mp4",
                "/static/videos/pizarra-demo-2.mp4"
            ],
        },
        {
            "id": "repuve",
            "icon": "ðŸš—",
            "name": "REPUVE",
            "summary": "AutomatizaciÃ³n para procesamiento masivo de vehÃ­culos, consultas por lotes y manejo de escenarios con CAPTCHA.",
            "problem": "Las consultas manuales por vehÃ­culo eran lentas, difÃ­ciles de escalar y sensibles a bloqueos o validaciones externas.",
            "solution": "Se diseÃ±Ã³ una arquitectura por batches para procesar listas de vehÃ­culos, registrar resultados y manejar errores de forma controlada.",
            "technologies": ["AutomatizaciÃ³n", "Batches", "n8n", "APIs", "Procesamiento masivo"],
            "categories": ["automation", "data", "api"],
        },
        {
            "id": "swartz",
            "icon": "ðŸ§¾",
            "name": "Swartz",
            "summary": "Asistente contable con IA para recepciÃ³n, validaciÃ³n documental y soporte por WhatsApp.",
            "problem": "Los usuarios necesitaban enviar documentos fiscales y recibir orientaciÃ³n clara sin saturar al equipo contable.",
            "solution": "Se diseÃ±Ã³ un flujo con WhatsApp, OCR, validaciÃ³n documental, clasificaciÃ³n de archivos y respuestas basadas en reglas de negocio.",
            "technologies": ["WhatsApp", "OCR", "OpenAI", "n8n", "ValidaciÃ³n documental"],
            "categories": ["ai", "automation", "data"],
        },
        {
            "id": "riviera-smart",
            "icon": "ðŸï¸",
            "name": "Riviera Smart",
            "summary": "Sistema para matching inmobiliario, generaciÃ³n de propuestas patrimoniales y documentos personalizados.",
            "problem": "El equipo necesitaba convertir informaciÃ³n inmobiliaria dispersa en propuestas claras, visuales y personalizadas para prospectos.",
            "solution": "Se planteÃ³ un flujo de matching con IA, extracciÃ³n de datos, generaciÃ³n de HTML/PDF y entrega automatizada de propuestas.",
            "technologies": ["IA", "Matching", "PDF", "Google Drive", "AutomatizaciÃ³n"],
            "categories": ["ai", "automation", "data"],
        },
        {
            "id": "bot-educativo",
            "icon": "ðŸŽ“",
            "name": "Bot Educativo",
            "summary": "Bot educativo por Telegram con IA, planes de suscripciÃ³n y control de acceso mediante registros.",
            "problem": "Los estudiantes necesitaban un asistente acadÃ©mico accesible con lÃ­mites por plan y validaciÃ³n sencilla de pagos.",
            "solution": "Se diseÃ±Ã³ un bot con registro en Sheets, referencias de pago, validaciÃ³n manual y activaciÃ³n automÃ¡tica segÃºn estatus.",
            "technologies": ["Telegram", "OpenAI", "Google Sheets", "Suscripciones", "AutomatizaciÃ³n"],
            "categories": ["ai", "automation"],
        },
        {
            "id": "ki-os",
            "icon": "ðŸ«€",
            "name": "Ki OS",
            "summary": "Laboratorio interno para experimentar con voz, memoria, modelos locales y experiencias persistentes de IA.",
            "problem": "Se requerÃ­a un espacio experimental para probar interacciÃ³n por voz, memoria persistente y arquitectura de asistente personal.",
            "solution": "Se creÃ³ un laboratorio interno conectado a microservicios, modelos locales y servicios de IA para prototipar capacidades avanzadas.",
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
            "title": "DiseÃ±o",
            "description": "Mapeamos arquitectura, datos, herramientas, riesgos y experiencia del usuario.",
        },
        {
            "title": "Desarrollo",
            "description": "Construimos el MVP con cÃ³digo limpio, flujos claros e integraciones mantenibles.",
        },
        {
            "title": "Pruebas",
            "description": "Validamos errores, casos reales, respuestas, tiempos y rutas alternativas.",
        },
        {
            "title": "ImplementaciÃ³n",
            "description": "Dejamos la soluciÃ³n corriendo en entorno local, cloud o herramienta operativa.",
        },
        {
            "title": "Soporte",
            "description": "Ajustamos, documentamos y mejoramos segÃºn uso real del negocio.",
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
        raise HTTPException(status_code=400, detail="El correo no parece vÃ¡lido.")

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
        label = "CÃ³digo" if any(word in file_stem for word in ["code", "codigo", "script", "api"]) else "Workflow"

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

