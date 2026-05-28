const state = {
  catalog: null,
  activeFilter: "all",
};

const qs = (selector) => document.querySelector(selector);
const qsa = (selector) => [...document.querySelectorAll(selector)];

function createElement(tag, className, html) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (html) element.innerHTML = html;
  return element;
}

function showToast(message) {
  const toast = qs("#toast");
  toast.textContent = message;
  toast.classList.add("visible");

  window.setTimeout(() => {
    toast.classList.remove("visible");
  }, 3600);
}

async function fetchCatalog() {
  const response = await fetch("/api/catalog");

  if (!response.ok) {
    throw new Error("No se pudo cargar el catálogo.");
  }

  return response.json();
}

function renderServices(services) {
  const grid = qs("#servicesGrid");
  grid.innerHTML = "";

  services.forEach((service) => {
    const card = createElement(
      "article",
      "service-card reveal",
      `
        <div class="card-icon">${service.icon}</div>
        <h3>${service.title}</h3>
        <p>${service.description}</p>
        <div class="benefit">${service.benefit}</div>
      `
    );

    grid.appendChild(card);
  });
}

function renderProjects(projects) {
  const grid = qs("#projectsGrid");
  grid.innerHTML = "";

  const filteredProjects =
    state.activeFilter === "all"
      ? projects
      : projects.filter((project) => project.categories.includes(state.activeFilter));

  filteredProjects.forEach((project) => {
    const tags = project.technologies
      .map((tech) => `<span class="project-tag">${tech}</span>`)
      .join("");

    const card = createElement(
      "article",
      "project-card reveal",
      `
        <div class="card-icon">${project.icon}</div>
        <h3>${project.name}</h3>
        <p>${project.summary}</p>
        <div class="project-tags">${tags}</div>
        <button class="project-open" type="button" data-project-id="${project.id}">
          Ver problema, solución y stack →
        </button>
      `
    );

    grid.appendChild(card);
  });

  hydrateProjectButtons();
  observeReveals();
}

function renderTechnologies(technologies) {
  const grid = qs("#techGrid");
  grid.innerHTML = "";

  technologies.forEach((tech) => {
    const pill = createElement("div", "tech-pill", tech);
    grid.appendChild(pill);
  });
}

function renderProcess(process) {
  const timeline = qs("#processTimeline");
  timeline.innerHTML = "";

  process.forEach((step, index) => {
    const item = createElement(
      "article",
      "timeline-step",
      `
        <div class="timeline-number">${String(index + 1).padStart(2, "0")}</div>
        <h3>${step.title}</h3>
        <p>${step.description}</p>
      `
    );

    timeline.appendChild(item);
  });
}

function formatGalleryTitle(filename) {
  return filename
    .replace(/\.[^/.]+$/, "")
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function renderGallery(items) {
  const grid = qs("#galleryGrid");
  if (!grid) return;

  grid.innerHTML = "";

  if (!items || !items.length) {
    grid.innerHTML = `
      <article class="gallery-card">
        <div class="gallery-card-body">
          <span class="gallery-badge">Info</span>
          <h3>Aún no hay imágenes cargadas</h3>
          <p>Agrega screenshots o imágenes en app/static/gallery para mostrarlas aquí.</p>
        </div>
      </article>
    `;
    return;
  }

  items.forEach((item) => {
    const card = createElement(
      "article",
      "gallery-card reveal",
      `
        <img class="gallery-image" src="${item.url}?v=${Date.now()}" alt="${item.filename}">
        <div class="gallery-card-body">
          <span class="gallery-badge">${item.label}</span>
          <h3>${formatGalleryTitle(item.filename)}</h3>
          <a class="gallery-link" href="${item.url}" target="_blank" rel="noopener">Abrir imagen</a>
        </div>
      `
    );

    grid.appendChild(card);
  });
}

function renderCodeExamples(items) {
  const grid = qs("#codeGrid");
  if (!grid) return;

  grid.innerHTML = "";

  if (!items || !items.length) {
    grid.innerHTML = `
      <article class="code-card">
        <h3>Sin ejemplos cargados</h3>
        <p>Agrega archivos .py en app/static/code-examples.</p>
      </article>
    `;
    return;
  }

  items.forEach((item) => {
    const escapedPreview = item.preview
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    const card = createElement(
      "article",
      "code-card reveal",
      `
        <div class="code-card-top">
          <span class="code-language">${item.language}</span>
          <a href="${item.url}" target="_blank" rel="noopener">Abrir archivo</a>
        </div>
        <h3>${item.title}</h3>
        <pre><code>${escapedPreview}</code></pre>
      `
    );

    grid.appendChild(card);
  });
}

function hydrateFilters() {
  qsa(".filter-btn").forEach((button) => {
    button.addEventListener("click", () => {
      qsa(".filter-btn").forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      state.activeFilter = button.dataset.filter;
      renderProjects(state.catalog.projects);
    });
  });
}

function hydrateProjectButtons() {
  qsa("[data-project-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const project = state.catalog.projects.find(
        (item) => item.id === button.dataset.projectId
      );

      if (project) {
        openProjectModal(project);
      }
    });
  });
}

function openProjectModal(project) {
  const modal = qs("#projectModal");
  const modalContent = qs("#modalContent");

  const videos = Array.isArray(project.videos) && project.videos.length
    ? `
      <div class="modal-block">
        <strong>Demos visuales</strong>
        <div class="video-grid">
          ${project.videos
            .map((videoUrl, index) => `
              <video class="demo-video" controls preload="metadata">
                <source src="${videoUrl}" type="video/mp4">
                Tu navegador no puede reproducir este video.
              </video>
              <p class="video-caption">Demo ${index + 1} · ${project.name}</p>
            `)
            .join("")}
        </div>
      </div>
    `
    : "";

  modalContent.innerHTML = `
    <div class="modal-body">
      <div class="card-icon">${project.icon}</div>
      <h3>${project.name}</h3>

      ${videos}

      <div class="modal-block">
        <strong>Problema</strong>
        <p>${project.problem}</p>
      </div>

      <div class="modal-block">
        <strong>Solución</strong>
        <p>${project.solution}</p>
      </div>

      <div class="modal-block">
        <strong>Tecnologías utilizadas</strong>
        <p>${project.technologies.join(" · ")}</p>
      </div>
    </div>
  `;

  modal.showModal();
}

function hydrateModal() {
  const modal = qs("#projectModal");
  const closeButton = qs("#modalClose");

  closeButton.addEventListener("click", () => modal.close());

  modal.addEventListener("click", (event) => {
    const modalBox = modal.getBoundingClientRect();

    const clickedOutside =
      event.clientX < modalBox.left ||
      event.clientX > modalBox.right ||
      event.clientY < modalBox.top ||
      event.clientY > modalBox.bottom;

    if (clickedOutside) {
      modal.close();
    }
  });
}

function hydrateNavigation() {
  const navToggle = qs("#navToggle");
  const navLinks = qs("#navLinks");

  navToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });

  qsa(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
    });
  });
}

function observeReveals() {
  const revealElements = qsa(".reveal:not(.visible)");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14 }
  );

  revealElements.forEach((element) => observer.observe(element));
}

function hydrateLeadForm() {
  const form = qs("#leadForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    const payload = {
      name: formData.get("name"),
      company: formData.get("company"),
      email: formData.get("email"),
      message: formData.get("message"),
      source: "kioai-catalog-mvp",
    };

    try {
      const response = await fetch("/api/leads", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "No se pudo guardar el lead.");
      }

      form.reset();
      showToast("Solicitud enviada. Lead guardado correctamente en FastAPI.");
    } catch (error) {
      showToast(error.message || "Ocurrió un error al enviar la solicitud.");
    }
  });
}

async function init() {
  try {
    qs("#currentYear").textContent = new Date().getFullYear();

    hydrateNavigation();
    hydrateModal();
    hydrateFilters();
    hydrateLeadForm();

    state.catalog = await fetchCatalog();

    renderServices(state.catalog.services);
    renderProjects(state.catalog.projects);
    renderTechnologies(state.catalog.technologies);
    renderProcess(state.catalog.process);

    const galleryResponse = await fetch(`/api/gallery?t=${Date.now()}`);
    const galleryData = await galleryResponse.json();
    renderGallery(galleryData.items);

    const codeResponse = await fetch(`/api/code-examples?t=${Date.now()}`);
    const codeData = await codeResponse.json();
    renderCodeExamples(codeData.items);

    observeReveals();
  } catch (error) {
    console.error(error);
    showToast("No se pudo inicializar el catálogo.");
  }
}

document.addEventListener("DOMContentLoaded", init);







