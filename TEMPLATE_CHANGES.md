# Template Changes for Design System Overhaul

This document outlines the template changes made for the FlowHub design system overhaul.

## New Files Created

### `/templates/core/settings.html`
New user settings page with theme selection. Users can choose between:
- Light theme
- Dark theme
- System (follows OS preference)

### `/templates/tasks/partials/quick_add.html`
Inline task creation widget for quick task entry without leaving the current page.

### `/templates/tasks/task_list_minimal.html`
Example minimal task list page demonstrating:
- Quick add widget
- Task item styling with priority accent bars
- Clean, simple layout

## Modified Files

### `/templates/base.html`
Major updates to implement the new design system:

**HTML Structure Changes:**
- Added `data-theme="light"` attribute to `<html>` element
- Added `<style>` block with CSS variables for light and dark themes
- Added base typography and card styles
- Completely redesigned sidebar:
  - New minimal layout with `sidebar-header` containing logo and theme toggle
  - Organized navigation sections (Main, Lists, Tags)
  - Added dynamic task lists and tags from context processor
  - Added create buttons for lists and tags
  - Clean `nav-link` styling with active states
  - Footer with settings link

**JavaScript Changes:**
- Added `ThemeManager` object for theme management
- Theme persistence in localStorage and sync to server
- System preference change detection
- Automatic theme application on page load

**Data Attributes:**
- `data-user-id` on body for authenticated users
- `data-csrftoken` on body for CSRF token access

### CSS (`/static/css/styles.css`)
Completely rewritten with new component system:

**New Components:**
- Sidebar navigation styling
- Task items with priority accent bars
- Badge system (primary, danger, success, warning)
- Tag badges with custom colors
- Button styles (primary, secondary, ghost, sizes)
- Form controls (inputs, textareas, selects)
- Dashboard cards
- Quick add widget
- Animations (fadeIn, slideUp)

**Responsive Design:**
- Mobile sidebar hiding at 768px breakpoint
- Fluid grid layouts
- Responsive spacing and typography

**Accessibility:**
- Focus-visible outlines
- Skip to main content link
- Reduced motion support

### Backend Changes

#### `/core/models.py`
Updated `UserProfile` model:
- Added `THEME_CHOICES` constant with options for light, dark, system
- Updated `theme` field to use choices with 10 character max
- Added default value of 'light'

#### `/core/views.py`
New views added:
- `settings_view`: Renders settings page and handles theme updates
- `set_theme`: API endpoint for AJAX theme updates

#### `/core/urls.py`
New URL patterns:
- `/settings/` - Settings page
- `/api/theme/` - Theme API endpoint

#### `/core/context_processors.py` (NEW)
New context processor to inject task lists and tags into all templates:
- `user_task_lists`: User's non-archived task lists ordered by position
- `user_tags`: User's first 10 tags ordered newest first

#### `/config/settings.py`
Added `'core.context_processors.user_task_context'` to template context processors.

## Default Theme

The system defaults to light theme on first visit. When a user:
1. Toggles theme via sidebar button - saves to localStorage and server
2. Selects theme in settings - saves to server and applies immediately
3. Returns to site - loads from localStorage, falls back to profile theme, falls back to system preference

## Browser Support

- Modern browsers with CSS custom property support
- System theme preference detection via `prefers-color-scheme`
- Graceful degradation for older browsers (defaults to light theme)

## Migration Notes

The database migration updates the `theme` field in the `UserProfile` model. Run:

```bash
python manage.py migrate
```

This will add the new field constraints and update existing records to use 'light' as default.
