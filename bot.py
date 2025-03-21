"""
Main Discord bot class.
Handles events and command registration.
"""
import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        intents.message_content = True  # To receive message content
        intents.members = True  # To receive member join/leave events
        
        super().__init__(command_prefix=command_prefix, intents=intents, help_command=None)
        
        # Register event handlers
        self.setup_events()
        
        # We'll load cogs in the on_ready event instead
        # since load_cogs is now an async method
    
    def setup_events(self):
        """Register event handlers"""
        @self.event
        async def on_ready():
            logger.info(f"Bot is ready! Logged in as {self.user} (ID: {self.user.id})")
            logger.info(f"Connected to {len(self.guilds)} guilds")
            
            # Load cogs
            await self.load_cogs()
            
            # Status is now handled by the RichPresence cog
        
        @self.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"Command not found. Use `{self.command_prefix}help` to see available commands.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Missing required argument. Use `{self.command_prefix}help {ctx.command}` for proper usage.")
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send("You don't have permission to use this command.")
            else:
                logger.error(f"Command error: {error}", exc_info=True)
                await ctx.send(f"An error occurred: {error}")
        
        @self.event
        async def on_guild_join(guild):
            logger.info(f"Bot joined a new guild: {guild.name} (ID: {guild.id})")
        
        @self.event
        async def on_message(message):
            # Don't respond to bot messages
            if message.author.bot:
                return
            
            # Log messages in DMs or when the bot is mentioned
            if message.guild is None or self.user in message.mentions:
                logger.info(f"Message from {message.author}: {message.content}")
            
            # Process commands
            await self.process_commands(message)
    
    async def load_cogs(self):
        """Load command modules (cogs)"""
        try:
            # Core functionality cogs
            await self.load_extension("cogs.utils")
            await self.load_extension("cogs.moderation")
            await self.load_extension("cogs.fun")
            await self.load_extension("cogs.admin")
            await self.load_extension("cogs.presence")
            await self.load_extension("cogs.language")
            await self.load_extension("cogs.welcome")
            await self.load_extension("cogs.music")
            await self.load_extension("cogs.help")
            
            # New functionality cogs
            await self.load_extension("cogs.actions")
            await self.load_extension("cogs.economy")
            await self.load_extension("cogs.games")
            await self.load_extension("cogs.marriage")
            await self.load_extension("cogs.pets")
            await self.load_extension("cogs.anime")
            await self.load_extension("cogs.meme")
            await self.load_extension("cogs.adventure")
            await self.load_extension("cogs.webhooks")
            await self.load_extension("cogs.levels")
            
            logger.info("Loaded all cogs successfully")
        except Exception as e:
            logger.error(f"Failed to load cogs: {e}", exc_info=True)
    
    # O comando help está definido no cog Help
