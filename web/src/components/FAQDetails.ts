import { qs } from "../selectors";
import { ComponentProps } from "../types";
import { insertElement } from "../utils";


export default (props: ComponentProps): Element | undefined => {
  const faqDetailHTML = `
        <div class="faq-container">
          <h2 class="cardHeader">Frequently Asked Questions</h2>

          <div class="faq-item">
            <p class="faq-question">What is YANA?</p>
            <p class="faq-answer">
              YANA stands for "You Are Not Alone". It's a comprehensive health
              management platform designed to help you manage your medications,
              appointments, and overall health.
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">How do I add a new medication?</p>
            <p class="faq-answer">
              To add a new medication, go to the "Medication" page and use the
              "Prescription Manager" form. Fill in details like medication name,
              strength, dosage, frequency, and special instructions, then click
              "Add Medication".
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">Can I set reminders for my medications?</p>
            <p class="faq-answer">
              Yes, when you add a medication, you can set the start date, end
              date, and time for reminders. These will appear in your "Upcoming
              reminders" list.
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">How do I view my upcoming appointments?</p>
            <p class="faq-answer">
              You can view your upcoming appointments on the "Appointments"
              page. This page will show all your scheduled healthcare
              appointments.
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">What kind of analysis does YANA provide?</p>
            <p class="faq-answer">
              YANA provides health analytics on the "Analysis" page. This may
              include trends in your medication usage, appointment frequency,
              and other health-related data to give you insights into your
              overall health management.
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">How do I change my account settings?</p>
            <p class="faq-answer">
              You can change your account settings by clicking on the "Settings"
              option in the navigation menu. Here you can update your personal
              information, notification preferences, and other account-related
              settings.
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">Is my health information secure?</p>
            <p class="faq-answer">
              Yes, YANA takes your privacy seriously. We use industry-standard
              encryption and security measures to protect your personal and
              health information. Only you and the healthcare providers you
              authorize can access your data.
            </p>
          </div>

          <div class="faq-item">
            <p class="faq-question">
              How do I contact support if I have more questions?
            </p>
            <p class="faq-answer">
              If you have any questions that aren't answered here, please email
              our support team at support@yana.com or use the "Contact Us" form
              in the app. We're here to help!
            </p>
          </div>
        </div>
        `
  insertElement({ parent: props.parent, child: faqDetailHTML, position: "beforeend" });
  return qs(".faq-container")!
};
