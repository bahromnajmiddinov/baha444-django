# FlowHub - All-in-One Productivity & Life Management Platform

A beautiful, full-featured Django application for managing your entire productive life. Includes task management, habit tracking, Pomodoro timer, finance tracking, notes, daily mood tracking, and more.

## ✨ Features

### 📋 Task Management
- **Multiple Views**: List, Kanban board, and Calendar views
- **Status Tracking**: Pitched → In Progress → Completed → Paid
- **Priority Levels**: Low, Medium, High with visual indicators
- **Drag & Drop**: Reorder tasks easily in Kanban view
- **Attachments & Comments**: Add files and collaborate on tasks
- **Google Tasks Integration**: Sync with Google Tasks (optional)

### 🔥 Habit Tracking
- **Streak Tracking**: Build momentum with daily streak counts
- **Custom Icons & Colors**: Personalize each habit
- **Daily/Weekly/Monthly**: Different frequency options
- **Completion Rate**: Track your consistency over time
- **Visual Dashboards**: Beautiful widgets showing progress

### ⏱️ Pomodoro Timer
- **Structured Sessions**: Focus blocks with break times
- **Customizable Durations**: Set your preferred timer lengths
- **Session History**: Track completed Pomodoros
- **Task Integration**: Link sessions to specific tasks
- **Minimal Distraction Mode**: Full-screen focus interface

### 💰 Personal Finance
- **Multiple Accounts**: Track checking, savings, credit cards, investments
- **Budget Management**: Set budgets by category
- **Transaction Tracking**: Record income and expenses
- **Visual Analytics**: Charts showing spending patterns
- **Monthly Reports**: See where your money goes

### 📝 Notes & Ideas
- **Rich Text Notes**: Write and organize your thoughts
- **Folders & Tags**: Organize notes hierarchically
- **Ideas Tracker**: Capture and develop ideas
- **Reminders**: Never forget important tasks
- **Quick Search**: Find notes instantly

### 📊 Daily Tracker
- **Mood Logging**: Track how you feel throughout the day
- **Daily Reflections**: Morning and evening journal entries
- **Gratitude Journal**: What are you thankful for?
- **Sleep Tracking**: Monitor sleep quality and duration
- **Custom Metrics**: Track anything (water, exercise, screen time, etc.)
- **Energy Levels**: Monitor your energy patterns

## 🎨 Design Philosophy

FlowHub features a **modern, dark-themed interface** inspired by the best productivity tools:
- **Minimalist Dark UI** with subtle gradients and glows
- **Smooth Animations** using CSS transitions
- **Custom Typography** with Epilogue and Space Mono fonts
- **Responsive Design** works on desktop, tablet, and mobile
- **HTMX Integration** for seamless updates without page reloads

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone or extract the project**
```bash
cd productivity_hub
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Visit http://localhost:8000**

## 📁 Project Structure

```
productivity_hub/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Core app (dashboard, auth)
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── tasks/                  # Task management
│   ├── models.py          # Task, TaskAttachment, TaskComment
│   ├── views.py           # List, Kanban, Calendar views
│   └── urls.py
├── habits/                 # Habit tracking
│   ├── models.py          # Habit, HabitCompletion
│   ├── views.py
│   └── urls.py
├── pomodoro/              # Pomodoro timer
│   ├── models.py          # PomodoroSession, PomodoroSettings
│   ├── views.py
│   └── urls.py
├── finance/               # Finance tracking
│   ├── models.py          # Account, Transaction, Budget, Category
│   ├── views.py
│   └── urls.py
├── notes/                 # Notes and ideas
│   ├── models.py          # Note, Folder, Tag, Idea, Reminder
│   ├── views.py
│   └── urls.py
├── tracker/               # Daily tracking
│   ├── models.py          # DailyEntry, MoodLog, CustomMetric
│   ├── views.py
│   └── urls.py
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── dashboard.html     # Main dashboard
│   └── [app]/             # App-specific templates
├── static/                # CSS, JS, images
├── media/                 # User uploads
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Google Calendar Integration (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Calendar API and Tasks API
4. Create OAuth 2.0 credentials
5. Add credentials to `.env` file:

```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

### Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Google API (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Database (optional, defaults to SQLite)
DATABASE_URL=
```

## 🎯 Usage Tips

### Task Management
1. **Use Kanban View** for visual project management
2. **Set Priorities** to focus on what matters
3. **Add Due Dates** to stay on schedule
4. **Link Tasks to Pomodoros** for better focus tracking

### Habit Building
1. **Start Small** - Begin with 2-3 habits
2. **Be Consistent** - Track daily for best results
3. **Celebrate Streaks** - Watch those 🔥 grow!
4. **Review Weekly** - Adjust habits as needed

### Pomodoro Technique
1. **Standard Session**: 25 min work, 5 min break
2. **After 4 Sessions**: Take a 15-30 minute break
3. **Minimize Distractions**: Use the full-screen mode
4. **Track Your Progress**: Review completed sessions

### Finance Tracking
1. **Set Realistic Budgets** per category
2. **Record All Transactions** for accuracy
3. **Review Monthly** to adjust spending
4. **Track Net Worth** across all accounts

### Daily Tracking
1. **Morning Routine**: Set intentions for the day
2. **Evening Reflection**: Review wins and challenges
3. **Gratitude Practice**: List 3 things daily
4. **Mood Patterns**: Identify what affects your mood

## 🛠️ Development

### Adding New Features

The project is modular and easy to extend:

1. **Create a New App**
```bash
python manage.py startapp myapp
```

2. **Add to INSTALLED_APPS** in `config/settings.py`

3. **Create Models** in `myapp/models.py`

4. **Create Views** in `myapp/views.py`

5. **Add URL Patterns** in `myapp/urls.py`

6. **Include in Main URLs** in `config/urls.py`

### Database Migrations

After changing models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests

```bash
python manage.py test
```

## 🌈 Customization

### Theming
Edit `templates/base.html` CSS variables:
- Colors: `--primary`, `--secondary`, `--accent`
- Backgrounds: `--bg-primary`, `--bg-card`
- Text: `--text-primary`, `--text-secondary`

### Fonts
Update font imports in `base.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont" rel="stylesheet">
```

## 📝 Models Overview

### Task
- title, description, status, priority
- due_date, completed_date
- attachments, comments
- Google Tasks sync

### Habit
- name, description, icon, color
- frequency (daily/weekly/monthly)
- streak tracking
- completion history

### PomodoroSession
- session_type (focus/short_break/long_break)
- duration, completed_minutes
- linked to tasks
- completion tracking

### Transaction
- amount, description, date
- linked to account and category
- income/expense type

### Note
- title, content, folder
- tags, pinned, archived
- creation and update timestamps

### DailyEntry
- mood, energy_level
- morning/evening notes
- wins, challenges, gratitude
- sleep tracking, water intake

## 🚧 Roadmap

Future features planned:
- [ ] Mobile apps (iOS/Android)
- [ ] Team collaboration features
- [ ] Advanced analytics and insights
- [ ] Email reminders and notifications
- [ ] Export data to CSV/PDF
- [ ] Dark/Light theme toggle
- [ ] Custom widgets and layouts
- [ ] API for third-party integrations

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 💡 Credits

Inspired by the best productivity tools:
- Notion - for versatile workspace design
- Todoist - for task management excellence
- Habitica - for gamified habit tracking
- Forest - for focused work sessions
- YNAB - for mindful budgeting
- Day One - for journaling and reflection

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Check the documentation
- Review existing issues for solutions

---

**Built with ❤️ using Django, HTMX, and modern web technologies**

Start your journey to better productivity today! 🚀
