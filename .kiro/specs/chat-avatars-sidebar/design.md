# Design Document: Chat Avatars in Sidebar

## Overview

This design document describes the implementation of real user avatars in the chat sidebar for the Senger messenger application. The feature replaces placeholder emoji (👤) with actual user profile pictures while maintaining the retro ICQ-style aesthetic. The implementation uses Jinja2 template conditionals to check avatar availability and provides a graceful fallback to emoji when avatars are unavailable.

### Key Design Goals

1. **Visual Consistency**: Maintain the retro ICQ aesthetic with proper border styling and color scheme
2. **Robustness**: Handle missing or invalid avatar data gracefully
3. **Performance**: Use efficient CSS and minimal JavaScript
4. **Accessibility**: Include proper alt attributes and semantic HTML
5. **Maintainability**: Clear separation of concerns between template logic, styling, and data

---

## Architecture

### Component Hierarchy

```
chat-container (flex layout)
├── chat-main (main chat area)
│   └── window (retro window frame)
│       ├── title-bar
│       └── window-body
│           ├── messages-list
│           └── input-area
└── chat-sidebar (NEW - uncommented)
    └── window (retro window frame)
        ├── title-bar ("Участники")
        └── window-body
            └── profiles-container
                ├── profile-section (current user)
                │   ├── profile-avatar (with conditional image/emoji)
                │   └── profile-info
                └── profile-section (chat participant)
                    ├── profile-avatar (with conditional image/emoji)
                    └── profile-info
```

### Data Flow

```
User Model (avatar field)
    ↓
Jinja2 Template ({% if user.avatar %})
    ↓
Conditional Rendering
    ├─→ Avatar Image: <img src="{{ url_for(...) }}">
    └─→ Fallback Emoji: 👤
    ↓
CSS Styling (.profile-avatar img)
    ↓
Rendered Output
```

---

## Components and Interfaces

### 1. Sidebar Container (`.chat-sidebar`)

**Purpose**: Main container for the participants sidebar

**Properties**:
- `width: 200px` - Fixed width for consistent layout
- `flex-shrink: 0` - Prevents sidebar from collapsing
- `overflow: hidden` - Prevents content overflow

**Responsibilities**:
- Provides flex container for the window component
- Maintains fixed width in the chat layout
- Handles overflow behavior

### 2. Sidebar Window (`.chat-sidebar .window`)

**Purpose**: Retro-styled window frame for the sidebar

**Properties**:
- `max-height: calc(100vh - 180px)` - Responsive height calculation
- `overflow-y: auto` - Vertical scrolling for many participants
- Inherits window styling from base CSS

**Responsibilities**:
- Provides scrollable container for participant list
- Maintains retro window appearance
- Adapts to viewport height

### 3. Profiles Container (`.profiles-container`)

**Purpose**: Flex container for profile sections

**Properties**:
- `display: flex`
- `flex-direction: column`
- `gap: 0` - No gap between items
- `padding: 0` - No padding
- `background: #c0c0c0` - Retro gray background

**Responsibilities**:
- Arranges profile sections vertically
- Maintains consistent background color
- Provides flex context for child items

### 4. Profile Section (`.profile-section`)

**Purpose**: Individual participant entry in the sidebar

**Properties**:
- `display: flex`
- `align-items: center`
- `gap: 8px` - Space between avatar and info
- `padding: 8px` - Internal spacing
- `border-bottom: 1px solid #dfdfdf` - Separator line
- `background: #c0c0c0` - Retro gray
- `cursor: pointer` - Interactive feedback
- `transition: background-color 0.2s` - Smooth hover effect

**Responsibilities**:
- Displays single participant with avatar and info
- Provides visual separation between participants
- Supports hover interaction

### 5. Profile Avatar Container (`.profile-avatar`)

**Purpose**: Container for avatar image or fallback emoji

**Properties**:
- `width: 50px` - Fixed square size
- `height: 50px` - Fixed square size
- `border: 2px solid` - Retro border
- `border-color: #dfdfdf #0a0a0a #0a0a0a #dfdfdf` - 3D effect
- `background: #ffffff` - White background
- `display: flex` - Flex container
- `align-items: center` - Vertical centering
- `justify-content: center` - Horizontal centering
- `font-size: 28px` - Emoji size
- `flex-shrink: 0` - Prevents shrinking

**Responsibilities**:
- Provides fixed-size container for avatar
- Centers content (image or emoji)
- Applies retro styling
- Prevents layout shifts

### 6. Profile Avatar Image (`.profile-avatar img`)

**Purpose**: Actual user avatar image

**Properties**:
- `width: 100%` - Fills container width
- `height: 100%` - Fills container height
- `object-fit: cover` - Maintains aspect ratio, crops if needed

**Responsibilities**:
- Displays user avatar image
- Maintains aspect ratio
- Fills entire container without distortion

### 7. Profile Info (`.profile-info`)

**Purpose**: Container for username and status

**Properties**:
- `flex: 1` - Takes remaining space
- `min-width: 0` - Allows text truncation
- `overflow-wrap: break-word` - Wraps long usernames

**Responsibilities**:
- Displays user information
- Handles text overflow gracefully
- Provides flexible layout

### 8. Profile Name (`.profile-name`)

**Purpose**: Username display

**Properties**:
- `font-weight: bold` - Emphasis
- `font-size: 10px` - Small retro font
- `word-break: break-word` - Breaks long names
- `margin-bottom: 4px` - Space before status

**Responsibilities**:
- Displays username
- Handles long usernames
- Maintains retro typography

### 9. Profile Status (`.profile-status`)

**Purpose**: User status indicator

**Properties**:
- `font-size: 9px` - Smaller than username
- `opacity: 0.7` - Subtle appearance

**Responsibilities**:
- Displays user status (e.g., "Online")
- Provides secondary information
- Maintains visual hierarchy

---

## Data Models

### User Model

```python
class User(SqlAlchemyBase, UserMixin):
    id: int                    # Primary key
    username: str              # Unique username
    avatar: str | None         # Path to avatar image (nullable)
    # ... other fields
```

**Avatar Field**:
- **Type**: `String` (nullable)
- **Default**: `None`
- **Format**: Relative path like `"avatars/user_1_1f526482.webp"`
- **Storage**: Files stored in `static/avatars/` directory

### Template Context

```python
{
    'current_user': User,      # Logged-in user
    'user': User,              # Chat participant
    'chat_id': int,            # Chat identifier
    'messages': List[Message]  # Message history
}
```

---

## HTML Structure

### Sidebar Template (Uncommented)

```html
<div class="chat-sidebar">
    <div class="window">
        <div class="title-bar">
            <div class="title-bar-text">Участники</div>
            <div class="title-bar-controls">
                <button aria-label="Close"></button>
            </div>
        </div>

        <div class="window-body" style="padding: 0;">
            <div class="profiles-container">
                <!-- Current User Profile -->
                <div class="profile-section">
                    <div class="profile-avatar">
                        {% if current_user.avatar %}
                            <img src="{{ url_for('static', filename=current_user.avatar) }}" 
                                 alt="{{ current_user.username }}">
                        {% else %}
                            👤
                        {% endif %}
                    </div>
                    <div class="profile-info">
                        <div class="profile-name">{{ current_user.username }}</div>
                        <div class="profile-status">Online</div>
                    </div>
                </div>

                <!-- Chat Participant Profile -->
                <div class="profile-section">
                    <div class="profile-avatar">
                        {% if user.avatar %}
                            <img src="{{ url_for('static', filename=user.avatar) }}" 
                                 alt="{{ user.username }}">
                        {% else %}
                            👤
                        {% endif %}
                    </div>
                    <div class="profile-info">
                        <div class="profile-name">{{ user.username }}</div>
                        <div class="profile-status">Online</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Key Template Features

1. **Conditional Avatar Rendering**:
   - `{% if current_user.avatar %}` - Checks if avatar exists
   - `{{ url_for('static', filename=current_user.avatar) }}` - Generates correct path
   - Fallback to `👤` emoji if no avatar

2. **Alt Attributes**:
   - `alt="{{ current_user.username }}"` - Accessibility and fallback text
   - Helps screen readers identify users

3. **Jinja2 Syntax**:
   - Uses Flask's `url_for()` for dynamic path generation
   - Ensures paths work regardless of deployment configuration

---

## CSS Styling

### Avatar Image Styling

```css
.profile-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
```

**Explanation**:
- `width: 100%` - Image fills container width
- `height: 100%` - Image fills container height
- `object-fit: cover` - Maintains aspect ratio while filling container
  - Crops image if necessary
  - Prevents distortion or stretching
  - Centers image within container

### Avatar Container Styling (Existing)

```css
.profile-avatar {
    width: 50px;
    height: 50px;
    border: 2px solid;
    border-color: #dfdfdf #0a0a0a #0a0a0a #dfdfdf;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    flex-shrink: 0;
}
```

**Explanation**:
- `width: 50px; height: 50px;` - Fixed square container
- `border: 2px solid; border-color: #dfdfdf #0a0a0a #0a0a0a #dfdfdf;` - 3D retro effect
  - Top/left: light (#dfdfdf)
  - Bottom/right: dark (#0a0a0a)
  - Creates beveled appearance
- `background: #ffffff;` - White background for emoji fallback
- `display: flex; align-items: center; justify-content: center;` - Centers content
- `font-size: 28px;` - Emoji size
- `flex-shrink: 0;` - Prevents container from shrinking

### Profile Section Styling (Existing)

```css
.profile-section {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    border-bottom: 1px solid #dfdfdf;
    background: #c0c0c0;
    cursor: pointer;
    transition: background-color 0.2s;
}
```

**Explanation**:
- `display: flex; align-items: center;` - Horizontal layout with vertical centering
- `gap: 8px;` - Space between avatar and info
- `padding: 8px;` - Internal spacing
- `border-bottom: 1px solid #dfdfdf;` - Separator between profiles
- `background: #c0c0c0;` - Retro gray (matches window background)
- `cursor: pointer;` - Interactive feedback
- `transition: background-color 0.2s;` - Smooth hover effect

---

## Fallback Mechanism

### Avatar Availability Check

The system uses Jinja2 conditionals to check avatar availability:

```html
{% if current_user.avatar %}
    <!-- Display image -->
{% else %}
    <!-- Display emoji -->
{% endif %}
```

### Fallback Scenarios

1. **Avatar Field is None**:
   - Database stores `NULL` for avatar
   - Jinja2 condition evaluates to `False`
   - Emoji fallback displayed

2. **Avatar Field is Empty String**:
   - Database stores `""` for avatar
   - Jinja2 condition evaluates to `False`
   - Emoji fallback displayed

3. **Avatar File Missing**:
   - File path is invalid or file deleted
   - Browser displays alt text or broken image
   - CSS can hide broken images with `display: none` if needed
   - Emoji fallback provides visual consistency

### Fallback Styling

The emoji fallback uses the same container styling:
- Same 50x50px size
- Same border and background
- Same centering (flexbox)
- Font size: 28px for readable emoji

---

## Error Handling

### Missing Avatar Data

**Scenario**: User record has `avatar = None`

**Handling**:
```html
{% if current_user.avatar %}
    <!-- Image rendered -->
{% else %}
    <!-- Emoji displayed -->
{% endif %}
```

**Result**: Graceful fallback to emoji, no errors

### Invalid Avatar Path

**Scenario**: `avatar` field contains invalid path

**Handling**:
1. `url_for()` generates path as-is
2. Browser attempts to load image
3. Image fails to load (404 or similar)
4. Browser displays alt text
5. User sees broken image icon or alt text

**Improvement** (optional):
```html
<img src="{{ url_for('static', filename=current_user.avatar) }}" 
     alt="{{ current_user.username }}"
     onerror="this.style.display='none'">
```

This hides broken images, but emoji fallback is already in place via Jinja2.

### Empty Avatar Field

**Scenario**: `avatar = ""`

**Handling**:
```html
{% if current_user.avatar %}  <!-- Empty string is falsy -->
    <!-- Not rendered -->
{% else %}
    <!-- Emoji displayed -->
{% endif %}
```

**Result**: Emoji fallback displayed

---

## Testing Strategy

### Unit Tests

#### Test 1: Avatar Image Rendering
- **Scenario**: User has avatar path
- **Setup**: Create user with `avatar = "avatars/user_1_1f526482.webp"`
- **Action**: Render template
- **Assertion**: HTML contains `<img src="/static/avatars/user_1_1f526482.webp">`

#### Test 2: Emoji Fallback
- **Scenario**: User has no avatar
- **Setup**: Create user with `avatar = None`
- **Action**: Render template
- **Assertion**: HTML contains `👤` emoji, no `<img>` tag

#### Test 3: Empty Avatar Field
- **Scenario**: User has empty avatar field
- **Setup**: Create user with `avatar = ""`
- **Action**: Render template
- **Assertion**: HTML contains `👤` emoji

#### Test 4: Alt Attribute
- **Scenario**: Avatar image has alt text
- **Setup**: Create user with avatar and username
- **Action**: Render template
- **Assertion**: `<img>` tag contains `alt="username"`

#### Test 5: CSS Styling
- **Scenario**: Avatar container has correct styles
- **Setup**: Inspect `.profile-avatar` element
- **Assertion**: 
  - Width: 50px
  - Height: 50px
  - Border: 2px solid
  - Background: #ffffff
  - Display: flex

#### Test 6: Image Sizing
- **Scenario**: Avatar image fills container
- **Setup**: Render avatar with image
- **Assertion**:
  - `.profile-avatar img` has `width: 100%`
  - `.profile-avatar img` has `height: 100%`
  - `.profile-avatar img` has `object-fit: cover`

#### Test 7: Sidebar Visibility
- **Scenario**: Sidebar is visible and not commented
- **Setup**: Render chat template
- **Assertion**: `.chat-sidebar` element exists and is visible

#### Test 8: Both Profiles Displayed
- **Scenario**: Both current user and chat participant shown
- **Setup**: Render template with two users
- **Assertion**: Two `.profile-section` elements present

### Integration Tests

#### Test 1: Full Sidebar Rendering
- **Scenario**: Complete sidebar with both users
- **Setup**: Load chat page with two users
- **Assertion**: Sidebar visible with both profiles

#### Test 2: Avatar Loading
- **Scenario**: Avatar images load correctly
- **Setup**: Load chat page with avatar files present
- **Assertion**: Images display without errors

#### Test 3: Responsive Layout
- **Scenario**: Sidebar maintains layout on different screen sizes
- **Setup**: Resize viewport
- **Assertion**: Sidebar remains visible and properly positioned

### Manual Testing Checklist

- [ ] Sidebar uncommented and visible
- [ ] Current user profile displayed
- [ ] Chat participant profile displayed
- [ ] Avatar images display correctly (if present)
- [ ] Emoji fallback displays (if no avatar)
- [ ] Sidebar scrolls if content exceeds max-height
- [ ] Retro styling consistent with main chat area
- [ ] Text doesn't overflow profile-info container
- [ ] Avatar containers are square (50x50px)
- [ ] Borders have 3D effect
- [ ] Hover effect works on profile sections
- [ ] Alt text visible when image fails to load

---

## Visual Consistency

### Retro ICQ Aesthetic

The sidebar maintains consistency with the main chat area:

1. **Color Scheme**:
   - Background: `#c0c0c0` (retro gray)
   - Borders: `#dfdfdf` (light) and `#0a0a0a` (dark)
   - Text: `#000000` (black)

2. **Border Styling**:
   - 2px solid borders
   - 3D effect: light top/left, dark bottom/right
   - Matches window frame styling

3. **Typography**:
   - Font: 'MS Sans Serif', Arial, sans-serif
   - Username: 10px, bold
   - Status: 9px, 70% opacity

4. **Spacing**:
   - Profile sections: 8px padding
   - Gap between avatar and info: 8px
   - Separator: 1px border-bottom

5. **Interactive Elements**:
   - Cursor: pointer on hover
   - Transition: smooth 0.2s background-color change

---

## Implementation Checklist

- [ ] Uncomment `.chat-sidebar` block in `templates/old/chat.html`
- [ ] Replace emoji with Jinja2 conditionals for current user
- [ ] Replace emoji with Jinja2 conditionals for chat participant
- [ ] Add `.profile-avatar img` CSS rule to `static/old/chat.css`
- [ ] Verify `.profile-avatar` has correct dimensions (50x50px)
- [ ] Verify flexbox centering in `.profile-avatar`
- [ ] Test avatar rendering with real user data
- [ ] Test emoji fallback with users without avatars
- [ ] Verify sidebar visibility and layout
- [ ] Test responsive behavior
- [ ] Verify retro styling consistency
- [ ] Test alt attributes for accessibility
- [ ] Verify no console errors

---

## Future Enhancements

1. **Dynamic Status**: Replace hardcoded "Online" with actual user status
2. **Click Handlers**: Add JavaScript to handle profile section clicks
3. **Hover Effects**: Add visual feedback on hover (e.g., highlight)
4. **Avatar Upload**: Allow users to upload custom avatars
5. **Lazy Loading**: Implement lazy loading for avatar images
6. **Caching**: Add cache headers for avatar images
7. **Responsive Sidebar**: Collapse sidebar on mobile devices
8. **User Presence**: Show online/offline indicator with color coding

---

## References

- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)
- [Flask url_for()](https://flask.palletsprojects.com/en/latest/api/#flask.url_for)
- [CSS object-fit Property](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit)
- [Flexbox Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)
- [ICQ Retro UI Design](https://en.wikipedia.org/wiki/ICQ)
