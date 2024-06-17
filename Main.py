import os
import discord
import shutil
import asyncio
from PIL import ImageGrab
from discord.ext import commands

# Set the Discord bot token
TOKEN = "YOUR DISCORD TOKEN HERE"

# Set the directory where you want to save the screenshots
screenshot_dir = "THE DIRECTORY FOR YOUR SCREENSHOTS HERE"

# Create the directory if it doesn't exist
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Define the intents
intents = discord.Intents.all()

# Create a Discord bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

async def capture_screenshot():
    # Calculate the region for the middle center with a height of 50 pixels
    screen_width, screen_height = ImageGrab.grab().size
    left = (screen_width - 800) // 2  # Center horizontally
    top = (screen_height - 50) // 2  # Center vertically
    width, height = 650, 600

    # Capture the screenshot with the specified region
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))

    # Set the output file path
    filename = f"{screenshot_dir}/screenshot.png"
    screenshot.save(filename)

    return filename

async def send_screenshot():
    try:
        channel_id = 1168296240845426852  # Replace with your channel ID
        channel = bot.get_channel(channel_id)

        while True:
            screenshot = await capture_screenshot()

            # Send the screenshot as a file
            await channel.send(file=discord.File(screenshot))

            # Rename the current screenshot to "latest_screenshot.png"
            shutil.move(screenshot, "latest_screenshot.png")

            # Sleep for a while before capturing the next screenshot
            

    except KeyboardInterrupt:
        print("\nScreen capture terminated.")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    # Run the send_screenshot task concurrently with the bot
    asyncio.create_task(send_screenshot())

# Run the bot
bot.run(TOKEN)
