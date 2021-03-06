import discord
import random
from captcha.image import ImageCaptcha, _Captcha
from discord import message
from discord import file
from discord.utils import get
import asyncio
from discord.http import Route
import datetime

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

token = "토큰"
channel = "인증채널 ID"
log = "인증로그 ID"
gmsg =  '상태메세지', '1', '2', '3', '4', '5'

@client.event
async def on_ready(): 
  async def message(games):
    await client.wait_until_ready()

    while not client.is_closed():
        for g in games:
            await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
            await asyncio.sleep(10)

  print("=====================================\n봇이 로그인 & 실행 되었습니다.\n=====================================\n[ 봇정보 ]\nID : {}\nNAME : {}\n버전 : {}\n=====================================".format(client.user.id, client.user.name, discord.__version__))

  await message([gmsg])

@client.event
async def on_message(message):
    if message.content.startswith("!인증"):
        if not message.channel.id == int(channel):
            await message.channel.purge(limit=1)
            return

        a = ""
        Captcha_img = ImageCaptcha()
        for i in range(6):
            a += str(random.randint(0, 9))

        name = str(message.author. id) + ".png"
        Captcha_img.write(a, name)

        embed = discord.Embed(title="인증절차", description=f"{message.author.mention}님, 서버를 이용하시려면, 인증을 해야합니다.\n여기에 아래의 1분이내에, 인증번호를 입력해주세요!", color=0x7289DA, timestamp=message.created_at)
    
        verify = await message.author.send(embed=embed)
        img = await message.author.send(file=discord.File(name))
        

        def check(msg):
            return msg.author == message.author and msg.author == message.author

        try:
            msg = await client.wait_for("message", timeout=60, check=check)

        except:

            embed = discord.Embed(title="시간초과", description="{}님이 시간초과로 인해 인증실패하였습니다.".format(message.author.mention), color=0x43B481, timestamp=message.created_at)
            await client.get_channel(int(log)).send(embed=embed)

            await verify.delete()
            await img.delete()
            embed = discord.Embed(title="인증 시간초과", description="<a:a_Time_out:852102621204054016> {}님, 인증에 실패 하였습니다. 다시시도 해주세요!".format(message.author.mention), color=0xFCB801, timestamp=message.created_at)
            await message.author.send(embed=embed)
            await message.channel.purge(limit=1)
            
            return

        if msg.content == a:
            embed = discord.Embed(title="성공", description="{}님이 인증에 성공하였습니다!".format(message.author.mention), color=0x43B481, timestamp=message.created_at)
            await client.get_channel(int(log)).send(embed=embed)

            await verify.delete()
            await img.delete()
            embed = discord.Embed(title="인증성공", description="<a:a_Success:852102590589566996> {}님, 인증이 완료 되었습니다.".format(message.author.mention), color=0x43B481, timestamp=message.created_at)
            await message.channel.purge(limit=1)
            await message.author.send(embed=embed)

            await asyncio.sleep(3)
            await message.author.add_roles(get(message.author.guild.roles, name="User"))

        else:
                
                embed = discord.Embed(title="실패", description="{}님이 잘못된 코드로 인해 인증에 실패하였습니다.".format(message.author.mention), color=0xF04947, timestamp=message.created_at)
                await client.get_channel(int(log)).send(embed=embed)

                await verify.delete()
                await img.delete()
                embed = discord.Embed(title="인증실패", description="<a:a_Error:852102604473368596> {}님, 인증에 실패 하였습니다. 다시시도 해주세요!".format(message.author.mention), color=0xF04947, timestamp=message.created_at)
                await message.author.send(embed=embed)

client.run(token)
