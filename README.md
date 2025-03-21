# Discord Bot

A multipurpose Discord bot built with Python and discord.py.

## Features

- Command handling with prefix recognition
- Help command system
- Utility commands
- Moderation commands
- Fun commands
- Welcome system for new members
- Brazilian Portuguese language support
- Rich presence with streaming status
- Error handling for commands
- Event logging

## Commands

### Utility Commands
- `!help [command]` - Shows help information for all commands or a specific command
- `!ping` - Check the bot's latency
- `!serverinfo` - Display information about the current server
- `!roll [NdN]` - Roll dice in NdN format (e.g., 2d6)
- `!userinfo [member]` - Display information about a user

### Moderation Commands
- `!kick @member [reason]` - Kick a member from the server
- `!ban @member [reason]` - Ban a member from the server
- `!unban user_id [reason]` - Unban a user by their ID
- `!purge amount` - Delete a specified number of messages
- `!mute @member [duration] [reason]` - Mute a member in the server

### Fun Commands
- `!8ball <question>` - Ask the magic 8ball a question
- `!coinflip` - Flip a coin
- `!choose option1, option2, ...` - Choose between multiple options
- `!fact` - Get a random fun fact
- `!joke` - Get a random joke
- `!pergunta <question>` or `!ask <question>` - Ask Kimiko AI any question for an original and insightful response

### Brazilian Portuguese (PT-BR) Commands
- `!ptbr` - Show Brazilian Portuguese command menu
- `!ptbr help` - Show help for Brazilian Portuguese commands
- `!ptbr greet` - Get a random greeting in Portuguese
- `!ptbr slang [term]` - Show Brazilian slang with translations
- `!ptbr joke` - Get a random joke in Portuguese
- `!ptbr expression` - Learn a common Brazilian expression
- `!ptbr translate [text]` - Translate text to Portuguese

### Welcome System Commands
- `!welcome` - Show current welcome system configuration
- `!welcome channel #channel` - Set the welcome message channel
- `!welcome toggle` - Toggle welcome system on/off
- `!welcome dm` - Toggle direct message welcomes on/off
- `!welcome test` - Test the welcome message

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install discord.py python-dotenv
   ```
3. Create a `.env` file in the root directory (use `.env.example` as a template)
4. Add your Discord bot token to the `.env` file:
   ```
   DISCORD_TOKEN=your_discord_token_here
   ```
5. Run the bot:
   ```
   python main.py
   ```

## Development

For development, you can use the included development script:

```
python run_dev.py
```

This script includes additional logging and uses a different command prefix (`!!` instead of `!`) to avoid conflicts with production bots.

To run in debug mode with extra logging:

```
python run_dev.py --debug
```

## Requirements

- Python 3.8 or higher
- discord.py
- python-dotenv

## Adding the Bot to Your Server

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select your existing bot
3. Go to the "Bot" tab and copy your token (this goes in the `.env` file)
4. Go to the "OAuth2" tab, then "URL Generator"
5. Select the "bot" scope and choose appropriate permissions
6. Use the generated URL to add the bot to your server

## Voice Functionality (Optional)

To enable voice functionality, install the PyNaCl library:
```
pip install PyNaCl
```

## License

This project is available under the MIT License.
   