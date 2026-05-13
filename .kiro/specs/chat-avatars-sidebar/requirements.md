# Requirements Document: Chat Avatars in Sidebar

## Introduction

The Senger messenger application currently displays a commented-out sidebar in the chat interface with placeholder emoji (👤) instead of real user avatars. This feature aims to uncomment the sidebar, replace emoji placeholders with actual user avatar images, and add proper CSS styling to ensure avatars display correctly. The implementation will include fallback behavior for users without avatars and ensure the sidebar is visually consistent with the ICQ-style retro aesthetic.

## Glossary

- **System**: The Senger messenger application chat interface
- **Sidebar**: Right panel in chat window displaying active participants
- **Avatar**: User profile picture displayed in the sidebar
- **Current_User**: The logged-in user viewing the chat
- **Chat_User**: The other participant in the conversation
- **Fallback**: Default emoji (👤) displayed when avatar is unavailable
- **Avatar_Container**: HTML element that holds either an image or emoji
- **Object-fit**: CSS property controlling how images fill their container
- **Jinja2**: Template engine used for server-side rendering

## Requirements

### Requirement 1: Uncomment and Display Sidebar

**User Story:** As a user, I want to see the participants sidebar in the chat window, so that I can see who is in the conversation.

#### Acceptance Criteria

1. WHEN the System displays the chat window, THE System SHALL render the sidebar on the right side
2. WHEN the System renders the sidebar, THE System SHALL display a "Участники" (Participants) title bar
3. WHEN the System displays the sidebar, THE System SHALL show both the current user and the chat participant
4. WHEN the System displays the sidebar, THE System SHALL apply consistent window styling with the main chat area
5. WHEN the System displays the sidebar, THE System SHALL ensure it is visible and not hidden or commented out

### Requirement 2: Display Real User Avatars

**User Story:** As a user, I want to see real user avatars instead of emoji placeholders, so that I can quickly identify participants by their profile pictures.

#### Acceptance Criteria

1. WHEN the System displays a user in the sidebar, THE System SHALL check if the user has an avatar
2. WHEN a user has an avatar, THE System SHALL display the avatar image from the user.avatar path
3. WHEN the System displays the current user, THE System SHALL display current_user.avatar if available
4. WHEN the System displays the chat participant, THE System SHALL display user.avatar if available
5. WHEN the System renders an avatar image, THE System SHALL use the correct image source path (e.g., /static/avatars/...)
6. WHEN the System displays multiple avatars, THE System SHALL apply consistent sizing and styling

### Requirement 3: Implement Fallback to Emoji

**User Story:** As a user, I want to see a placeholder emoji when a user doesn't have an avatar, so that the interface remains complete and visually consistent.

#### Acceptance Criteria

1. WHEN a user does not have an avatar, THE System SHALL display the emoji 👤 as a fallback
2. WHEN the System displays a fallback emoji, THE System SHALL render it in the same container as an avatar image would be
3. WHEN the System displays a fallback emoji, THE System SHALL apply the same styling and sizing as avatar images
4. WHEN the System checks for avatar availability, THE System SHALL use Jinja2 conditional logic (if user.avatar)
5. WHEN the System renders the fallback, THE System SHALL ensure it is centered in the avatar container

### Requirement 4: Add CSS Styling for Avatar Images

**User Story:** As a developer, I want proper CSS styling for avatar images, so that they display correctly and consistently in the sidebar.

#### Acceptance Criteria

1. WHEN the System displays an avatar image, THE System SHALL apply width: 100% to fill the container
2. WHEN the System displays an avatar image, THE System SHALL apply height: 100% to fill the container
3. WHEN the System displays an avatar image, THE System SHALL apply object-fit: cover to maintain aspect ratio
4. WHEN the System displays an avatar image, THE System SHALL ensure the image fills the entire avatar container
5. WHEN the System displays an avatar image, THE System SHALL prevent image distortion or stretching
6. WHEN the System displays an avatar container, THE System SHALL maintain a square shape (50x50px)

### Requirement 5: Ensure Avatar Container Styling

**User Story:** As a user, I want avatar containers to be properly styled and visually distinct, so that they stand out in the sidebar.

#### Acceptance Criteria

1. WHEN the System displays an avatar container, THE System SHALL apply a 50px width and 50px height
2. WHEN the System displays an avatar container, THE System SHALL apply a 2px border with retro styling
3. WHEN the System displays an avatar container, THE System SHALL use border colors: #dfdfdf #0a0a0a #0a0a0a #dfdfdf
4. WHEN the System displays an avatar container, THE System SHALL apply a white background (#ffffff)
5. WHEN the System displays an avatar container, THE System SHALL center content (flexbox with align-items and justify-content)
6. WHEN the System displays an avatar container, THE System SHALL prevent shrinking (flex-shrink: 0)

### Requirement 6: Validate Sidebar Layout

**User Story:** As a user, I want the sidebar to display correctly with proper spacing and alignment, so that it looks professional and organized.

#### Acceptance Criteria

1. WHEN the System displays the sidebar, THE System SHALL apply consistent padding and spacing
2. WHEN the System displays profile sections, THE System SHALL apply 8px padding and gap between items
3. WHEN the System displays profile sections, THE System SHALL apply a bottom border (1px solid #dfdfdf)
4. WHEN the System displays the sidebar, THE System SHALL ensure proper overflow handling (overflow-y: auto)
5. WHEN the System displays the sidebar, THE System SHALL maintain a fixed width (200px)
6. WHEN the System displays profile information, THE System SHALL show username and status below the avatar

### Requirement 7: Implement Jinja2 Conditional Logic

**User Story:** As a developer, I want to use Jinja2 conditionals to check avatar availability, so that the template correctly handles both avatar and fallback cases.

#### Acceptance Criteria

1. WHEN the System renders the sidebar, THE System SHALL use {% if user.avatar %} to check for avatar
2. WHEN an avatar exists, THE System SHALL render <img src="{{ url_for('static', filename=user.avatar) }}" alt="...">
3. WHEN an avatar does not exist, THE System SHALL render the emoji 👤 as fallback
4. WHEN the System renders the current user, THE System SHALL apply the same conditional logic
5. WHEN the System renders the chat participant, THE System SHALL apply the same conditional logic
6. WHEN the System renders the template, THE System SHALL ensure proper Jinja2 syntax and escaping

### Requirement 8: Ensure Visual Consistency with ICQ Style

**User Story:** As a user, I want the sidebar to match the retro ICQ aesthetic, so that it feels cohesive with the rest of the interface.

#### Acceptance Criteria

1. WHEN the System displays the sidebar, THE System SHALL use the same background color (#c0c0c0) as other UI elements
2. WHEN the System displays profile sections, THE System SHALL apply the same border styling as other retro elements
3. WHEN the System displays text, THE System SHALL use the same font sizing and styling as other sidebar elements
4. WHEN the System displays the sidebar, THE System SHALL maintain consistent spacing with the main chat area
5. WHEN the System displays the sidebar, THE System SHALL apply the same window styling (title bar, borders) as the chat window

### Requirement 9: Handle Missing Avatar Paths

**User Story:** As a developer, I want the system to gracefully handle missing or invalid avatar paths, so that the interface doesn't break if avatar data is incomplete.

#### Acceptance Criteria

1. WHEN a user has an avatar field but it is empty or null, THE System SHALL display the fallback emoji
2. WHEN the System renders an avatar image, THE System SHALL include an alt attribute with the username
3. WHEN an image fails to load, THE System SHALL display the fallback emoji (via CSS or JavaScript)
4. WHEN the System checks avatar availability, THE System SHALL verify both the field existence and non-empty value
5. WHEN the System renders the template, THE System SHALL not throw errors for missing avatar data

### Requirement 10: Verify Sidebar Visibility and Responsiveness

**User Story:** As a user, I want the sidebar to be visible and properly positioned, so that I can see participants without scrolling or resizing.

#### Acceptance Criteria

1. WHEN the System displays the chat container, THE System SHALL render the sidebar with flex layout
2. WHEN the System displays the sidebar, THE System SHALL apply flex-shrink: 0 to prevent collapsing
3. WHEN the System displays the sidebar, THE System SHALL ensure it does not overflow the chat container
4. WHEN the System displays the sidebar, THE System SHALL apply max-height: calc(100vh - 180px) for proper scrolling
5. WHEN the System displays the sidebar, THE System SHALL maintain proper alignment with the main chat area
6. WHEN the System displays on different screen sizes, THE System SHALL ensure the sidebar remains visible and usable

