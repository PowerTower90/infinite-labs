# INFINITE LABS ADMIN DASHBOARD - STRICT INSTRUCTIONS

## CRITICAL RULES - READ FIRST

**ADMIN DASHBOARD APP IDENTITY:**
- Heroku App: `admin-infinite-labs`
- URL: https://admin-infinite-labs-0ebf1ce315a8.herokuapp.com/
- Python File: `admin_app.py` ONLY
- Environment Variable: `APP_TYPE=admin` (SET ON THIS APP)
- Purpose: Product management backend ONLY - NOT visible to customers

---

## WHAT THE ADMIN DASHBOARD IS

The admin dashboard is a **backend management tool** for authorized administrators to:
- Add new products to inventory
- Edit existing products
- Delete products
- Manage discounts (if enabled)
- View product inventory

**It is NOT:**
- A customer-facing website
- A shopping interface
- Open to the public
- For browsing products

---

## STRICT DEPLOYMENT RULES

### Rule 1: ALWAYS Deploy to Correct Heroku App
- **ADMIN changes** → `git push heroku-admin main`
- **MAIN website changes** → `git push heroku main`
- **NEVER push both simultaneously**

### Rule 2: Verify APP_TYPE Before Push
Before any admin deployment, verify the environment is set:
```powershell
heroku config --app admin-infinite-labs | findstr "APP_TYPE"
```
Expected output: `APP_TYPE: admin`

### Rule 3: Single Procfile Rule
- One `Procfile` controls both apps
- Procfile must always contain: `gunicorn wsgi:application`
- `wsgi.py` routes based on `APP_TYPE` environment variable
- **NEVER modify Procfile for individual apps**

### Rule 4: Changes Affecting Admin Dashboard
If you modify ANY of these files:
- `admin_app.py` - MUST verify it's the correct file
- `admin_templates/*` - ADMIN ONLY changes
- `wsgi.py` - ADMIN section only
- `admin_templates/admin_products.html` - PRODUCT MANAGEMENT INTERFACE ONLY
- `admin_templates/admin_dashboard.html` - ADMIN STATS ONLY

Then:
1. Ensure changes are in correct files
2. Run locally to test: `python admin_app.py`
3. Deploy: `git push heroku-admin main`
4. Verify: Visit admin URL and test

---

## DATABASE OPERATIONS FOR ADMIN

### Adding Products
**ONLY use these methods:**

1. **Via Admin Dashboard UI:**
   - Login at https://admin-infinite-labs-0ebf1ce315a8.herokuapp.com/
   - Click "Add New Product"
   - Fill form and submit

2. **Via Script (Production Only):**
   ```bash
   heroku run python sync_products_to_production.py --app admin-infinite-labs
   ```

**NEVER:**
- Directly modify database without logging
- Add products via the main website app
- Use generic database tools without admin app context

### Deleting Products
**ONLY via Admin Dashboard:**
- Click "Delete" button next to product
- Confirm warning dialog
- Changes immediately sync to shared database

---

## FILE STRUCTURE RULES

**Admin Dashboard Files:**
```
admin_app.py                     ← ADMIN APPLICATION (MAIN)
admin_templates/
  ├── admin_base.html           ← Header/nav
  ├── admin_login.html          ← Login form
  ├── admin_dashboard.html      ← Stats/overview
  ├── admin_products.html       ← Product list & management
  ├── admin_add_product.html    ← Add form
  └── admin_edit_product.html   ← Edit form
wsgi.py                         ← Routes to admin_app if APP_TYPE=admin
```

**DO NOT CONFUSE WITH:**
```
app.py                          ← CUSTOMER WEBSITE (DIFFERENT APP)
templates/                      ← CUSTOMER PAGES (DIFFERENT APP)
```

---

## TESTING BEFORE DEPLOYMENT

### Local Testing
```powershell
cd "d:\infinite labs"
python admin_app.py
# Should run on http://localhost:5001
# NOT on http://localhost:5000 (that's the main website)
```

### Test Checklist
- [ ] Login page loads
- [ ] Dashboard shows correct stats
- [ ] Product list displays all products
- [ ] Can add a test product
- [ ] Can edit a test product
- [ ] Can delete a test product
- [ ] Product appears in shared database

### Production Testing
After `git push heroku-admin main`:
1. Wait for build to complete
2. Visit: https://admin-infinite-labs-0ebf1ce315a8.herokuapp.com/
3. Login with admin credentials
4. Verify all functions work
5. Do NOT modify customer website immediately after

---

## WHAT NEVER TO DO

### ❌ CRITICAL - NEVER DO THESE

1. **Modify customer-facing templates**
   - ❌ Edit `templates/products.html`
   - ❌ Edit `templates/product_detail.html`
   - Use admin templates only

2. **Deploy admin changes to wrong app**
   - ❌ `git push heroku main` for admin changes
   - ✓ `git push heroku-admin main` for admin changes

3. **Mix APP_TYPE environment variables**
   - ❌ Set `APP_TYPE=admin` on `infinite-labs-peptides`
   - ❌ Set `APP_TYPE=main` on `admin-infinite-labs`
   - ✓ Keep them separate

4. **Modify app.py when working on admin**
   - ❌ Edit `app.py` for admin dashboard features
   - ✓ Edit `admin_app.py` ONLY

5. **Direct database access**
   - ❌ Connect to PostgreSQL directly
   - ✓ Use admin dashboard UI or scripts

6. **Deploy without testing**
   - ❌ Push changes without local testing first
   - ✓ Test locally, then deploy

7. **Forgetting APP_TYPE on Heroku**
   - ❌ Deploy without confirming APP_TYPE environment variable
   - ✓ Always verify: `heroku config --app admin-infinite-labs`

---

## DEPLOYMENT WORKFLOW (STEP BY STEP)

### Step 1: Make Changes
Edit files in your admin directory:
- `admin_app.py`
- `admin_templates/*`

### Step 2: Test Locally
```powershell
python admin_app.py
# Test at http://localhost:5001
```

### Step 3: Verify Environment
```powershell
heroku config --app admin-infinite-labs | findstr "APP_TYPE"
# Must show: APP_TYPE=admin
```

### Step 4: Commit Changes
```powershell
git add admin_app.py admin_templates/*
git commit -m "Admin Dashboard: [description of changes]"
```

### Step 5: Deploy
```powershell
git push heroku-admin main
# NEVER git push heroku main for admin changes
```

### Step 6: Verify Deployment
```powershell
heroku logs --app admin-infinite-labs --tail
# Look for successful build and deployment
```

### Step 7: Test in Production
Visit: https://admin-infinite-labs-0ebf1ce315a8.herokuapp.com/
- Login
- Test features
- Verify products show in product list

---

## EMERGENCY ROLLBACK

If something goes wrong after deployment:

```powershell
# Revert to previous commit
git revert HEAD
git push heroku-admin main

# OR check status
heroku logs --app admin-infinite-labs --tail

# OR restart the app
heroku restart --app admin-infinite-labs
```

---

## QUICK REFERENCE

| Action | Command | App |
|--------|---------|-----|
| Test locally | `python admin_app.py` | N/A |
| Deploy admin changes | `git push heroku-admin main` | admin-infinite-labs |
| View logs | `heroku logs --app admin-infinite-labs --tail` | admin-infinite-labs |
| Check environment | `heroku config --app admin-infinite-labs` | admin-infinite-labs |
| Run script in production | `heroku run python script.py --app admin-infinite-labs` | admin-infinite-labs |

---

## REMEMBER

✓ Admin Dashboard = Backend Management Tool  
✓ APP_TYPE = admin (on admin-infinite-labs)  
✓ Use admin templates ONLY  
✓ Deploy with `git push heroku-admin main`  
✓ Test before deploying  
✓ Keep main website and admin dashboard separate  

---

**Last Updated:** February 20, 2026  
**Status:** ACTIVE - Multiply enforced rules
