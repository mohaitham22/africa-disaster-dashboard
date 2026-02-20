# 🚀 Deploy Your Africa Disaster Dashboard to Streamlit Cloud

## 📋 Quick Deployment Guide

Follow these simple steps to deploy your dashboard online and share with friends!

---

## ✅ Step 1: Create a GitHub Account (if you don't have one)

1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process

---

## ✅ Step 2: Install Git (if not already installed)

### For Windows:

1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your computer if needed

---

## ✅ Step 3: Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `africa-disaster-dashboard`
3. Description: "Africa Disaster Events Analysis Dashboard"
4. Choose **Public** (required for free Streamlit Cloud deployment)
5. Click "Create repository"

---

## ✅ Step 4: Push Your Code to GitHub

Open **PowerShell** in your project folder and run these commands:

```powershell
# Navigate to your project folder
cd "D:\Graduation project"

# Initialize Git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Africa Disaster Dashboard"

# Add your GitHub repository (REPLACE with YOUR username)
git remote add origin https://github.com/YOUR-USERNAME/africa-disaster-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANT:** Replace `YOUR-USERNAME` with your actual GitHub username!

**If prompted for credentials:**

- Username: Your GitHub username
- Password: Use a Personal Access Token (not your GitHub password)
  - Create token at: https://github.com/settings/tokens
  - Select "repo" scope
  - Copy and paste the token as password

---

## ✅ Step 5: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io

2. **Sign in with GitHub**
   - Click "Sign in with GitHub"
   - Authorize Streamlit

3. **Create New App**
   - Click "New app" button
   - Repository: Select `africa-disaster-dashboard`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

4. **Wait for Deployment** (2-5 minutes)
   - Streamlit will install dependencies
   - Your app will be built and deployed

---

## 🎉 Step 6: Get Your Shareable Link!

Once deployed, you'll get a URL like:

```
https://YOUR-USERNAME-africa-disaster-dashboard-RANDOM.streamlit.app
```

**This is your shareable link!** 🎊

---

## 📱 Share with Friends

Send them the link via:

- WhatsApp
- Email
- Facebook
- Twitter
- SMS

They can access it from:

- ✅ Phone
- ✅ Tablet
- ✅ Computer
- ✅ Anywhere with internet!

---

## 🔧 Update Your App Later

When you make changes:

```powershell
cd "D:\Graduation project"
git add .
git commit -m "Updated dashboard"
git push
```

Streamlit Cloud will automatically redeploy! 🚀

---

## ❓ Troubleshooting

### "Git is not recognized"

- Install Git from https://git-scm.com/download/win
- Restart PowerShell

### "Permission denied"

- Use a Personal Access Token instead of password
- Create at: https://github.com/settings/tokens

### "Module not found" on Streamlit Cloud

- Make sure `requirements.txt` is in your repository
- Check all packages are listed

### Data file not found

- Make sure `Book1.csv` is in the repository
- Check it's not in `.gitignore`

---

## 🎯 Your Deployment Checklist

- [ ] GitHub account created
- [ ] Git installed
- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed on Streamlit
- [ ] Shareable link obtained
- [ ] Shared with friends! 🎉

---

## 📞 Need Help?

- Streamlit Docs: https://docs.streamlit.io/streamlit-cloud
- GitHub Docs: https://docs.github.com
- Streamlit Community: https://discuss.streamlit.io

---

**Created: February 20, 2026**
**Status: Ready to Deploy! ✅**
