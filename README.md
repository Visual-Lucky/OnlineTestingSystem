# ⚡ Online Testing System — Upgraded Edition

A modern, secure online exam platform for teachers and students.

## 🚀 New Features (Upgraded)

### For Teachers
- **Shareable Test Links** — Every test gets a unique UUID link (e.g. `/test/abc-123/`). Copy and share with students.
- **Simultaneous Students** — 50–100 students can take the same test at the same time via the shared link.
- **Teacher Dashboard** — View all tests, copy shareable links, see submission counts.
- **Live Leaderboard** — Select any test to see ranked results (Name + Score only, no private data).
- **Anti-cheat Reports** — Every result records tab switches, copy attempts, and fullscreen exits.
- **Bulk JSON Upload** — Upload entire question banks at once via the dashboard.

### For Students
- **Modern UI** — Dark cosmic theme, smooth animations, responsive design.
- **Leaderboard After Test** — See your rank among all students who took the same test.
- **History Page** — View all past test scores with grades.

### Anti-Cheat System (Enhanced)
| Feature | Action |
|---|---|
| Fullscreen enforced | Test cannot proceed without fullscreen |
| Tab switch | Warning shown; auto-submit at 3 violations |
| Ctrl+C / Copy blocked | Clipboard intercepted, count tracked |
| Right-click disabled | No context menu |
| F12 / DevTools blocked | Key combos blocked |
| Text selection blocked | Can't select question text |
| All violations recorded | Teacher sees full cheat report per student |

## 🛠 Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit:
- **Student portal**: `http://localhost:8000/`
- **Teacher dashboard**: `http://localhost:8000/teacher/` (requires Django admin login)
- **Django admin**: `http://localhost:8000/admin/`

## 📋 How to Use

### Teacher Workflow
1. Login to Django admin → create Subject → create Test → add Questions (min 10)
2. Visit `/teacher/` → copy the shareable link for your test
3. Share the link with students (WhatsApp, email, etc.)
4. Students click the link, register/login, and take the test
5. View results and rankings in the Teacher Dashboard

### Student Workflow
1. Click the link shared by teacher (or go to `/`)
2. Register or login
3. Test opens in fullscreen — complete all questions within the time limit
4. Submit → see your score + rank on the leaderboard

## 📦 Project Structure

```
OTS/
├── models.py          — Candidate, Subject, Test (with token), Question, Result (with anti-cheat fields)
├── views.py           — All views + testByToken + api_leaderboard
├── urls.py            — All URL patterns including /test/<uuid>/
├── templates/
│   ├── main.html      — Base layout (dark theme)
│   ├── welcome.html   — Landing page
│   ├── login.html     — Student login
│   ├── home.html      — Subject/test selector
│   ├── Test_paper.html — Exam page with anti-cheat
│   ├── show_result.html — Result + leaderboard
│   ├── teacher_dashboard.html — Full teacher panel
│   └── candidate_history.html — Student history
└── static/
    └── theme.css      — Complete cosmic dark theme
```
