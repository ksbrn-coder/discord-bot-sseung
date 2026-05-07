import os
import discord
from discord import app_commands
from datetime import date, timedelta

MY_GUILD = discord.Object(id=1440241980528529598)

BASE_DATE = date(2026, 5, 2)
PVP_MAPS = [
    "봉인된 바위섬 (쟁탈전)",
    "영광의 평원 (쇄빙전)",
    "온살 하카이르 (계절 끝 합전)",
    "워코 치테 (연습전)",
    "봉인된 바위섬 (쟁탈전)",
    "카르테노 평원 (제압전)",
    "온살 하카이르 (계절 끝 합전)",
    "워코 치테 (연습전)"
]

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        await self.tree.sync(guild=MY_GUILD)
        print(f"명령어가 {MY_GUILD.id} 서버에 동기화되었습니다!")

    async def on_ready(self):
        game = discord.Game("/오늘전장 | 전장 로테이션 알림")
        await self.change_presence(status=discord.Status.online, activity=game)
        print(f'{self.user}이 로그인했습니다!')

client = MyBot()

def get_pvp_map(target_date):
    delta = (target_date - BASE_DATE).days
    return PVP_MAPS[delta % 8]

@client.tree.command(name="오늘전장", description="오늘의 전장 로테이션을 확인합니다.")
async def today_pvp(interaction: discord.Interaction):
    pvp_map = get_pvp_map(date.today())
    embed = discord.Embed(
        title="⚔️ 오늘 전장은?",
        description=f"오늘은 **{pvp_map}** 입니다.",
        color=0xe74c3c
    )
    embed.set_footer(text=f"기준일: {BASE_DATE.strftime('%Y-%m-%d')}")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="내일전장", description="내일의 전장 로테이션을 확인합니다.")
async def tomorrow_pvp(interaction: discord.Interaction):
    tomorrow = date.today() + timedelta(days=1)
    pvp_map = get_pvp_map(tomorrow)
    embed = discord.Embed(
        title="📅 내일의 전장 예보",
        description=f"내일의 전장은 **{pvp_map}** 입니다.",
        color=0x3498db
    )
    await interaction.response.send_message(embed=embed)

client.run(os.environ["DISCORD_BOT_TOKEN"])
