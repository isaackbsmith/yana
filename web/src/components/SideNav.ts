import { Pages } from "../routes";
import { qs, qsa } from "../selectors";
import { insertElement, renderPage, strToEnum } from "../utils";
import navLinks from "../static/navLinks.json";
import { ComponentProps } from "../types";


export default (props: ComponentProps): Element | undefined => {
  const sideNavHTML = `
  <div class="container">
    <div id="main-nav" class="navigation">
      <ul>
        <li class="logo">
          <a href="#" data-page="Dashboard" class="nav-link">
            <span class="icon">
              <ion-icon name="heart-circle-outline"></ion-icon>
            </span>
            <span class="title">YANA</span>
          </a>
        </li>
  ${navLinks.map((link) => (
    `
        <li>
          <a href="#" data-page=${link.name} class="nav-link">
            <span class="icon">
              <ion-icon name=${link.icon}></ion-icon>
            </span>
            <span class="title">${link.name}</span>
          </a>
        </li>
        `
  )).join("")}
      </ul>
    </div>
    `

  try {
    // Render the side nav
    insertElement({ parent: props.parent, child: sideNavHTML, position: "afterbegin" });

    const sideNavContainer = qs(".container")!;
    const sideNavLinks = qsa<HTMLAnchorElement>(".nav-link")!
    console.log("Links", sideNavLinks);

    // set the currently clicked link active
    const setActiveLink = (link: HTMLAnchorElement): void => {
      sideNavLinks.forEach((l) => l.classList.remove("active"));
      link.classList.add("active");
    }

    // Attach 'click' event handlers to every nav-link and
    // navigate to the page
    sideNavContainer.addEventListener("click", (e) => {
      const target = e.target as HTMLAnchorElement;
      if (target.matches(".nav-link")) {
        const page = target.getAttribute("data-page")!;
        renderPage(strToEnum(page, Pages));
        setActiveLink(target);
      }
    });
    return qs(".container")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Error loading Component</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};
