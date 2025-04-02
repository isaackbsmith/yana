import { qs } from "../selectors";
import { ComponentProps } from "../types";
import { insertElement } from "../utils";


export default (props: ComponentProps): Element | undefined => {
  const cardBoxHTML = `
    <div class="cardBox">
      <div class="card1">
        <div class="queryheader">PERSONAL DETAILS</div>

        <div class="carddetails">
          <div class="query">name</div>
          <div class="cardName">Anna</div>
        </div>

        <div class="carddetails">
          <div class="query">blood</div>
          <div class="cardName">O+</div>
        </div>

        <div class="carddetails">
          <div class="query">height</div>
          <div class="cardName">4ft</div>
        </div>

        <div class="carddetails">
          <div class="query">weight</div>
          <div class="cardName">60kg</div>
        </div>
      </div>

      <div class="card">
        <div>
          <div class="numbers">20</div>
          <div class="cardName">number of Drugs</div>
        </div>

        <div class="iconBx">
          <ion-icon name="medkit-outline"></ion-icon>
        </div>
      </div>
    </div>
    `
  try {
    insertElement({ parent: props.parent, child: cardBoxHTML, position: "beforeend" });
    return qs(".cardBox")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Error loading Component</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};
