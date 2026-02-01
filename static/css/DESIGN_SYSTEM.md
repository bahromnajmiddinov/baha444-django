# FlowHub Design System

A minimal, clean Todoist-style interface with support for light and dark theme modes.

## Features

✅ **Light and Dark Theme Variables** - Complete CSS variable system with consistent color schemes
✅ **Theme Switcher** - Toggle button in sidebar and settings page
✅ **Sidebar Navigation** - Clean, minimal navigation with task lists and tags
✅ **Minimal Design** - Clean component design throughout
✅ **Task Items** - Left-side priority accent bars
✅ **Badges & Tags** - Minimal styling
✅ **Forms** - Clean, simple input styling
✅ **Dashboard Cards** - Clear metric display
✅ **Quick Add Widget** - Fast task creation
✅ **Responsive** - Collapses sidebar on mobile
✅ **Smooth Transitions** - Subtle animations and transitions
✅ **User Preferences** - Theme settings persist in localStorage and server

## CSS Variables

### Colors
- `--primary` - Primary brand color
- `--primary-light` - Light variant for backgrounds
- `--secondary` - Secondary accent color
- `--success`, `--warning`, `--danger` - Status colors
- `--bg-primary`, `--bg-secondary`, `--bg-tertiary` - Background layers
- `--text-primary`, `--text-secondary`, `--text-muted` - Text hierarchy
- `--border`, `--border-hover` - Border colors

### Shadows
- `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-xl` - Consistent shadow scale

## Components

### Task Item
```html
<div class="task-item priority-high">
    <div class="task-checkbox">
        <input type="checkbox">
    </div>
    <div class="task-content">
        <h3 class="task-title">Task title</h3>
        <div class="task-meta">
            <!-- Badges and tags -->
        </div>
    </div>
    <div class="task-actions">
        <!-- Action buttons -->
    </div>
</div>
```

### Button
```html
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary Button</button>
<button class="btn btn-ghost">Ghost Button</button>
```

### Card
```html
<div class="card">
    <h3 class="card-title">Card Title</h3>
    <p>Card content</p>
</div>
```

### Badge
```html
<span class="badge">Default</span>
<span class="badge primary">Primary</span>
<span class="badge danger">Danger</span>
```

### Form
```html
<div class="form-group">
    <label class="form-label">Label</label>
    <input type="text" class="form-input">
</div>
```

## JavaScript API

### ThemeManager
```javascript
// Initialize theme system
ThemeManager.init();

// Set theme (light, dark, system)
ThemeManager.setTheme('dark');

// Toggle between light and dark
ThemeManager.toggle();
```

## Theme Implementation

Themes are defined with CSS variables and controlled by the `data-theme` attribute on the `<html>` element. The JavaScript API handles:

1. Loading saved theme from localStorage
2. Falling back to user profile theme
3. Falling back to system preference
4. Persisting theme changes to server
5. Listening for system preference changes

## Responsive Design

- Desktop: 260px sidebar + main content area
- Mobile: Sidebar hidden, accessible via toggle
- Fluid grid layout for dashboard cards
- Responsive typography and spacing

## Accessibility

- Focus-visible outlines for keyboard navigation
- Skip to main content link
- Proper contrast ratios
- Semantic HTML structure
- Reduced motion support
