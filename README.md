# Sync-Bot

A Discord bot that automatically syncs roles from your Patreon Discord server to your main Discord server.

## Features

- 🔄 Automatic role syncing when members join or roles change
- 🎯 Configurable role mappings between servers
- 📊 Status and manual sync commands
- 🚀 Optimized for Railway deployment
- 🛡️ Robust error handling and auto-reconnection

## 📖 Quick Start

**New to Discord bots?** Start here: **[HOW_TO_ADD_BOT.md](HOW_TO_ADD_BOT.md)** - Complete step-by-step guide with exact instructions!

## Setup Instructions

### 1. Create and Add Discord Bot

**👉 Follow the detailed guide: [HOW_TO_ADD_BOT.md](HOW_TO_ADD_BOT.md)**

This guide includes:
- Step-by-step instructions with exact button locations
- How to enable Server Members Intent
- How to generate the invite URL
- How to add bot to both servers
- How to set up role hierarchy
- Troubleshooting tips

**Quick summary:**
1. Create bot at https://discord.com/developers/applications
2. Enable "SERVER MEMBERS INTENT" in Bot settings
3. Copy bot token (save for Railway)
4. Generate invite URL in OAuth2 → URL Generator
5. Add bot to both Patreon and Main servers
6. Position bot's role above roles to sync

### 2. Get Server IDs

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on your Patreon server → Copy Server ID
3. Right-click on your Main server → Copy Server ID

### 3. Configure Role Mappings

1. Note the exact role names in both servers that you want to sync
2. Format: `PatreonRoleName:MainRoleName`
3. Example: If you have "Patreon Supporter" in Patreon server and "Supporter" in Main server, use: `Patreon Supporter:Supporter`

### 4. Railway Deployment (Optimized)

#### Recommended: Deploy via GitHub

1. **Push to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push
   ```

2. **Go to Railway**
   - Visit: https://railway.app
   - Sign up/login (can use GitHub account)

3. **Create New Project**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Authorize Railway to access your GitHub
   - Select your **Sync-Bot** repository
   - Railway will automatically detect Python and start building

4. **Add Environment Variables**
   - In your Railway project, click on the service
   - Go to **"Variables"** tab
   - Click **"New Variable"** and add each:
     
     **Required Variables:**
     ```
     DISCORD_BOT_TOKEN=your_bot_token_here
     PATREON_GUILD_ID=123456789012345678
     MAIN_GUILD_ID=987654321098765432
     SYNC_ROLES=Patreon Supporter:Supporter, Patreon VIP:VIP
     ```
     
     **Format for SYNC_ROLES:**
     - `PatreonRoleName:MainRoleName`
     - Separate multiple with commas: `Role1:Role1, Role2:Role2`
     - No spaces around colons (or be consistent)

5. **Deploy**
   - Railway will automatically deploy when you add variables
   - Watch the **"Deployments"** tab for build progress
   - Check **"Logs"** tab to see bot startup messages

6. **Verify Bot is Running**
   - Check Railway logs - you should see: `✅ Bot logged in as: YourBotName`
   - Bot should appear online in Discord
   - Use `!status` command in Discord to verify

#### Railway Optimizations Included

- ✅ Auto-reconnection on network issues
- ✅ Optimized logging for Railway's log viewer
- ✅ Better error handling and recovery
- ✅ Health monitoring ready
- ✅ Graceful shutdown handling

### 5. Environment Variables

Create a `.env` file for local development (or set in Railway):

```env
DISCORD_BOT_TOKEN=your_bot_token_here
PATREON_GUILD_ID=123456789012345678
MAIN_GUILD_ID=987654321098765432
SYNC_ROLES=Patreon Supporter:Supporter, Patreon VIP:VIP
```

**Important:** Never commit your `.env` file! It's already in `.gitignore`.

## Commands

- `!sync [member]` - Manually sync roles for a specific member or all members (Admin only)
- `!status` - Check bot status and configuration (Admin only)
- `!reload` - Reload role mappings from configuration (Admin only)

## How It Works

1. The bot monitors the Patreon server for:
   - New members joining
   - Role changes on existing members

2. When a change is detected:
   - The bot finds the corresponding member in the Main server
   - Compares their roles based on the configured mappings
   - Adds or removes roles in the Main server to match the Patreon server

3. Initial sync runs when the bot starts to ensure all current members are synced

## Requirements

- Python 3.11+
- discord.py 2.3.2+
- Bot must have "Manage Roles" permission in both servers
- Bot's role must be **above** the roles it needs to assign in the role hierarchy

## Troubleshooting

### Bot not syncing roles

1. Check that the bot has "Manage Roles" permission
2. Ensure the bot's role is higher than the roles it's trying to assign
3. Verify role names match exactly (case-sensitive)
4. Check bot logs in Railway dashboard

### Bot can't find servers

1. Verify the server IDs are correct
2. Ensure the bot is actually in both servers
3. Check that the bot has proper permissions

### Roles not mapping correctly

1. Verify role names match exactly (including spaces and capitalization)
2. Use `!status` command to see current mappings
3. Use `!reload` to reload mappings after fixing configuration

## Support

If you encounter issues, check the Railway logs or Discord bot logs for error messages.
