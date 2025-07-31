import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "✅ Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

TOKEN = "MTM4NjEwNDIzMDk1MDk5ODA0Nw.GsqQwq.qaMi7SJZ7W5IcI3MHhK0c59uMcN7hiewQx0LL4"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"{bot.user} جاهز!")

@tree.command(name="اضافة_ايموجي", description="إضافة إيموجي من إيدي")
@app_commands.describe(emote_id="اكتب إيدي الإيموجي", name="اسم الإيموجي الجديد")
async def add_emoji(interaction: discord.Interaction, emote_id: str, name: str):
    if not interaction.user.guild_permissions.manage_emojis:
        await interaction.response.send_message("❌ لا تملك صلاحية `Manage Emojis`.", ephemeral=True)
        return

    try:
        emoji_url = f"https://cdn.discordapp.com/emojis/{emote_id}.png"
        emoji = await interaction.guild.create_custom_emoji(name=name, image=await (await bot.http._HTTPClient__session.get(emoji_url)).read())
        await interaction.response.send_message(f"✅ تم إضافة الإيموجي: <:{name}:{emoji.id}>")
    except Exception as e:
        await interaction.response.send_message(f"❌ فشل في إضافة الإيموجي: {e}", ephemeral=True)

keep_alive()
bot.run(TOKEN)
