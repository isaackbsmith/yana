import { qs } from "../selectors";
import { ComponentProps } from "../types";
import { insertElement, toggleSideNav } from "../utils";


export default (props: ComponentProps): Element | undefined => {
  const headerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="toggle">
        <ion-icon name="menu-outline"></ion-icon>
      </div>

      <div class="search">
        <label>
          <input type="text" placeholder="Search here" />
          <ion-icon name="search-outline"></ion-icon>
        </label>
      </div>

      <div class="user">
        <img src="assets/imgs/customer01.jpeg" alt="" />
      </div>
    </div>
`
  insertElement({ parent: props.parent, child: headerHTML, position: "afterbegin" });

  toggleSideNav();

  return qs(".topbar")!
};

