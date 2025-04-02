import { qs } from "./selectors.js";
import { renderPage } from "./utils.js";
import SideNav from "./components/SideNav.js";
import { Pages } from "./routes.js";


// Get Elements
const rootContainer = qs(".root")!;

const main = (): void => {
  document.addEventListener("DOMContentLoaded", () => {
    // Layout
    SideNav({ parent: rootContainer });

    // Initial page render
    renderPage(Pages.DASHBOARD);
  });
};

main()
