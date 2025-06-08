import discord
from discord.ext import commands

from bapral.application.rectangle_service import RectangleService


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ここどうにかしたい
service = RectangleService(blur_depth=5, template_dir="templates")


@bot.event
async def on_ready():
    print("Bot is ready.")
    
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.attachments:
        for attachment in message.attachments:
            if any(
                attachment.filename.lower().endswith(ext)
                for ext in ['png', 'jpg', 'jpeg']
            ):
                img = await attachment.read()
                
                rect, own_labels, opp_labels = service.process_image(img)
                
                if rect:
                    own_str = " ".join(own_labels) if own_labels else "None"
                    opp_str = " ".join(opp_labels) if opp_labels else "None"
                    
                    await message.channel.send(
                        f"自分側:{own_str}\n相手側:{opp_str}"
                    )
                else:
                    await message.channel.send("何も検出できませんでした")