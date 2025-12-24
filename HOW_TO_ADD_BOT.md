# 🎯 How to Add Your Bot to Discord Servers

This is a **step-by-step guide** with exact instructions on how to add your Discord bot to your servers.

---

## 📋 Step 1: Create the Bot Application

1. **Go to Discord Developer Portal**
   - Open: https://discord.com/developers/applications
   - Log in with your Discord account

2. **Create New Application**
   - Click the **"New Application"** button (top right, blue button)
   - Enter a name (e.g., "Role Sync Bot")
   - Click **"Create"**

3. **You should now see your application dashboard**

---

## 🤖 Step 2: Create the Bot User

1. **In the left sidebar, click "Bot"**
   - You'll see a page with bot settings

2. **Click "Add Bot"**
   - A popup will appear asking "Do you want to add a bot to this application?"
   - Click **"Yes, do it!"**

3. **Enable Server Members Intent**
   - Scroll down on the Bot page
   - Find the section called **"Privileged Gateway Intents"**
   - Look for **"SERVER MEMBERS INTENT"** (or "MEMBERS INTENT")
   - **Toggle it ON** (switch should be blue/enabled)
   - A warning will appear - click **"Yes"** to confirm

4. **Save Your Bot Token**
   - Above the intents section, you'll see **"Token"**
   - Click **"Reset Token"** or **"Copy"** button
   - **SAVE THIS TOKEN** - you'll need it for Railway!
   - ⚠️ **NEVER share this token publicly!**

---

## 🔗 Step 3: Generate Invite URL

1. **In the left sidebar, click "OAuth2"**
   - Then click **"URL Generator"** (under OAuth2)
   - ⚠️ **IMPORTANT:** You're using "URL Generator", NOT "General" or "Redirects"
   - If you see an error about URIs, you're in the wrong section - make sure you clicked "URL Generator"

2. **Select Scopes (checkboxes)**
   - Under **"SCOPES"**, check:
     - ✅ **`bot`** (this is required!)
     - ✅ `applications.commands` (optional, for slash commands)

3. **Select Bot Permissions**
   - Scroll down to **"BOT PERMISSIONS"**
   - Check these boxes:
     - ✅ **Manage Roles** (REQUIRED - most important!)
     - ✅ View Channels
     - ✅ Read Message History
     - ✅ Send Messages (optional, for command responses)

4. **Copy the Generated URL**
   - At the bottom, you'll see a box with a URL that looks like:
     ```
     https://discord.com/api/oauth2/authorize?client_id=123456789&permissions=268435456&scope=bot
     ```
   - Click **"Copy"** button next to the URL

---

## ➕ Step 4: Add Bot to Your Patreon Server

1. **Open the copied URL in your web browser**
   - Paste it in the address bar and press Enter

2. **You'll see a Discord authorization page**
   - It shows your bot's name and avatar
   - It lists the permissions you selected

3. **Select Your Patreon Server**
   - Look for the dropdown that says **"Select a server"**
   - Click it and choose your **Patreon Discord server**
   - ⚠️ **Make sure you have "Manage Server" permission** in that server!

4. **Click "Authorize"**
   - You might need to complete a CAPTCHA
   - Click **"Authorize"** again if prompted

5. **Success!**
   - You should see "Authorized" message
   - Go to your Patreon Discord server
   - The bot should appear in the member list (usually offline at first)

---

## ➕ Step 5: Add Bot to Your Main Server

1. **Use the SAME URL from Step 3**
   - You can use the same invite URL for multiple servers!

2. **Open the URL again in your browser**

3. **Select Your Main Server**
   - In the dropdown, choose your **Main Discord server**

4. **Click "Authorize"**
   - Complete CAPTCHA if needed

5. **Success!**
   - The bot should now be in both servers

---

## ⚙️ Step 6: Set Up Bot Role Position (IMPORTANT!)

The bot's role must be **ABOVE** the roles it needs to assign!

1. **Go to your Main Discord server**
   - Click the server name (top left)
   - Click **"Server Settings"**

2. **Click "Roles"** (left sidebar)

3. **Find your bot's role**
   - Look for the bot's name in the role list
   - It should be near the bottom by default

4. **Drag the bot's role UP**
   - Click and hold the bot's role
   - Drag it **ABOVE** all the roles you want to sync
   - For example, if you want to sync "Supporter" and "VIP" roles, the bot's role must be above both

5. **Repeat for Patreon server** (if needed)
   - Do the same in your Patreon server

6. **Save changes** (usually auto-saves)

---

## ✅ Step 7: Verify Bot is Working

1. **Check both servers**
   - The bot should appear in the member list
   - It might show as "Offline" until you deploy it to Railway

2. **Get Server IDs** (you'll need these for Railway)
   - Enable Developer Mode: Discord Settings → Advanced → Developer Mode (toggle ON)
   - Right-click your **Patreon server** → **"Copy Server ID"**
   - Right-click your **Main server** → **"Copy Server ID"**
   - Save both IDs!

---

## 🎯 Quick Checklist

Before deploying to Railway, make sure you have:

- [ ] Bot created in Discord Developer Portal
- [ ] Server Members Intent enabled
- [ ] Bot token copied (for Railway)
- [ ] Bot added to Patreon server
- [ ] Bot added to Main server
- [ ] Bot's role positioned above roles to sync
- [ ] Patreon Server ID copied
- [ ] Main Server ID copied
- [ ] Role names noted (for SYNC_ROLES config)

---

## 🆘 Troubleshooting

### "I don't see the bot in my server"
- Make sure you clicked "Authorize" after selecting the server
- Check that you have "Manage Server" permission
- Try the invite URL again

### "Bot can't assign roles"
- Make sure bot's role is **above** the roles it needs to assign
- Check that "Manage Roles" permission is enabled
- Verify bot's role has "Manage Roles" permission enabled

### "I can't find Server Members Intent"
- Make sure you clicked "Add Bot" first
- Refresh the page
- It's in the "Privileged Gateway Intents" section, below the token

### "The invite URL doesn't work"
- Make sure you copied the full URL
- Try generating a new one in OAuth2 → URL Generator
- Make sure you selected the `bot` scope

### "You must specify at least one URI for authentication to work"
- ❌ **You're in the wrong section!** This error appears in OAuth2 → General
- ✅ **Solution:** Go to OAuth2 → **URL Generator** instead
- The URL Generator doesn't require redirect URIs - that's only for OAuth2 authentication flows
- **Steps to fix:**
  1. In the left sidebar, click **"OAuth2"**
  2. Make sure you click **"URL Generator"** (NOT "General" or "Redirects")
  3. You should see checkboxes for "SCOPES" and "BOT PERMISSIONS"
  4. If you see a field asking for "Redirects" or "URIs", you're in the wrong place!

---

## 📸 Visual Guide Locations

**Discord Developer Portal Structure:**
```
Applications
├── Your App Name
    ├── General Information
    ├── Bot ← Click here first!
    ├── OAuth2 ← Then here for invite URL
    ├── ...
```

**Bot Page Sections (top to bottom):**
1. Bot Username & Icon
2. Token (copy this!)
3. Public Bot (toggle)
4. Require OAuth2 Code Grant
5. **Privileged Gateway Intents** ← Server Members Intent is here!
6. Remove Bot / Delete Bot

**OAuth2 URL Generator Sections:**
1. SCOPES (check `bot`)
2. BOT PERMISSIONS (check `Manage Roles`)
3. Generated URL (at bottom - copy this!)

---

Need more help? Check the main README.md for Railway deployment instructions!

