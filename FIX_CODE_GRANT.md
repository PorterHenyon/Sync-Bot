# 🔧 Fix: "Integration requires code grant" Error

If you see this error when trying to add your bot to a server, here's how to fix it:

## ✅ Quick Fix

1. **Go to Discord Developer Portal**
   - https://discord.com/developers/applications
   - Select your application

2. **Click "Bot" in the left sidebar**

3. **Find "Require OAuth2 Code Grant"**
   - Scroll down on the Bot page
   - Look for a toggle/checkbox labeled **"Require OAuth2 Code Grant"**
   - It's usually near the "Public Bot" setting

4. **Turn it OFF**
   - The toggle should be **gray/unchecked/disabled**
   - If it's blue/checked/enabled, click it to turn it off

5. **Try your invite URL again**
   - The bot should now install normally

## 📍 Where to Find It

**Bot Page Layout (top to bottom):**
1. Bot Username & Icon
2. Token
3. Public Bot (toggle)
4. **Require OAuth2 Code Grant** ← **Turn this OFF!**
5. Privileged Gateway Intents
6. Remove Bot / Delete Bot

## 🔍 Visual Guide

**What it looks like when OFF (correct):**
```
☐ Require OAuth2 Code Grant
  (toggle is gray/unchecked)
```

**What it looks like when ON (wrong):**
```
☑ Require OAuth2 Code Grant
  (toggle is blue/checked) ← Turn this OFF!
```

## ❓ Why This Happens

- **OAuth2 Code Grant** is for advanced OAuth2 authentication flows
- For simple bot installation, you don't need it
- When enabled, it requires additional authentication steps
- **Keep it OFF** for easy bot installation

## ✅ After Fixing

Once you turn it off:
1. Use your invite URL (manual or generated)
2. Select your server
3. Click "Authorize"
4. Bot should install successfully!

## 🆘 Still Not Working?

If you still get the error after turning it off:
- Refresh the Discord Developer Portal page
- Make sure you saved the change (usually auto-saves)
- Try generating a new invite URL
- Clear your browser cache and try again

