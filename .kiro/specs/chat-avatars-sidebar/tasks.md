# Implementation Plan: Chat Avatars in Sidebar

## Overview

This implementation plan converts the feature design into a series of actionable coding tasks. The feature uncomments the chat sidebar, replaces emoji placeholders with real user avatars, and adds proper CSS styling. Each task builds incrementally on previous steps, ensuring the sidebar displays correctly with avatar images and graceful fallback to emoji when avatars are unavailable.

## Implementation Language

**Python** (Flask backend with Jinja2 templates and CSS styling)

---

## Tasks

### Phase 1: Uncomment and Prepare Sidebar Structure

- [x] 1. Uncomment the sidebar HTML block in chat template
  - Open `templates/old/chat.html`
  - Locate the commented-out `<div class="chat-sidebar">` block (lines ~35-60)
  - Uncomment the entire sidebar section including the window frame, title bar, and profiles container
  - Verify the HTML structure is intact and properly indented
  - Ensure the closing `</div>` tags match the opening tags
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 2. Verify sidebar HTML structure and layout
  - Check that `.chat-sidebar` div is a direct child of `.chat-container`
  - Verify `.window` div is properly nested inside `.chat-sidebar`
  - Confirm `.title-bar` contains "Участники" text
  - Verify `.window-body` has `style="padding: 0;"`
  - Check that `.profiles-container` is properly nested
  - Ensure two `.profile-section` divs exist (one for current user, one for chat participant)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

### Phase 2: Replace Emoji with Conditional Avatar Logic for Current User

- [x] 3. Replace first profile-avatar emoji with Jinja2 conditional for current_user
  - Open `templates/old/chat.html`
  - Locate the first `.profile-avatar` div (for current user)
  - Replace the hardcoded `👤` emoji with:
    ```html
    {% if current_user.avatar %}
        <img src="{{ url_for('static', filename=current_user.avatar) }}" alt="{{ current_user.username }}">
    {% else %}
        👤
    {% endif %}
    ```
  - Verify the Jinja2 syntax is correct (proper indentation and closing tags)
  - Ensure `url_for()` function is used for dynamic path generation
  - Check that `alt` attribute contains the username for accessibility
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 7.1, 7.2, 7.3, 7.4, 9.1, 9.2_

- [x] 4. Verify current_user avatar conditional logic
  - Check that the Jinja2 condition `{% if current_user.avatar %}` is correct
  - Verify the image source path uses `url_for('static', filename=current_user.avatar)`
  - Confirm the fallback emoji `👤` is displayed when avatar is None or empty
  - Test that the template renders without Jinja2 errors
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 7.1, 7.2, 7.3, 7.4_

### Phase 3: Replace Emoji with Conditional Avatar Logic for Chat Participant

- [x] 5. Replace second profile-avatar emoji with Jinja2 conditional for user
  - Open `templates/old/chat.html`
  - Locate the second `.profile-avatar` div (for chat participant)
  - Replace the hardcoded `👤` emoji with:
    ```html
    {% if user.avatar %}
        <img src="{{ url_for('static', filename=user.avatar) }}" alt="{{ user.username }}">
    {% else %}
        👤
    {% endif %}
    ```
  - Verify the Jinja2 syntax is correct (proper indentation and closing tags)
  - Ensure `url_for()` function is used for dynamic path generation
  - Check that `alt` attribute contains the username for accessibility
  - _Requirements: 2.1, 2.2, 2.4, 3.1, 3.2, 3.3, 7.1, 7.2, 7.3, 7.5, 9.1, 9.2_

- [x] 6. Verify chat participant avatar conditional logic
  - Check that the Jinja2 condition `{% if user.avatar %}` is correct
  - Verify the image source path uses `url_for('static', filename=user.avatar)`
  - Confirm the fallback emoji `👤` is displayed when avatar is None or empty
  - Test that the template renders without Jinja2 errors
  - _Requirements: 2.1, 2.2, 2.4, 3.1, 3.2, 3.3, 7.1, 7.2, 7.3, 7.5_

### Phase 4: Add CSS Styling for Avatar Images

- [x] 7. Add CSS rule for avatar images in chat.css
  - Open `static/old/chat.css`
  - Add the following CSS rule after the `.profile-avatar` rule:
    ```css
    .profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    ```
  - Verify the CSS syntax is correct (proper braces and semicolons)
  - Ensure the rule is placed in the correct location (after `.profile-avatar` definition)
  - Check that the file is saved properly
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 8. Verify avatar container styling is correct
  - Check that `.profile-avatar` has `width: 50px` and `height: 50px`
  - Verify `.profile-avatar` has `border: 2px solid` with correct colors
  - Confirm `.profile-avatar` has `background: #ffffff`
  - Check that `.profile-avatar` uses `display: flex` with `align-items: center` and `justify-content: center`
  - Verify `.profile-avatar` has `flex-shrink: 0`
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

### Phase 5: Verify Profile Section Layout and Styling

- [x] 9. Verify profile section layout and spacing
  - Check that `.profile-section` has `display: flex` and `align-items: center`
  - Verify `.profile-section` has `gap: 8px` between avatar and info
  - Confirm `.profile-section` has `padding: 8px`
  - Check that `.profile-section` has `border-bottom: 1px solid #dfdfdf`
  - Verify `.profile-section` has `background: #c0c0c0`
  - Confirm `.profile-section` has `cursor: pointer` and `transition: background-color 0.2s`
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [x] 10. Verify profile info and text styling
  - Check that `.profile-info` has `flex: 1` and `min-width: 0`
  - Verify `.profile-name` has `font-weight: bold` and `font-size: 10px`
  - Confirm `.profile-status` has `font-size: 9px` and `opacity: 0.7`
  - Check that text wrapping is handled correctly with `word-break: break-word`
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

### Phase 6: Verify Sidebar Container and Window Styling

- [x] 11. Verify sidebar container styling
  - Check that `.chat-sidebar` has `width: 200px`
  - Verify `.chat-sidebar` has `flex-shrink: 0`
  - Confirm `.chat-sidebar` has `overflow: hidden`
  - Check that `.chat-sidebar .window` has `max-height: calc(100vh - 180px)`
  - Verify `.chat-sidebar .window` has `overflow-y: auto`
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [x] 12. Verify visual consistency with ICQ style
  - Check that `.profiles-container` has `background: #c0c0c0`
  - Verify all profile sections use the same background color
  - Confirm border colors match the retro style (#dfdfdf and #0a0a0a)
  - Check that font sizing is consistent (10px for names, 9px for status)
  - Verify spacing and padding are consistent throughout
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

### Phase 7: Test Avatar Rendering and Fallback

- [ ] 13. Test avatar image rendering with real user data
  - Verify that users with avatars display images correctly
  - Check that image paths are generated correctly by `url_for()`
  - Confirm images are displayed at 50x50px size
  - Verify images maintain aspect ratio with `object-fit: cover`
  - Check that images are centered in the container
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [ ] 14. Test emoji fallback for users without avatars
  - Verify that users without avatars display the 👤 emoji
  - Check that emoji is centered in the container
  - Confirm emoji is displayed at the correct size (28px)
  - Verify emoji fallback works for both current user and chat participant
  - Check that fallback emoji has the same styling as avatar containers
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 15. Test empty and null avatar field handling
  - Verify that `avatar = None` displays emoji fallback
  - Check that `avatar = ""` (empty string) displays emoji fallback
  - Confirm that Jinja2 conditionals correctly evaluate falsy values
  - Test that no errors are thrown for missing avatar data
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

### Phase 8: Test Sidebar Visibility and Layout

- [ ] 16. Test sidebar visibility and positioning
  - Verify that sidebar is visible on the right side of the chat window
  - Check that sidebar is not hidden or commented out
  - Confirm sidebar is properly positioned with flexbox layout
  - Verify sidebar does not collapse (flex-shrink: 0)
  - Check that sidebar maintains proper alignment with main chat area
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [ ] 17. Test sidebar scrolling and overflow handling
  - Verify that sidebar scrolls when content exceeds max-height
  - Check that max-height is calculated correctly (100vh - 180px)
  - Confirm overflow-y: auto is applied
  - Test scrolling behavior with multiple participants
  - _Requirements: 6.4, 10.3, 10.4_

- [ ] 18. Test sidebar responsiveness on different screen sizes
  - Verify sidebar remains visible on desktop (1920x1080)
  - Check sidebar behavior on tablet (768x1024)
  - Test sidebar on mobile (375x667)
  - Confirm sidebar maintains proper layout and doesn't overflow
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

### Phase 9: Test Accessibility and Alt Attributes

- [ ] 19. Test alt attributes for avatar images
  - Verify that all avatar images have alt attributes
  - Check that alt text contains the username
  - Confirm alt text is displayed when image fails to load
  - Test screen reader compatibility with alt attributes
  - _Requirements: 9.2, 9.3_

- [ ] 20. Test accessibility of sidebar structure
  - Verify that sidebar has proper semantic HTML
  - Check that title bar is properly labeled ("Участники")
  - Confirm profile sections are properly structured
  - Test keyboard navigation (if applicable)
  - _Requirements: 1.2, 1.3, 1.4, 1.5_

### Phase 10: Final Verification and Testing

- [x] 21. Checkpoint - Verify all HTML changes are correct
  - Ensure sidebar is uncommented and visible
  - Verify both profile sections are present
  - Check that Jinja2 conditionals are properly formatted
  - Confirm all closing tags match opening tags
  - Test that template renders without errors
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 22. Checkpoint - Verify all CSS changes are correct
  - Ensure `.profile-avatar img` rule is added
  - Verify all existing avatar container styles are intact
  - Check that CSS syntax is correct
  - Confirm no CSS errors in browser console
  - Test that styles are applied correctly
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 23. Checkpoint - Test complete feature end-to-end
  - Load chat page with two users
  - Verify sidebar displays on the right side
  - Check that current user profile is displayed
  - Verify chat participant profile is displayed
  - Confirm avatars display correctly (if present)
  - Verify emoji fallback displays (if no avatar)
  - Check that no console errors appear
  - Test that sidebar scrolls if needed
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 8.1, 8.2, 8.3, 8.4, 8.5, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [x] 24. Checkpoint - Verify visual consistency and styling
  - Check that sidebar matches retro ICQ aesthetic
  - Verify background colors are consistent (#c0c0c0)
  - Confirm border styling matches other UI elements
  - Check that font sizing is consistent
  - Verify spacing and padding are uniform
  - Test that hover effects work on profile sections
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

---

## Task Dependencies

- Tasks 1-2 must be completed before tasks 3-6 (sidebar must be uncommented first)
- Tasks 3-6 must be completed before tasks 13-15 (avatar logic must be in place before testing)
- Tasks 7-12 must be completed before tasks 13-15 (CSS must be added before testing rendering)
- Tasks 13-20 can be completed in parallel after tasks 1-12
- Tasks 21-24 are final checkpoints and must be completed last

## Files Modified

1. `templates/old/chat.html` - Uncomment sidebar, add Jinja2 conditionals for avatars
2. `static/old/chat.css` - Add `.profile-avatar img` CSS rule

## Success Criteria

- [ ] Sidebar is uncommented and visible in chat interface
- [ ] Both current user and chat participant profiles are displayed
- [ ] Avatar images display correctly for users with avatars
- [ ] Emoji fallback (👤) displays for users without avatars
- [ ] CSS styling is applied correctly (50x50px, object-fit: cover, etc.)
- [ ] Sidebar maintains retro ICQ aesthetic
- [ ] No console errors or warnings
- [ ] Sidebar scrolls properly when content exceeds max-height
- [ ] Alt attributes are present on all avatar images
- [ ] Feature works on different screen sizes

## Notes

- All tasks are mandatory (no optional sub-tasks)
- Each task builds on previous steps
- Testing tasks (13-20) validate the implementation
- Checkpoint tasks (21-24) ensure quality before completion
- The implementation uses existing Flask/Jinja2 infrastructure
- No new dependencies are required
- Avatar files are stored in `static/avatars/` directory
- User model must have `avatar` field (assumed to exist based on design)

