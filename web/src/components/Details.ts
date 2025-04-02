import { ComponentProps } from "../types";
import { insertElement } from "../utils";

export default (props: ComponentProps): Element | undefined => {
  const detailsHTML = `
    <div class="details">
      <div class="recentOrders">
        <div class="cardHeader">
          <h2>prescribtion</h2>
          <div class="search">
            <label>
              <input type="text" placeholder="Search here" />
              <ion-icon name="search-outline"></ion-icon>
            </label>
          </div>
          <a href="#" class="btn">View All</a>
        </div>

        <table>
          <thead>
            <tr>
              <td>Name</td>
              <td>Dosage</td>
              <td>Daily Dosage</td>
              <td>Status</td>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status delivered">Dosage taken</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status pending">Pending</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status delivered">Dosage taken</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status delivered">Dosage taken</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status pending">Pending</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status pending">Pending</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status pending">Pending</span></td>
            </tr>

            <tr>
              <td>paracetamol</td>
              <td>2 tablets</td>
              <td>2 times dialy</td>
              <td><span class="status pending">Pending</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ================= New Customers ================ -->

      <div class="recentCustomers">
        <div class="cardHeader">
          <h2>Recent Caregivers</h2>
        </div>

        <table>
          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer02.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Daniella <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer01.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Ama <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer02.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Daniella <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer01.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Ama <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer02.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Daniella <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer01.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Ama <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer01.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Daniella <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>

          <tr>
            <td width="60px">
              <div class="imgBx">
                <img src="assets/imgs/customer02.jpeg" alt="" />
              </div>
            </td>
            <td>
              <h4>
                Ama <br />
                <span>Dance hosipital</span>
              </h4>
            </td>
          </tr>
        </table>
      </div>
    </div>
    `
};
