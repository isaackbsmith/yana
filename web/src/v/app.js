import { renderDashboard } from "./dashboard.js";
import { renderMedication } from "./medication.js";
import { renderAdherenceReportsV1 } from "./ar1.js";
import { renderAdherenceReportsV2 } from "./ar2.js";

const mainContent = document.getElementById("main-content");
const navLinks = document.querySelectorAll("#main-nav a[data-page]");
const toggleNav = document.getElementById("toggle-nav");
const navigation = document.getElementById("main-nav");
const mainContainer = document.querySelector(".main");

function renderPage(page) {
  mainContent.innerHTML = '<div class="loader">Loading...</div>';
  switch (page) {
    case "dashboard":
      renderDashboard();
      break;
    case "appointments":
      renderAppointments();
      break;
    case "medication":
      renderMedication();
      break;
    case "ar1":
      renderAdherenceReportsV1();
      break;
    case "ar2":
      renderAdherenceReportsV2();
      break;
    case "faq":
      renderFAQ();
      break;
    case "settings":
      renderSettings();
      break;
    default:
      mainContent.innerHTML = "<h1>404 - Page Not Found</h1>";
  }
}

navLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const page = e.currentTarget.getAttribute("data-page");
    renderPage(page);
    navLinks.forEach((l) => l.classList.remove("active"));
    e.currentTarget.classList.add("active");
  });
});

toggleNav.addEventListener("click", () => {
  navigation.classList.toggle("hidden");
  mainContainer.classList.toggle("nav-open");
});

// Initial page render
renderPage("dashboard");
