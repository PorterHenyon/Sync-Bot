# 🔧 Manual Bot Invite URL Generator

If Discord's URL Generator isn't working, use this method to create your bot invite URL manually.

## Step 1: Get Your Application ID

1. Go to https://discord.com/developers/applications
2. Select your application
3. Click **"General Information"** in the left sidebar
4. Find **"APPLICATION ID"** (it's a long number like `123456789012345678`)
5. **Copy this number** - this is your Client ID

## Step 2: Calculate Permissions

### Option A: Use Permission Calculator
1. Go to: https://discordapi.com/permissions.html
2. Check the permissions you need:
   - ✅ **Manage Roles** (REQUIRED)
   - ✅ View Channels
   - ✅ Read Message History
   - ✅ Send Messages
3. Copy the permission number from the bottom

### Option B: Use Pre-calculated Values

**Minimal (just Manage Roles):**
```
268435456
```

**Recommended (Manage Roles + View Channels + Read Message History + Send Messages):**
```
268446720
```

**Full Permissions (everything):**
```
8
```

## Step 3: Build Your URL

Replace the values in this URL:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_APPLICATION_ID&permissions=PERMISSION_NUMBER&scope=bot
```

### Example:
If your Application ID is `123456789012345678` and you want the recommended permissions:

```
https://discord.com/api/oauth2/authorize?client_id=123456789012345678&permissions=268446720&scope=bot
```

## Step 4: Use the URL

1. **Copy your complete URL**
2. **Paste it in your web browser** and press Enter
3. **Select your Patreon server** from the dropdown
4. **Click "Authorize"**
5. **Repeat** with the same URL for your Main server

## Quick Reference

**Permission Values:**
- Manage Roles only: `268435456`
- Recommended: `268446720`
- Administrator: `8` (use with caution!)

**URL Template:**
```
https://discord.com/api/oauth2/authorize?client_id=APPLICATION_ID&permissions=PERMISSIONS&scope=bot
```

## Troubleshooting

**"Invalid client" error:**
- Make sure you copied the Application ID correctly
- Make sure you've created the bot (Bot → Add Bot)

**"Missing permissions" error:**
- The permission number might be wrong
- Try using `268446720` (recommended permissions)

**URL doesn't work:**
- Make sure the URL starts with `https://discord.com/api/oauth2/authorize?`
- Make sure it ends with `&scope=bot`
- Check for typos in the Application ID

