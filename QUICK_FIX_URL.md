# 🚨 Quick Fix: URL Won't Generate

If you can't see the generated URL in Discord Developer Portal, follow these steps:

## ✅ Step-by-Step Fix

1. **Go to:** https://discord.com/developers/applications
2. **Select your application**
3. **Click "OAuth2" in the left sidebar**
4. **Click "URL Generator"** (NOT "General"!)

5. **Check the `bot` scope:**
   - Look for "SCOPES" section
   - ✅ **CHECK the `bot` checkbox** (this is MANDATORY!)
   - The URL will NOT appear until you check this!

6. **Select permissions (optional but recommended):**
   - Scroll down to "BOT PERMISSIONS"
   - Check: ✅ Manage Roles
   - Check: ✅ View Channels
   - Check: ✅ Read Message History

7. **Scroll ALL THE WAY DOWN:**
   - The generated URL is at the very bottom
   - Look for a section called "Generated URL" or "SCOPED URL"
   - It will be in a text box with a "Copy" button

## 🔍 Still Not Working?

### Check These Things:

- [ ] Did you check the `bot` scope? (Most common issue!)
- [ ] Are you in "URL Generator" and NOT "General"?
- [ ] Did you scroll all the way to the bottom?
- [ ] Did you create the bot first? (Bot → Add Bot)
- [ ] Try refreshing the page after checking `bot` scope

### Visual Checklist:

**What you SHOULD see:**
```
OAuth2
├── General (don't use this)
├── URL Generator ← CLICK THIS!
└── Redirects (don't use this)

In URL Generator page:
├── SCOPES
│   └── ☑ bot ← MUST CHECK THIS!
├── BOT PERMISSIONS
│   └── ☑ Manage Roles
└── Generated URL (at bottom) ← This appears after checking bot scope
```

**What you SHOULD NOT see:**
- Fields asking for "Redirect URIs"
- Error about "must specify at least one URI"
- Empty URL box at bottom

## 💡 Pro Tip

The URL generates **instantly** after you check the `bot` scope - no need to save anything. Just check the box and scroll down!

