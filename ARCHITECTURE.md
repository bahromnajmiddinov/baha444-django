# FlowHub Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FlowHub                               │
│                   Productivity Platform                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │     │   Backend    │     │   Database   │
│              │     │              │     │              │
│  - HTML/CSS  │────▶│   Django     │────▶│   SQLite     │
│  - HTMX      │     │   Python     │     │   PostgreSQL │
│  - JavaScript│     │   Views      │     │   (optional) │
└──────────────┘     └──────────────┘     └──────────────┘
```

## 📦 Application Structure

### Core Apps

```
productivity_hub/
│
├── 🏠 core/              Dashboard & Authentication
│   ├── Dashboard view with stats
│   ├── User authentication
│   └── Profile management
│
├── ✅ tasks/             Task Management System
│   ├── List view
│   ├── Kanban board
│   ├── Calendar view
│   ├── Task CRUD operations
│   └── Attachments & comments
│
├── 🔥 habits/            Habit Tracking
│   ├── Habit creation
│   ├── Daily completion
│   ├── Streak tracking
│   └── Statistics
│
├── ⏱️ pomodoro/          Focus Timer
│   ├── Timer interface
│   ├── Session management
│   ├── Break scheduling
│   └── History tracking
│
├── 💰 finance/           Personal Finance
│   ├── Account management
│   ├── Transaction tracking
│   ├── Budget creation
│   ├── Category management
│   └── Financial reports
│
├── 📝 notes/             Notes & Ideas
│   ├── Note editor
│   ├── Folder organization
│   ├── Tag system
│   ├── Ideas tracker
│   └── Reminders
│
└── 📊 tracker/           Daily Tracking
    ├── Mood logging
    ├── Daily entries
    ├── Custom metrics
    └── Journaling
```

## 🗄️ Database Schema

### Core Models

```sql
-- User Profile
UserProfile
├── user (FK → User)
├── avatar
├── timezone
├── theme
└── google_tokens

-- Tasks
Task
├── user (FK → User)
├── title
├── description
├── status (pitched/in_progress/completed/paid)
├── priority (low/medium/high)
├── due_date
├── completed_date
└── position

TaskAttachment
├── task (FK → Task)
├── file
└── filename

TaskComment
├── task (FK → Task)
├── user (FK → User)
├── content
└── created_at

-- Habits
Habit
├── user (FK → User)
├── name
├── description
├── icon
├── color
├── frequency
└── is_active

HabitCompletion
├── habit (FK → Habit)
├── date
└── notes

-- Pomodoro
PomodoroSession
├── user (FK → User)
├── session_type
├── duration_minutes
├── completed_minutes
├── task (FK → Task, optional)
└── started_at

PomodoroSettings
├── user (FK → User)
├── focus_duration
├── short_break_duration
├── long_break_duration
└── auto_start options

-- Finance
Account
├── user (FK → User)
├── name
├── account_type
├── balance
└── currency

Category
├── user (FK → User)
├── name
├── category_type (income/expense)
├── icon
├── color
└── budget_limit

Transaction
├── user (FK → User)
├── account (FK → Account)
├── category (FK → Category)
├── amount
├── description
└── date

Budget
├── user (FK → User)
├── category (FK → Category)
├── amount
└── month

-- Notes
Note
├── user (FK → User)
├── title
├── content
├── folder (FK → Folder)
├── tags (M2M → Tag)
├── is_pinned
└── is_archived

Folder
├── user (FK → User)
├── name
└── parent (FK → self)

Tag
├── user (FK → User)
├── name
└── color

Idea
├── user (FK → User)
├── title
├── description
└── status

Reminder
├── user (FK → User)
├── title
├── remind_at
└── is_completed

-- Tracker
DailyEntry
├── user (FK → User)
├── date
├── mood
├── energy_level
├── morning_notes
├── evening_notes
├── wins
├── challenges
├── gratitude
├── sleep_hours
├── sleep_quality
├── water_intake
└── exercise_minutes

MoodLog
├── user (FK → User)
├── mood
├── notes
└── logged_at

CustomMetric
├── user (FK → User)
├── name
├── unit
├── icon
└── target_value

MetricEntry
├── metric (FK → CustomMetric)
├── date
├── value
└── notes
```

## 🔄 Request Flow

### User Interaction Flow

```
User Action
    │
    ▼
Browser (Client)
    │
    ├─► HTMX Request (Partial Update)
    │       │
    │       ▼
    │   Django View
    │       │
    │       ├─► Query Database
    │       │       │
    │       │       ▼
    │       │   Return Data
    │       │
    │       ▼
    │   Render Partial Template
    │       │
    │       ▼
    └─► Update DOM Section
            
OR
    │
    ▼
Full Page Request
    │
    ▼
Django View
    │
    ├─► Query Database
    │   
    ├─► Process Logic
    │
    ├─► Prepare Context
    │
    ▼
Render Full Template
    │
    ▼
Return HTML
```

## 🎨 Frontend Architecture

### Design System

```
CSS Architecture
│
├── Variables (Theme)
│   ├── Colors (Primary, Secondary, Accent)
│   ├── Backgrounds (Dark theme)
│   ├── Text (Primary, Secondary, Muted)
│   ├── Borders
│   └── Shadows & Glows
│
├── Base Styles
│   ├── Typography (Epilogue font)
│   ├── Layout (Flexbox, Grid)
│   └── Animations
│
├── Components
│   ├── Cards
│   ├── Buttons
│   ├── Forms
│   ├── Navigation
│   └── Modals
│
└── Pages
    ├── Dashboard
    ├── Task views
    ├── Habit tracker
    └── Finance dashboard
```

### Component Hierarchy

```
App Container
│
├── Sidebar Navigation
│   ├── Logo
│   ├── Menu Items
│   │   ├── Dashboard
│   │   ├── Tasks
│   │   ├── Habits
│   │   ├── Pomodoro
│   │   ├── Finance
│   │   ├── Notes
│   │   └── Tracker
│   └── User Profile
│
└── Main Content Area
    │
    ├── Page Header
    │   ├── Title & Subtitle
    │   └── Action Buttons
    │
    ├── Stats Grid (Dashboard)
    │   ├── Total Tasks
    │   ├── Completed Today
    │   ├── Pomodoro Sessions
    │   └── Monthly Balance
    │
    └── Content Grid
        │
        ├── Left Column
        │   ├── Today's Tasks
        │   └── Habit Tracker
        │
        └── Right Column
            ├── Mood Tracker
            ├── Recent Notes
            └── Upcoming Reminders
```

## 🔌 Integration Points

### External Services

```
FlowHub ←→ Google APIs
    │
    ├── Google Calendar API
    │   └── Sync events & reminders
    │
    └── Google Tasks API
        └── Sync tasks bidirectionally
```

### Future Integrations

```
Planned:
├── Email (SMTP)
│   └── Reminders & notifications
├── Mobile Apps
│   └── iOS & Android
├── Third-party APIs
│   ├── Slack
│   ├── Trello
│   └── GitHub
└── Webhooks
    └── Custom integrations
```

## 🚀 Deployment Architecture

### Development

```
Local Machine
│
├── SQLite Database
├── Django Dev Server (port 8000)
├── Static Files (served by Django)
└── Media Files (local storage)
```

### Production (Recommended)

```
┌─────────────────────────────────────┐
│         Reverse Proxy               │
│         (Nginx)                     │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────┐   ┌──────────────┐
│   WSGI       │   │   Static     │
│  (Gunicorn)  │   │   Files      │
└──────┬───────┘   └──────────────┘
       │
       ▼
┌──────────────┐
│   Django     │
│ Application  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  PostgreSQL  │
│   Database   │
└──────────────┘
```

## 🔐 Security Features

### Authentication & Authorization
- Django's built-in auth system
- Password hashing (PBKDF2)
- CSRF protection
- Session management
- Login required decorators

### Data Protection
- User data isolation (FK filters)
- Input validation
- XSS protection (Django templates)
- SQL injection prevention (ORM)

## 📈 Performance Optimization

### Database
- Indexed foreign keys
- Efficient queries (select_related, prefetch_related)
- Query optimization

### Frontend
- HTMX for partial updates
- Minimal JavaScript
- CSS animations (GPU accelerated)
- Lazy loading where appropriate

### Caching (Future)
- Redis for session storage
- Query result caching
- Static file caching

## 🧪 Testing Strategy

```
Test Pyramid
    │
    ├── Unit Tests
    │   ├── Model methods
    │   ├── View functions
    │   └── Utility functions
    │
    ├── Integration Tests
    │   ├── View + Model interaction
    │   ├── Form validation
    │   └── API endpoints
    │
    └── E2E Tests
        ├── User workflows
        ├── CRUD operations
        └── Multi-step processes
```

## 📊 Monitoring & Analytics

### Built-in Metrics
- Task completion rates
- Habit streaks
- Pomodoro session counts
- Financial summaries
- Mood trends

### Future Analytics
- User activity patterns
- Feature usage stats
- Performance metrics
- Error tracking

---

This architecture is designed for:
✅ Scalability
✅ Maintainability
✅ Performance
✅ User experience
✅ Security

Built with modern best practices and ready to grow with your needs!
