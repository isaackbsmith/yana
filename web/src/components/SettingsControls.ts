import { qs } from "../selectors";
import { ComponentProps } from "../types";
import { insertElement } from "../utils";


export default (props: ComponentProps): Element | undefined => {
  const settingsControlHTML = `
        <div class="settings-container">
          <div class="settings-card">
            <h2 class="settings-header">Account Settings</h2>
            <div class="profile-image-section">
              <img
                src="/api/placeholder/100/100"
                alt="Profile Picture"
                class="profile-image"
                id="profile-image"
              />
              <div>
                <input type="file" id="image-upload" accept="image/*" />
                <label for="image-upload" class="image-upload-btn"
                  >Upload New Image</label
                >
              </div>
            </div>
            <div class="settings-section">
              <h3>Personal Information</h3>
              <input
                type="text"
                class="settings-input"
                placeholder="Full Name"
                value="John Doe"
              />
              <input
                type="email"
                class="settings-input"
                placeholder="Email"
                value="john.doe@example.com"
              />
            </div>
            <div class="settings-section">
              <h3>Change Password</h3>
              <input
                type="password"
                class="settings-input"
                placeholder="Current Password"
              />
              <input
                type="password"
                class="settings-input"
                placeholder="New Password"
              />
              <input
                type="password"
                class="settings-input"
                placeholder="Confirm New Password"
              />
            </div>
          </div>

          <div class="settings-card">
            <h2 class="settings-header">Notification Settings</h2>
            <div class="settings-section">
              <h3>Email Notifications</h3>
              <label class="toggle-switch">
                <input type="checkbox" checked />
                <span class="slider"></span>
              </label>
            </div>
            <div class="settings-section">
              <h3>Push Notifications</h3>
              <label class="toggle-switch">
                <input type="checkbox" />
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="settings-card">
            <h2 class="settings-header">Privacy Settings</h2>
            <div class="settings-section">
              <h3>Profile Visibility</h3>
              <label class="toggle-switch">
                <input type="checkbox" checked />
                <span class="slider"></span>
              </label>
            </div>
            <div class="settings-section">
              <h3>Data Sharing</h3>
              <label class="toggle-switch">
                <input type="checkbox" />
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <button class="save-button">Save Changes</button>
        </div>
  `;
  insertElement({ parent: props.parent, child: settingsControlHTML, position: "beforeend" });
  return qs(".settings-container")!;
};
