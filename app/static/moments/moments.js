const menuButton = document.querySelector(".moments-menu-button");
const navLinks = document.querySelector(".moments-nav-links");

if (menuButton && navLinks) {
  menuButton.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
    });
  });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        return;
      }

      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    });
  },
  {
    threshold: 0.12,
  },
);

document.querySelectorAll(".reveal").forEach((element) => {
  revealObserver.observe(element);
});
