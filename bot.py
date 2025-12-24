import discord
from discord.ext import commands
import os
import asyncio
from typing import Optional, Dict, List
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration from environment variables
PATREON_GUILD_ID = int(os.getenv('PATREON_GUILD_ID', '0'))
MAIN_GUILD_ID = int(os.getenv('MAIN_GUILD_ID', '0'))
SYNC_ROLES = os.getenv('SYNC_ROLES', '').split(',') if os.getenv('SYNC_ROLES') else []

# Role mapping: {patreon_role_id: main_role_id}
ROLE_MAPPING: Dict[int, int] = {}

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    
    # Get guilds
    patreon_guild = bot.get_guild(PATREON_GUILD_ID)
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    
    if not patreon_guild:
        logger.error(f'Patreon guild with ID {PATREON_GUILD_ID} not found!')
        return
    
    if not main_guild:
        logger.error(f'Main guild with ID {MAIN_GUILD_ID} not found!')
        return
    
    logger.info(f'Connected to Patreon guild: {patreon_guild.name}')
    logger.info(f'Connected to Main guild: {main_guild.name}')
    
    # Build role mapping if SYNC_ROLES is configured
    if SYNC_ROLES:
        await build_role_mapping(patreon_guild, main_guild)
    
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
    for member in patreon_guild.members:
        if member.bot:
            continue
        
        # Find corresponding member in main guild
        main_member = main_guild.get_member(member.id)
        if not main_member:
            continue
        
        # Sync roles
        await sync_member_roles(member, main_member)
        synced_count += 1
    
    logger.info(f'Initial sync complete! Synced {synced_count} members.')

async def sync_member_roles(patreon_member: discord.Member, main_member: discord.Member):
    """Sync roles from Patreon member to Main member."""
    roles_to_add = []
    roles_to_remove = []
    
    # Get current roles in main server
    main_role_ids = {role.id for role in main_member.roles if role.id != main_member.guild.id}
    
    # Check which roles should be added/removed
    for patreon_role_id, main_role_id in ROLE_MAPPING.items():
        has_patreon_role = any(role.id == patreon_role_id for role in patreon_member.roles)
        has_main_role = main_role_id in main_role_ids
        
        if has_patreon_role and not has_main_role:
            roles_to_add.append(main_role_id)
        elif not has_patreon_role and has_main_role:
            roles_to_remove.append(main_role_id)
    
    # Apply role changes
    if roles_to_add or roles_to_remove:
        try:
            # Get role objects
            add_roles = [main_member.guild.get_role(rid) for rid in roles_to_add if main_member.guild.get_role(rid)]
            remove_roles = [main_member.guild.get_role(rid) for rid in roles_to_remove if main_member.guild.get_role(rid)]
            
            if add_roles:
                await main_member.add_roles(*add_roles, reason='Synced from Patreon server')
                logger.info(f'Added roles to {main_member}: {[r.name for r in add_roles]}')
            
            if remove_roles:
                await main_member.remove_roles(*remove_roles, reason='Synced from Patreon server')
                logger.info(f'Removed roles from {main_member}: {[r.name for r in remove_roles]}')
        except discord.Forbidden:
            logger.error(f'Missing permissions to modify roles for {main_member}')
        except Exception as e:
            logger.error(f'Error syncing roles for {main_member}: {e}')

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    """Handle member role updates in Patreon server."""
    if after.guild.id != PATREON_GUILD_ID:
        return
    
    if before.roles == after.roles:
        return
    
    # Find corresponding member in main guild
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    if not main_guild:
        return
    
    main_member = main_guild.get_member(after.id)
    if not main_member:
        return
    
    # Sync roles
    await sync_member_roles(after, main_member)

@bot.event
async def on_member_join(member: discord.Member):
    """Handle new member joining Patreon server."""
    if member.guild.id != PATREON_GUILD_ID:
        return
    
    # Wait a bit for roles to be assigned
    await asyncio.sleep(2)
    
    # Find corresponding member in main guild
    main_guild = bot.get_guild(MAIN_GUILD_ID)
    if not main_guild:
        return
    
    main_member = main_guild.get_member(member.id)
    if not main_member:
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
        main_member = main_guild.get_member(member.id)
        
        if not patreon_member or not main_member:
            await ctx.send(f'❌ Member not found in one or both servers!')
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
                continue
            
            await sync_member_roles(patreon_member, main_member)
            synced_count += 1
        
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

# Run the bot
if __name__ == '__main__':
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error('DISCORD_BOT_TOKEN environment variable is not set!')
        exit(1)
    
    if not PATREON_GUILD_ID or not MAIN_GUILD_ID:
        logger.error('PATREON_GUILD_ID and MAIN_GUILD_ID must be set!')
        exit(1)
    
    bot.run(token)

