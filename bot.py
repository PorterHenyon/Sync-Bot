import discord
from discord.ext import commands
import os
import asyncio
from typing import Optional, Dict, List
import logging
import sys
from datetime import datetime

# Set up logging optimized for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Railway captures stdout
    ]
)
logger = logging.getLogger(__name__)

# Suppress noisy discord.py logs
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('discord.http').setLevel(logging.WARNING)

# Bot configuration
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration from environment variables
PATREON_GUILD_ID = int(os.getenv('PATREON_GUILD_ID', '0'))
MAIN_GUILD_ID = int(os.getenv('MAIN_GUILD_ID', '0'))
SYNC_ROLES_STR = os.getenv('SYNC_ROLES', '').strip()
SYNC_ROLES = [r.strip() for r in SYNC_ROLES_STR.split(',') if r.strip()] if SYNC_ROLES_STR else []

# Role mapping: {patreon_role_id: main_role_id}
ROLE_MAPPING: Dict[int, int] = {}

@bot.event
async def on_ready():
    logger.info('=' * 50)
    logger.info(f'✅ Bot logged in as: {bot.user} (ID: {bot.user.id})')
    logger.info(f'📊 Connected to {len(bot.guilds)} server(s)')
    logger.info('=' * 50)
    
    # Wait a moment for guilds to be cached (Railway may need a moment)
    await asyncio.sleep(3)
    
    # Get guilds (try fetching if not cached)
    patreon_guild = bot.get_guild(PATREON_GUILD_ID)
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    
    if not patreon_guild:
        try:
            patreon_guild = await bot.fetch_guild(PATREON_GUILD_ID)
        except discord.NotFound:
            logger.error(f'Patreon guild with ID {PATREON_GUILD_ID} not found!')
            return
        except discord.Forbidden:
            logger.error(f'No access to Patreon guild with ID {PATREON_GUILD_ID}!')
            return
    
    if not main_guild:
        try:
            main_guild = await bot.fetch_guild(MAIN_GUILD_ID)
        except discord.NotFound:
            logger.error(f'Main guild with ID {MAIN_GUILD_ID} not found!')
            return
        except discord.Forbidden:
            logger.error(f'No access to Main guild with ID {MAIN_GUILD_ID}!')
            return
    
    logger.info(f'Connected to Patreon guild: {patreon_guild.name}')
    logger.info(f'Connected to Main guild: {main_guild.name}')
    
    # Check if SYNC_ROLES is configured
    if not SYNC_ROLES:
        logger.warning('⚠️  SYNC_ROLES is not configured! Bot will not sync any roles.')
        logger.warning('   Please set SYNC_ROLES environment variable with role mappings.')
    else:
        # Build role mapping
        await build_role_mapping(patreon_guild, main_guild)
        
        if not ROLE_MAPPING:
            logger.error('❌ No valid role mappings found! Check your SYNC_ROLES configuration.')
        else:
            logger.info(f'✅ Configured {len(ROLE_MAPPING)} role mapping(s)')
            # Initial sync of all members
            await initial_sync(patreon_guild, main_guild)
    
    logger.info('Bot is ready and syncing roles!')

async def build_role_mapping(patreon_guild: discord.Guild, main_guild: discord.Guild):
    """Build a mapping between Patreon roles and Main server roles."""
    global ROLE_MAPPING
    
    for role_pair in SYNC_ROLES:
        if ':' not in role_pair:
            continue
        
        patreon_role_name, main_role_name = role_pair.split(':', 1)
        patreon_role_name = patreon_role_name.strip()
        main_role_name = main_role_name.strip()
        
        # Find roles by name
        patreon_role = discord.utils.get(patreon_guild.roles, name=patreon_role_name)
        main_role = discord.utils.get(main_guild.roles, name=main_role_name)
        
        if patreon_role and main_role:
            ROLE_MAPPING[patreon_role.id] = main_role.id
            logger.info(f'Mapped role: {patreon_role.name} -> {main_role.name}')
        else:
            if not patreon_role:
                logger.warning(f'Patreon role "{patreon_role_name}" not found!')
            if not main_role:
                logger.warning(f'Main role "{main_role_name}" not found!')

async def initial_sync(patreon_guild: discord.Guild, main_guild: discord.Guild):
    """Perform initial sync of all members."""
    logger.info('Starting initial role sync...')
    
    synced_count = 0
    skipped_count = 0
    
    for member in patreon_guild.members:
        if member.bot:
            continue
        
        # Find corresponding member in main guild
        main_member = main_guild.get_member(member.id)
        if not main_member:
            # Try fetching if not cached
            try:
                main_member = await main_guild.fetch_member(member.id)
            except discord.NotFound:
                skipped_count += 1
                continue
            except discord.HTTPException:
                skipped_count += 1
                continue
        
        # Sync roles
        await sync_member_roles(member, main_member)
        synced_count += 1
        
        # Small delay to avoid rate limits
        if synced_count % 10 == 0:
            await asyncio.sleep(0.5)
    
    logger.info(f'Initial sync complete! Synced {synced_count} members, skipped {skipped_count} members not in main server.')

async def sync_member_roles(patreon_member: discord.Member, main_member: discord.Member):
    """Sync roles from Patreon member to Main member."""
    if not ROLE_MAPPING:
        return  # No mappings configured, nothing to sync
    
    roles_to_add = []
    roles_to_remove = []
    
    # Get current roles in main server (excluding @everyone)
    main_role_ids = {role.id for role in main_member.roles if role.id != main_member.guild.id}
    
    # Get Patreon role IDs
    patreon_role_ids = {role.id for role in patreon_member.roles if role.id != patreon_member.guild.id}
    
    # Check which roles should be added/removed based on mapping
    for patreon_role_id, main_role_id in ROLE_MAPPING.items():
        has_patreon_role = patreon_role_id in patreon_role_ids
        has_main_role = main_role_id in main_role_ids
        
        if has_patreon_role and not has_main_role:
            roles_to_add.append(main_role_id)
        elif not has_patreon_role and has_main_role:
            roles_to_remove.append(main_role_id)
    
    # Apply role changes
    if roles_to_add or roles_to_remove:
        try:
            # Get role objects and filter out None values
            add_roles = [role for rid in roles_to_add if (role := main_member.guild.get_role(rid)) is not None]
            remove_roles = [role for rid in roles_to_remove if (role := main_member.guild.get_role(rid)) is not None]
            
            # Check bot's highest role position
            bot_member = main_member.guild.get_member(bot.user.id)
            if bot_member:
                bot_highest_position = max([r.position for r in bot_member.roles])
                
                # Filter roles the bot can actually assign (must be below bot's role)
                add_roles = [r for r in add_roles if r.position < bot_highest_position]
                remove_roles = [r for r in remove_roles if r.position < bot_highest_position]
            
            if add_roles:
                await main_member.add_roles(*add_roles, reason='Synced from Patreon server')
                logger.info(f'✅ Added roles to {main_member.display_name} ({main_member.id}): {[r.name for r in add_roles]}')
            
            if remove_roles:
                await main_member.remove_roles(*remove_roles, reason='Synced from Patreon server')
                logger.info(f'❌ Removed roles from {main_member.display_name} ({main_member.id}): {[r.name for r in remove_roles]}')
        except discord.Forbidden as e:
            logger.error(f'❌ Missing permissions to modify roles for {main_member.display_name} ({main_member.id}): {e}')
        except discord.HTTPException as e:
            logger.error(f'❌ HTTP error syncing roles for {main_member.display_name} ({main_member.id}): {e}')
        except Exception as e:
            logger.error(f'❌ Unexpected error syncing roles for {main_member.display_name} ({main_member.id}): {e}', exc_info=True)

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    """Handle member role updates in Patreon server."""
    if after.guild.id != PATREON_GUILD_ID:
        return
    
    if before.roles == after.roles:
        return
    
    # Only sync if a mapped role changed
    before_role_ids = {role.id for role in before.roles}
    after_role_ids = {role.id for role in after.roles}
    
    # Check if any mapped role changed
    mapped_roles_changed = any(
        (pid in before_role_ids) != (pid in after_role_ids)
        for pid in ROLE_MAPPING.keys()
    )
    
    if not mapped_roles_changed:
        return  # No relevant role changes
    
    # Find corresponding member in main guild
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    if not main_guild:
        return
    
    main_member = main_guild.get_member(after.id)
    if not main_member:
        # Try fetching if not cached
        try:
            main_member = await main_guild.fetch_member(after.id)
        except (discord.NotFound, discord.HTTPException):
            return
    
    # Sync roles
    await sync_member_roles(after, main_member)

@bot.event
async def on_member_join(member: discord.Member):
    """Handle new member joining Patreon server."""
    if member.guild.id != PATREON_GUILD_ID:
        return
    
    # Wait a bit for Patreon roles to be assigned (Patreon bot might assign roles)
    await asyncio.sleep(3)
    
    # Refresh member to get latest roles
    try:
        member = await member.guild.fetch_member(member.id)
    except (discord.NotFound, discord.HTTPException):
        return
    
    # Find corresponding member in main guild
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    if not main_guild:
        return
    
    main_member = main_guild.get_member(member.id)
    if not main_member:
        # Try fetching if not cached
        try:
            main_member = await main_guild.fetch_member(member.id)
        except (discord.NotFound, discord.HTTPException):
            return
    
    # Sync roles
    await sync_member_roles(member, main_member)

@bot.command(name='sync')
@commands.has_permissions(administrator=True)
async def manual_sync(ctx: commands.Context, member: Optional[discord.Member] = None):
    """Manually sync roles for a specific member or all members."""
    patreon_guild = bot.get_guild(PATREON_GUILD_ID)
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    
    if not patreon_guild or not main_guild:
        await ctx.send('❌ Could not find one or both guilds!')
        return
    
    if member:
        # Sync specific member
        patreon_member = patreon_guild.get_member(member.id)
        if not patreon_member:
            try:
                patreon_member = await patreon_guild.fetch_member(member.id)
            except (discord.NotFound, discord.HTTPException):
                await ctx.send(f'❌ Member not found in Patreon server!')
                return
        
        main_member = main_guild.get_member(member.id)
        if not main_member:
            try:
                main_member = await main_guild.fetch_member(member.id)
            except (discord.NotFound, discord.HTTPException):
                await ctx.send(f'❌ Member not found in Main server!')
                return
        
        await sync_member_roles(patreon_member, main_member)
        await ctx.send(f'✅ Synced roles for {member.mention}!')
    else:
        # Sync all members
        await ctx.send('🔄 Starting full sync... This may take a while.')
        synced_count = 0
        
        for patreon_member in patreon_guild.members:
            if patreon_member.bot:
                continue
            
            main_member = main_guild.get_member(patreon_member.id)
            if not main_member:
                # Try fetching if not cached
                try:
                    main_member = await main_guild.fetch_member(patreon_member.id)
                except (discord.NotFound, discord.HTTPException):
                    continue
            
            await sync_member_roles(patreon_member, main_member)
            synced_count += 1
            
            # Small delay to avoid rate limits
            if synced_count % 10 == 0:
                await asyncio.sleep(0.5)
        
        await ctx.send(f'✅ Full sync complete! Synced {synced_count} members.')

@bot.command(name='status')
@commands.has_permissions(administrator=True)
async def status(ctx: commands.Context):
    """Check bot status and configuration."""
    patreon_guild = bot.get_guild(PATREON_GUILD_ID)
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    
    embed = discord.Embed(title='Bot Status', color=discord.Color.blue())
    
    embed.add_field(
        name='Patreon Guild',
        value=patreon_guild.name if patreon_guild else '❌ Not found',
        inline=False
    )
    
    embed.add_field(
        name='Main Guild',
        value=main_guild.name if main_guild else '❌ Not found',
        inline=False
    )
    
    embed.add_field(
        name='Role Mappings',
        value=f'{len(ROLE_MAPPING)} role(s) configured',
        inline=False
    )
    
    if ROLE_MAPPING:
        mapping_text = '\n'.join([
            f'• {bot.get_guild(PATREON_GUILD_ID).get_role(pid).name if bot.get_guild(PATREON_GUILD_ID) else "Unknown"} → '
            f'{bot.get_guild(MAIN_GUILD_ID).get_role(mid).name if bot.get_guild(MAIN_GUILD_ID) else "Unknown"}'
            for pid, mid in list(ROLE_MAPPING.items())[:10]
        ])
        if len(ROLE_MAPPING) > 10:
            mapping_text += f'\n... and {len(ROLE_MAPPING) - 10} more'
        embed.add_field(name='Mappings', value=mapping_text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='reload')
@commands.has_permissions(administrator=True)
async def reload_mapping(ctx: commands.Context):
    """Reload role mappings from configuration."""
    patreon_guild = bot.get_guild(PATREON_GUILD_ID)
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    
    if not patreon_guild or not main_guild:
        await ctx.send('❌ Could not find one or both guilds!')
        return
    
    ROLE_MAPPING.clear()
    await build_role_mapping(patreon_guild, main_guild)
    await ctx.send(f'✅ Reloaded {len(ROLE_MAPPING)} role mapping(s)!')

# Health check for Railway
startup_time = datetime.now()

@bot.event
async def on_connect():
    """Called when the bot connects to Discord."""
    logger.info('🔌 Connected to Discord gateway')

@bot.event
async def on_disconnect():
    """Called when the bot disconnects from Discord."""
    logger.warning('⚠️  Disconnected from Discord gateway - will attempt to reconnect')

@bot.event
async def on_resumed():
    """Called when the bot resumes connection after a disconnect."""
    logger.info('✅ Resumed connection to Discord gateway')

@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler."""
    logger.error(f'❌ Error in event {event}:', exc_info=True)

# Run the bot with optimized settings for Railway
if __name__ == '__main__':
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error('❌ DISCORD_BOT_TOKEN environment variable is not set!')
        logger.error('   Please set it in Railway environment variables.')
        sys.exit(1)
    
    if not PATREON_GUILD_ID or PATREON_GUILD_ID == 0:
        logger.error('❌ PATREON_GUILD_ID environment variable is not set or invalid!')
        logger.error('   Please set it in Railway environment variables.')
        sys.exit(1)
    
    if not MAIN_GUILD_ID or MAIN_GUILD_ID == 0:
        logger.error('❌ MAIN_GUILD_ID environment variable is not set or invalid!')
        logger.error('   Please set it in Railway environment variables.')
        sys.exit(1)
    
    logger.info('🚀 Starting Discord bot...')
    logger.info(f'📋 Patreon Guild ID: {PATREON_GUILD_ID}')
    logger.info(f'📋 Main Guild ID: {MAIN_GUILD_ID}')
    logger.info(f'📋 Role mappings configured: {len(SYNC_ROLES)}')
    
    try:
        # Use reconnect=True for Railway (handles network issues)
        bot.run(token, reconnect=True, log_handler=None)
    except KeyboardInterrupt:
        logger.info('🛑 Bot stopped by user')
    except Exception as e:
        logger.error(f'❌ Fatal error: {e}', exc_info=True)
        sys.exit(1)

