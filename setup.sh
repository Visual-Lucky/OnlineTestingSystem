#!/bin/bash
# ============================================================
#  OTS Quick Setup Script
# ============================================================
echo "========================================"
echo "  Online Testing System — Setup"
echo "========================================"

# 1. Install dependencies
echo ""
echo "[1/4] Installing Python dependencies..."
pip install -r requirements.txt

# 2. Run migrations
echo ""
echo "[2/4] Setting up database..."
python manage.py migrate

# 3. Collect static files
echo ""
echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

# 4. Prompt for superuser
echo ""
echo "[4/4] Create admin/teacher account"
echo "      (This is used to access /admin/ and /teacher/)"
python manage.py createsuperuser

echo ""
echo "========================================"
echo "  Setup complete!"
echo "  Run: python manage.py runserver"
echo "  Then open: http://127.0.0.1:8000"
echo "========================================"
