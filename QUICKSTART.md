# FlowHub - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd productivity_hub

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

### Step 2: Set Up Database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Your Account

```bash
# Create admin user
python manage.py createsuperuser

# Follow prompts to set username and password
```

### Step 4: Launch!

```bash
# Start the development server
python manage.py runserver

# Visit http://localhost:8000 in your browser
```

## 🎯 First Steps in FlowHub

### 1. Explore the Dashboard
- See overview of all your productivity metrics
- Quick access to today's tasks and habits
- Track your mood and daily progress

### 2. Create Your First Task
- Click "➕ New Task" button
- Add title, description, due date
- Set priority (High/Medium/Low)
- Choose status (Pitched/In Progress/Completed)

### 3. Set Up Your Habits
- Go to Habits section
- Create 2-3 simple daily habits
- Choose fun icons and colors
- Start building streaks! 🔥

### 4. Try the Pomodoro Timer
- Navigate to Pomodoro section
- Start a 25-minute focus session
- Take breaks between sessions
- Track your productive hours

### 5. Track Your Finances
- Add your accounts (checking, savings, etc.)
- Create spending categories
- Record transactions
- Set monthly budgets

### 6. Write Notes & Ideas
- Capture thoughts in Notes
- Organize with folders and tags
- Track ideas you want to develop
- Set reminders for important items

### 7. Daily Check-ins
- Log your mood throughout the day
- Write morning intentions
- Evening reflections on wins/challenges
- Practice gratitude journaling

## 🎨 Customization Tips

### Change Theme Colors
Edit `templates/base.html` and modify CSS variables:
```css
:root {
    --primary: #6366f1;     /* Main accent color */
    --secondary: #8b5cf6;   /* Secondary color */
    --accent: #f59e0b;      /* Highlight color */
}
```

### Pomodoro Settings
- Default: 25 min work, 5 min break
- Customize in Pomodoro Settings
- Auto-start options available

## 🔌 Optional: Google Integration

### Connect Google Calendar & Tasks

1. **Get Google API Credentials**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create project and enable APIs
   - Download OAuth credentials

2. **Add to Settings**
   - Create `.env` file
   - Add your credentials:
   ```
   GOOGLE_CLIENT_ID=your_id_here
   GOOGLE_CLIENT_SECRET=your_secret_here
   ```

3. **Sync Your Data**
   - Tasks auto-sync with Google Tasks
   - Calendar events appear in your dashboard

## 📱 Mobile Access

The interface is fully responsive! Access from:
- Desktop browsers (best experience)
- Tablets (optimized layout)
- Mobile phones (touch-friendly)

## 💡 Pro Tips

### Task Management
- Use Kanban view for visual projects
- Calendar view for deadline planning
- List view for quick task scanning
- Drag & drop tasks between columns

### Habit Success
- Start with just 3 habits
- Check in at the same time daily
- Celebrate streaks - they matter!
- Don't break the chain 🔗

### Pomodoro Mastery
- Eliminate distractions before starting
- Use full-screen mode for focus
- Link sessions to specific tasks
- Track patterns in productivity

### Finance Wisdom
- Record expenses immediately
- Review budgets weekly
- Track all accounts for complete picture
- Categorize consistently

### Journaling Power
- Write morning intentions daily
- Evening reflection on what worked
- Gratitude practice boosts happiness
- Track mood patterns over time

## 🛠️ Troubleshooting

### Can't log in?
- Reset password through admin: `/admin/`
- Create new superuser if needed

### Tasks not showing?
- Check filter settings
- Ensure tasks aren't archived
- Try different view (List/Kanban/Calendar)

### Habits not tracking?
- Verify you're checking them off
- Check timezone settings
- Refresh the page

### Server won't start?
- Check port 8000 isn't in use
- Activate virtual environment
- Run migrations again

## 📚 Learn More

### Django Basics
- [Official Django Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- Models, Views, Templates explained

### HTMX Integration
- Real-time updates without JavaScript
- Smooth user experience
- Learn more at [htmx.org](https://htmx.org/)

## 🤝 Get Help

### Resources
- Check README.md for detailed docs
- Review code comments
- Explore Django admin at `/admin/`
- Search existing GitHub issues

### Community
- Share your customizations
- Report bugs
- Suggest features
- Contribute improvements

## 🎉 You're All Set!

Start building your perfect productivity system:
1. ✅ Tasks organized
2. 🔥 Habits tracked
3. ⏱️ Time managed
4. 💰 Finances monitored
5. 📝 Thoughts captured
6. 📊 Progress measured

**Happy productivity! 🚀**
