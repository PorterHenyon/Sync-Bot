# Sync-Bot

A Discord bot that automatically syncs roles from your Patreon Discord server to your main Discord server.

## Features

- 🔄 Automatic role syncing when members join or roles change
- 🎯 Configurable role mappings between servers
- 📊 Status and manual sync commands
- 🚀 Ready for Railway deployment

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot" and confirm
5. Under "Privileged Gateway Intents", enable:
   - ✅ Server Members Intent
   - ✅ Message Content Intent (if needed)
6. Copy the bot token (you'll need this later)
7. Go to "OAuth2" → "URL Generator"
8. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
9. Select bot permissions:
   - ✅ Manage Roles
   - ✅ View Channels
   - ✅ Read Message History
10. Copy the generated URL and open it in your browser
11. Add the bot to **both** your Patreon server and Main server

### 2. Get Server IDs

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on your Patreon server → Copy Server ID
3. Right-click on your Main server → Copy Server ID

### 3. Configure Role Mappings

1. Note the exact role names in both servers that you want to sync
2. Format: `PatreonRoleName:MainRoleName`
3. Example: If you have "Patreon Supporter" in Patreon server and "Supporter" in Main server, use: `Patreon Supporter:Supporter`

### 4. Railway Deployment

#### Option A: Deploy via Railway CLI

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize project:
   ```bash
   railway init
   ```

4. Add environment variables in Railway dashboard:
   - `DISCORD_BOT_TOKEN` - Your bot token
   - `PATREON_GUILD_ID` - Patreon server ID
   - `MAIN_GUILD_ID` - Main server ID
   - `SYNC_ROLES` - Role mappings (comma-separated, format: `Role1:Role1, Role2:Role2`)

5. Deploy:
   ```bash
   railway up
   ```

#### Option B: Deploy via GitHub

1. Push this repository to GitHub
2. Go to [Railway](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables in Railway dashboard (same as above)
6. Railway will automatically deploy

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
