import disnake
from disnake.ext import commands, tasks
from datetime import datetime
import pytz
import asyncio
import os
TOKEN = os.environ.get('TOKEN')

# 创建一个 Intents 对象并启用所需的权限
intents = disnake.Intents.all()
# 创建一个 Bot 实例
bot = commands.Bot(command_prefix='!', intents=intents)
# 特定用户 ID
AUTHORIZED_USER_ID = 1240584393458712607  # 替换为实际用户 ID
# 存储被禁言的用户 ID
muted_users = set()

# 查询时区的城市及其时区
timezones = {
    "中国北京": "Asia/Shanghai",
    "日本东京": "Asia/Tokyo",
    "澳大利亚堪培拉": "Australia/Sydney",
    "美国洛杉矶": "America/Los_Angeles",
    "美国纽约": "America/New_York",
    "英国伦敦": "Europe/London",
    "俄罗斯莫斯科": "Europe/Moscow"
}

def is_authorized(interaction):
    return interaction.author.id == AUTHORIZED_USER_ID


@bot.event
async def on_ready():
    print(f"Bot 已上线！已登录为 {bot.user}")

@bot.slash_command(description="闭嘴")
async def 闭嘴(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
    muted_users.add(member.id)

@bot.slash_command(description="张嘴")
async def 张嘴(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
    muted_users.discard(member.id)

@bot.slash_command(description="奖励华为手表", )
async def 奖励华为手表(interaction: disnake.ApplicationCommandInteraction, role: disnake.Role, member: disnake.Member):
    await member.add_roles(role)

@bot.slash_command(description="你不配作为我的学生", )
async def 你不配作为我的学生(interaction: disnake.ApplicationCommandInteraction, role: disnake.Role, member: disnake.Member):
    await member.remove_roles(role)

@bot.slash_command(description="滚")
async def 滚(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
    await member.ban()

@bot.slash_command(description="滚回来")
async def 滚回来(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
    await member.unban()

@bot.slash_command(description="查询时区")
async def 查询时区(interaction: disnake.ApplicationCommandInteraction):
    
    await interaction.send(content=update_timezones())
      
  

def update_timezones():
  now = datetime.now()
  times = [f"{city}: {now.astimezone(pytz.timezone(tz)).strftime('%Y-%m-%d %H:%M:%S')}" for city, tz in timezones.items()]
  content = "\n".join(times)
  return content
    
@bot.event
async def on_message(message):
    if message.author.id in muted_users:
        await message.delete()
    if bot.user.mentioned_in(message):
        # 发送初始消息
        sent_message = await message.reply(content=update_timezones())
        while True:
            await sent_message.edit(content=update_timezones())
            await asyncio.sleep(10)

# 运行机器人
bot.run(TOKEN)  # 替换为您的机器人的令牌