import discord
import os
import time
import random
import discord.ext
from discord.utils import get
from asyncio import sleep as s
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#from tinydb import TinyDB, Query
from datetime import datetime
from random import randint
import math
from threading import Thread
import itertools
import asyncio
import psycopg2
import psycopg2.extras

#import sqlite3

#^ basic imports for other features of discord.py and python ^

# !beg - Cooldown of 10 seconds, gives you 25-250 currency, random
# !hourly - Cooldown of 1 hour, gives you 500 currency
# !daily - Cooldown of 1 day, gives you 1500 currency
# !balance / !bal - Shows the amount of currency you have.
# !gift - gift another user currency max 1500 per hour 
# !work - Cooldown of 1 hour, Gives you a simple task such as sending an emoji/text and gives you 2,500 currency. (more difficult, this can be one of the last ideas)

#db = TinyDB("db.json")
#accounts = db.table("accounts")
DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='require')
#cursor_factory=psycopg2.extras.DictCursor
#database = sqlite3.connect('db.db')
#database.row_factory = sqlite3.Row
cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)

#create table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL, 
    begtime TEXT,
    hourtime TEXT,
    dailytime TEXT,
    worktime TEXT,
    gifttime TEXT,
    fishtime TEXT,
    arttime TEXT,
    hunttime TEXT,
    traveltime TEXT,
    twittertime TEXT,
    yttime TEXT,
    investtime TEXT,
    reddittime TEXT,
    buytime TEXT,
    digtime TEXT,
    igtime TEXT
  );
''')

database.commit()
cursor.close()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix=['heat ', 'HEAT','Heat'],case_insensitive=True)
client.remove_command("help")
#put your own prefix here
token = "ODU1NTU2NDA3NDQwODM0NTcw.YM0M_w.8RxIL0VELBgaoLbynbt37JhXTL8"

#obj.strftime(’%Y-%m-%dT%H:%M:%S’)
#datetime.strptime(s, ’%Y-%m-%dT%H:%M:%S’)
def dateString(obj):
  return obj.strftime("%Y-%m-%dT%H:%M:%S")

def dateObject(string):
  return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")

def createUser(id):
  cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cursor.execute("SELECT * FROM accounts WHERE id = %s;", [id])
  results = cursor.fetchall()
  #results = accounts.search(user.id == id)
  now = datetime.now()
  now_str = dateString(now)
  if len(results) == 0:
    #accounts.insert({"id": id, "balance": 0, "begtime": now_str, "hourtime": now_str, "dailytime": now_str, "worktime": now_str, "gifttime": now_str, "fishtime": now_str, "simptime": now_str, "cooltime": now_str, "sharetime": now_str, "hunttime": now_str, "traveltime": now_str, "twittertime": now_str, "yttime": now_str, "investtime": now_str, "reddittime": now_str, "8btime": now_str, "iqtime": now_str, "losertime": now_str, "noobtime": now_str, "protime": now_str, "strafetime": now_str, "sustime": now_str, "wintime": now_str, "addtime": now_str, "subtime": now_str, "divtime": now_str, "multtime": now_str, "helptime": now_str, "buytime":})
    cursor.execute('''INSERT INTO accounts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (id, 0, now_str, now_str ,now_str ,now_str ,now_str ,now_str ,now_str ,now_str ,now_str ,now_str ,now_str ,now_str, now_str , now_str , now_str, now_str)) 
    database.commit()
    cursor.close()
    return True
  return False

'''
def read_db(filename):
  with open(f"{cwd}/bot_config/{filename}.db", "r") as file:
    data = db.load(file)
  return data


def write_db(data, filename):
  with open(f"{cwd}/bot_config/{filename}.db", "w") as file:
    db.dump(data, file, indent=4)
'''

def findPerson(id):
  new = False #to check if we make new user
  #user = Query()
  #results = accounts.search(user.id == id) 
  cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cursor.execute("SELECT * FROM accounts WHERE id = %s", (id))
  results = cursor.fetchall()
  #search for the user
  if len(results) == 0: #user not found, make new
    createUser(id) #add new user
    new = True
    #results = accounts.search(user.id == id)
    cursor.execute("SELECT * FROM accounts WHERE id = %s", (id))
    results = cursor.fetchall()
    cursor.close() 
    #search for the user we just added
  return (results[0], new) #grab user

'''
@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")
  print("bot online") #will print "bot online" in the console when the bot is online
  for guild in client.guilds:
    for member in guild.members:
      print(member)
      if member.bot == False:
        createUser(member.id)'''

@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use heat help <category> for extra information about a command.", color = ctx.author.color)
  em.add_field(name = "`Currency`", value = "**Commands** ")
  em.add_field(name = "`Fun`", value = "**Commands**")
  em.add_field(name = "`math`" , value = "**Commands**")
  await ctx.send(embed = em)

@help.command()
async def currency(ctx):
  em = discord.Embed(title = "Currency Commands", description = "`balance` `daily` `hourly` `beg`\n`share` `fish` `hunt` `art` `dig` `instagram` \n`invest` `travel` `twitter` `youtube` `reddit` ", color = ctx.author.color)

  em.add_field(name = "**How To**", value = "Use heat help <command>")

  await ctx.send(embed = em)

@help.command()
async def fun(ctx):
  em = discord.Embed(title = "Fun Commands", description = "`eightball` `coolrate` `iq` `loserrate`\n`height` `noobrate` `prorate` `simprate`\n`straferate` `susrate` `winnerrate`", color = ctx.author.color)

  em.add_field(name = "**How To**", value = "Use heat help <command>")

  await ctx.send(embed = em)

@help.command()
async def math(ctx):
  em = discord.Embed(title = "Math Commands", description = "`add` `subtract` `divide` `multiply`", color = ctx.author.color)

  em.add_field(name = "**How To**", value = "Use heat help <command>")

  await ctx.send(embed = em)

@help.command()
async def multiply(ctx):
  em = discord.Embed(title = "Multiply", description = "You can figure out the answer to a multiplication problem.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat multiply # #")

  await ctx.send(embed = em)

@help.command()
async def reddit(ctx):
  em = discord.Embed(title = "Reddit", description = "You can get currency for being upvoted, or lose currency for being downvoted.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat divide # #")

  await ctx.send(embed = em)

@help.command()
async def divide(ctx):
  em = discord.Embed(title = "Divide", description = "You can figure out the number to a division problem.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat divide # #")

  await ctx.send(embed = em)

@help.command(aliases=['cf'])
async def coinflip(ctx):
  em = discord.Embed(title = "Coin Flip", description = "Chooses heads, or tails randomly. Sub-Command is heat cf.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat coinflip")

  await ctx.send(embed = em)

@help.command()
async def subtract(ctx):
  em = discord.Embed(title = "Subtract", description = "You can figure out the answer to a subtraction problem.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat subtract # #")

  await ctx.send(embed = em)


@help.command()
async def add(ctx):
  em = discord.Embed(title = "Add", description = "You can figure out the answer to an addition problem.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat add # #")

  await ctx.send(embed = em)

@help.command()
async def winnerrate(ctx):
  em = discord.Embed(title = "Winner Rate", description = "You can see if you win or lose.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat winnerrate")

  await ctx.send(embed = em)

@help.command()
async def susrate(ctx):
  em = discord.Embed(title = "Sus Rate", description = "You can see how sus you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat susrate")

  await ctx.send(embed = em)

@help.command()
async def straferate(ctx):
  em = discord.Embed(title = "Strafe Rate", description = "You can see how similar you are to Strafe.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat straferate")

  await ctx.send(embed = em)

@help.command()
async def simprate(ctx):
  em = discord.Embed(title = "Simp Rate", description = "You can see how much of a simp you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat simprate")

  await ctx.send(embed = em)

@help.command()
async def prorate(ctx):
  em = discord.Embed(title = "Pro Rate", description = "You can see how pro you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat prorate")

  await ctx.send(embed = em)

@help.command()
async def noobrate(ctx):
  em = discord.Embed(title = "Noob Rate", description = "You can see how much of a noob you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat noobrate")

  await ctx.send(embed = em)

@help.command()
async def height(ctx):
  em = discord.Embed(title = "Height", description = "You can see how tall you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat height")

  await ctx.send(embed = em)

@help.command()
async def loserrate(ctx):
  em = discord.Embed(title = "Loser Rate", description = "You can see how much of a loser you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat loserrate")

  await ctx.send(embed = em)

@help.command()
async def iq(ctx):
  em = discord.Embed(title = "IQ", description = "See how smart you are, the bot will tell you if you're dumb, or smart.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat iq")

  await ctx.send(embed = em)

@help.command(aliases= ['8b','8ball'])
async def eightball(ctx):
  em = discord.Embed(title = "Eight Ball", description = "Ask questions to the magic 8ball for a shocking suprise. Sub-Command's are 8b and 8ball.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat eightball")

  await ctx.send(embed = em)

@help.command()
async def coolrate(ctx):
  em = discord.Embed(title = "Cool Rate", description = "You can see how cool you are.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat coolrate")

  await ctx.send(embed = em)

@help.command(aliases=['bal'])
async def balance(ctx):
  em = discord.Embed(title = "Balance", description = "Shows whoevers balance is being checked. Sub-Command is bal.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat balance <user>")

  await ctx.send(embed = em)

@help.command()
async def daily(ctx):
  em = discord.Embed(title = "Daily", description = "Gives you 5000-15000 currency, Cooldown is 1 day.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat daily")

  await ctx.send(embed = em)

@help.command()
async def bet(ctx):
  em = discord.Embed(title = "Bet", description = "Allows you to bet 1,000 - 50,000 coins. You win big or you lose. ", color = ctx.author.color)
  em.add_field(name = "**SYNTAX**", value = "heat bet <amount>")

  await ctx.send(embed = em)

@help.command()
async def hourly(ctx):
  em = discord.Embed(title = "Hourly", description = "Gives you 1000 currency, Cooldown is 1 hour.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat hourly")

  await ctx.send(embed = em)

@help.command()
async def beg(ctx):
  em = discord.Embed(title = "Beg", description = "A random person gives you a random amount of currency.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat beg")

  await ctx.send(embed = em)

@help.command(aliases = ['give'])
async def share(ctx):
  em = discord.Embed(title = "Share", description = "You give your currency to another user, who isn't yourself. Sub-Command is give.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat give @user <# of currency>")

  await ctx.send(embed = em)

@help.command()
async def fish(ctx):
  em = discord.Embed(title = "Fish", description = "You can fish, which can make you earn or lose currency.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat fish")

  await ctx.send(embed = em)

@help.command()
async def hunt(ctx):
  em = discord.Embed(title = "Hunt", description = "You can hunt, which can make you earn or lose currency.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat hunt")

  await ctx.send(embed = em)

@help.command()
async def art(ctx):
  em = discord.Embed(title = "Art", description = "A famous artist will buy your art, giving you currency. You can also flop and lose currency from supplies.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat art")

  await ctx.send(embed = em)

@help.command()
async def dig(ctx):
  em = discord.Embed(title = "Dig", description = "You can dig, either find potatoes and sell them, or fall in lava and lose currency.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat dig")

  await ctx.send(embed = em)

@help.command(aliases = ['ig'])
async def instagram(ctx):
  em = discord.Embed(title = "Instagram", description = "Post an instagram story, get 1 currency per thousand views. Sub-Command is heat ig", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat instagram")

  await ctx.send(embed = em)

@help.command()
async def invest(ctx):
  em = discord.Embed(title = "Invest", description = "Invest in random comapnies/crypto currency. Make or lose money.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat invest")

  await ctx.send(embed = em)

@help.command()
async def travel(ctx):
  em = discord.Embed(title = "Travel", description = "Travel the world and get paid, or lose money from expenses.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat travel")

  await ctx.send(embed = em)

@help.command(aliases = ['yt'])
async def youtube(ctx):
  em = discord.Embed(title = "YouTube", description = "Post your videos to youtube and make money, or lose....", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat youtube")

  await ctx.send(embed = em)

@help.command()
async def twitter(ctx):
  em = discord.Embed(title = "Twitter", description = "Post on twitter, you may trend and get currency.", color = ctx.author.color)

  em.add_field(name = "**SYNTAX**", value = "heat twitter")

  await ctx.send(embed = em)

@client.command(aliases=['bal'])
async def balance(ctx, user: discord.Member = None):
  #check other user
  if user:
    person, new = findPerson(user.id) #find other user

    if new: #if theyre new embed 0 
      embedv = discord.Embed(title=f"{user.name}'s Balance", description="Their balance is <:pd_heatcoin:858357730951823360> 0.", color =0x170B0C)
    else: #otherwise embed balance
      embedv = discord.Embed(title=f"{user.name}'s Balance", description=f"Their balance is <:pd_heatcoin:858357730951823360> {person['balance']}.", color =0x8BEB09)
  #ourself
  else:
    person, new = findPerson(ctx.author.id)

    if new: 
      embedv = discord.Embed(title=f" {ctx.author.name}'s Balance", description="Your balance is <:pd_heatcoin:858357730951823360> 0.", color=0xFF0000)
    else:
      embedv = discord.Embed(title=f"{ctx.author.name}'s Balance", description=f"Your balance is <:pd_heatcoin:858357730951823360> {person['balance']}.", color=0x2E2EFE)
  #return the embed
  await ctx.send(embed = embedv)

ppl = ['Obama','Heat','Venom','Trump','Dream','Impostor from amongus','Sussy Baka','Default Skin','Taylor Swift','Pewdiepie','Dhar mann','Edward','Skarz','Doggy','Chris Pratt','Adam Sandler','Selena Gomez','Adelle','Mrbeast','DemonYuh','ArshCrossover','Kanye West','Joe Biden', 'Trump','Doge','Karl Jacobs','Dom Torreto', 'Aunt Susan','yo mama','Pablo','Beluga']

#share 
@client.command(aliases=['give'])
async def share(ctx, recipient: discord.Member = None, amount = 0):
  amount = round(int(amount)* .97)
  if recipient == None:
    embedv = discord.Embed(title=f"You need to choose someone to send currency to.", color=0x9209D7)
  if amount > 0 and recipient:
     gifter, newAuthor = findPerson(ctx.author.id)
     recipientObj, new = findPerson(recipient.id)
  embedv = discord.Embed(title="Your number must be positive.", color=0x8BEB09)
  if recipient.id == ctx.author.id:
    embedv = discord.Embed(title=f"You can't share with yourself.", color=0x9209D7)
  elif gifter['balance'] < amount:
    embedv = discord.Embed(title=f"You're too broke, you only have {gifter['balance']} ", color=0x9209D7)
  else:
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s
      WHERE id = %s;
    ''', (gifter['balance'] - amount, ctx.author.id))
    
    cursor.execute('''
      UPDATE accounts
      SET balance = %s
      WHERE id = %s;
    ''', (recipientObj['balance'] + amount, recipient.id))
    database.commit()
    cursor.close()
    #user = Query()
    #accounts.update({"balance": gifter['balance'] - amount}, user.id == ctx.author.id)
    #accounts.update({"balance": recipientObj['balance'] + amount}, user.id == recipient.id)
    gifter, newAuthor = findPerson(ctx.author.id)
    embedv = discord.Embed(title=f"You sent <:pd_heatcoin:858357730951823360> {amount} to {recipient} with a 3% tax, you now have <:pd_heatcoin:858357730951823360> {gifter['balance']} ", color=0x8BEB09)
  await ctx.send(embed = embedv)

colors =  [0x09CCEB, 0xEB2F09, 0xEB7709, 0xE4EB09, 0x8BEB09, 0x09EB10, 0x1F6021, 0x0FE7EA, 0x0F65EA, 0xAFC7EB, 0x908DE7, 0x413F8C, 0x6009D7, 0x9209D7, 0xD709CB, 0xD70964, 0xD70919, 0x170B0C, 0xF5EBEC]
@client.command()
async def beg(ctx):
  person, new = findPerson(ctx.author.id)
  current = datetime.now()
  print(person)
  print(person['begtime'])
  difference = current - dateObject(person['begtime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    toAdd = randint(25, 251)
    #user = Query()
    #accounts.update({"balance": person['balance'] + toAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, begtime = %s
      WHERE id = %s;
    ''', (person['balance'] + toAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    embedv = discord.Embed(title=f" {ctx.author.name} became a beggar", description=f"{random.choice(ppl)} gave {ctx.author.name} <:pd_heatcoin:858357730951823360> {toAdd}  for begging.", color =0x0FE7EA)
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)



# STATUS MESSAGE

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=f"I am in {len(client.guilds)} servers! | prefix: heat"))
 



@client.command()
async def simprate(ctx, user: discord.Member = None):
  simp = randint(1,100)
  if simp > 50:
    embedv = discord.Embed(title=f"{ctx.author.name}'s simprate", description=f" :neutral_face: Your simprate is {simp}. {random.choice(ppl)} is dissapointed in you.", color=0x33ccff)
  else:
    embedv = discord.Embed(title=f"{ctx.author.name}'s simprate", description=f" :thumbsup: Your simprate is {simp}. You aren't a simp!", color=0xecb3ff)
  await ctx.send(embed = embedv)


@client.command()
async def ping(ctx):
    embedv = discord.Embed(title="Pong!", description="pong", color=0xFF0000)
    await ctx.send(embed = embedv)



@client.command()
async def coolrate(ctx):
  cool = randint(1,100)
  if cool > 50:
    embedv = discord.Embed(title=f"{ctx.author.name}'s coolrate", description=f" :sunglasses: Your coolrate is {cool}. You're a very cool person!", color=0x75162F)
  else: 
    embedv = discord.Embed(title=f" {ctx.author.name}'s coolrate", description=f" :nerd: Your coolrate is {cool}. You're not very cool.", color=0x75162F)
  await ctx.send(embed = embedv)

@client.command()
async def fish(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['fishtime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    fishAdd = randint(-100,200)
    #user = Query()
    #accounts.update({"balance": person['balance'] + fishAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, fishtime = %s
      WHERE id = %s;
    ''', (person['balance'] + fishAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if fishAdd < 0:
      embedv = discord.Embed(title=f"{ctx.author.name} went fishing!", description=f"{ctx.author.name} found a bill in the water, now you need to pay <:pd_heatcoin:858357730951823360> {fishAdd}  lol.", color =0x10E06F) 
    else: 
      embedv = discord.Embed(title=f"{ctx.author.name} went fishing!", description=f"{ctx.author.name} found a  :fish: worth <:pd_heatcoin:858357730951823360> {fishAdd}. You sold it to {random.choice(ppl)}.", color =0xFF0000 ) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command()
async def hunt(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['hunttime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    huntAdd = randint(50,350)
    #user = Query()
    #accounts.update({"balance": person['balance'] + huntAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, hunttime = %s
      WHERE id = %s;
    ''', (person['balance'] + huntAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if huntAdd < 200:
      embedv = discord.Embed(title=f"{ctx.author.name} went hunting!", description=f"{ctx.author.name} found a tiny :boar:  worth <:pd_heatcoin:858357730951823360> {huntAdd} .", color =0xd24dff) 
    else:
      embedv = discord.Embed(title=f"<a:pd_catshoot:858092196237148180> {ctx.author.name} went hunting!", description=f"{ctx.author.name} found a big :deer:  worth <:pd_heatcoin:858357730951823360> {huntAdd}. You sold it to {random.choice(ppl)}.", color =0xd24dff) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0xd24dff) 
  await ctx.send(embed = embedv)

@client.command()
async def crime(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['crimetime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    crimeAdd = randint(-100,200)
    #user = Query()
    #accounts.update({"balance": person['balance'] + crimeAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, crimetime = %s
      WHERE id = %s;
    ''', (person['balance'] + crimeAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if crimeAdd > 0:
      embedv = discord.Embed(title=f" {ctx.author.name} decided to be naughty and rob a store...", description=f"{ctx.author.name} stole a :pizza:  worth <:pd_heatcoin:858357730951823360> {crimeAdd} , and succeeded! Turns out, it was {random.choice(ppl)}'s pizza.'", color =0x008000 ) 
    else:
      embedv = discord.Embed(title=f"    {ctx.author.name} decided to be naughty and rob a store...", description=f"{ctx.author.name} got caught stealing a <a:pd_trash:858350240339066900>  and was fined <:pd_heatcoin:858357730951823360> {crimeAdd} , better luck next time!", color =0xFF0000 ) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0xd24dff) 
  await ctx.send(embed = embedv)

@client.command()
async def invite(ctx):
    embedv = discord.Embed(title="Invites!", description=" :robot: [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=855556407440834570&permissions=347136&scope=bot)  \n :sunglasses: [Support Server](https://discord.gg/2wFp6G78Wy)", color=0xffff4d)
    await ctx.send(embed = embedv)

@client.command()
async def rules(ctx):
    embedv = discord.Embed(title="**Currency Bot rules**", description="1. No auto typing, if you’re caught you’ll be removed from the bot. \n 2. No spamming, if you are caught you’ll be data wiped and removed from the bot if you continue. \n3. Follow discord tos, don’t use the bot to break tos.\n4. Don’t advertise with any of the bots commands!\n5. Don’t trade our currency for other types of currency (when share comes out)", color=0xffff4d)
    await ctx.send(embed = embedv)

@client.command()
async def dig(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['digtime'])
  seconds = round(difference.total_seconds())
  foods = [':eggplant:', ':potato:', ':lemon:', ':carrot:', ':grapes: ']
  if (seconds > 3 or new):
    digAdd = randint(-100,250)
    #user = Query()
   # accounts.update({"balance": person['balance'] + digAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, digtime = %s
      WHERE id = %s;
    ''', (person['balance'] + digAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if digAdd > 0:
      embedv = discord.Embed(title=f" {ctx.author.name} went digging!", description=f"{ctx.author.name} found a {random.choice(foods)} worth <:pd_heatcoin:858357730951823360> {digAdd}! You sold it to {random.choice(ppl)}.", color =0x008000) 
    else:
      embedv = discord.Embed(title=f"  {ctx.author.name} went digging,and fell into lava...", description=f"{ctx.author.name} fell into Lava and lost <:pd_heatcoin:858357730951823360> {digAdd} .", color =0xFFA500) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command()
async def noobrate(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    noob = randint(1,100)
    if noob > 50:
      embedv = discord.Embed(title=f" {ctx.author.name}'s noobrate", description=f" :neutral_face:  Your noob rate is {noob}. Get better!", color=0x0F1272)
    else: 
      embedv = discord.Embed(title=f":tada: {ctx.author.name}'s noobrate", description=f" Your noob rate is {noob}. You clearly aren't a noob", color=0xffccff)
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)\

@client.command(aliases=['cf'])
async def coinflip(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  tailsUrl= "https://cdn.discordapp.com/attachments/876240128807407666/876309657847726110/s-l400.jpg"
  headsUrl = "https://cdn.discordapp.com/attachments/876240128807407666/876309799669727242/51NyMaKLydL._AC_.jpg" 
  if (seconds > 3 or new):
    head = randint(1,2)
    if head > 1:
      embedv = discord.Embed(title=f"Coin Flip", description=f" The coin chose heads!", color=0x0F1272)
      embedv.add_field(name="Heads", value = ":sunglasses:")
      embedv.set_thumbnail(url = tailsUrl)
    else:
      embedv = discord.Embed(title=f"Coin Flip", description=f" The coin is tails!", color=0xffccff)
      embedv.add_field(name="Tails",value = ":sunglasses:")
      embedv.set_thumbnail(url = headsUrl)
  await ctx.send(embed = embedv)

@client.command()
async def susrate(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    sus = randint(1,100)
    if sus > 50:
      embedv = discord.Embed(title=f" {ctx.author.name}'s susrate", description=f" Your susrate is {sus}. I think we may need to vote you out for being sus. :flushed:", color=0x2C720F)
    else:
      embedv = discord.Embed(title=f" {ctx.author.name}'s susrate", description=f" Your susrate is {sus}. You aren't sus!", color=0x2C720F)
  await ctx.send(embed = embedv)

@client.command()
async def loserrate(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    loser = randint(1,100)
    if loser > 50:
      embedv = discord.Embed(title=f" {ctx.author.name}'s loserrate", description=f" :nerd: Your loserrate is {loser}. You're a loser :/", color=0x75162F)
    else:
      embedv = discord.Embed(title=f" {ctx.author.name}'s loserrate", description=f" Your loserrate is {loser}. It seems you aren't a loser ", color=0x75162F)
  await ctx.send(embed = embedv)

@client.command()
async def winnerrate(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    win = randint(1,100)
    if win > 50:
      embedv = discord.Embed(title=f" {ctx.author.name}'s winner rate", description=f" :tada: Your winner rate is {win}. Seems like you're a true winner!", color=0x4d0026)
    else:
      embedv = discord.Embed(title=f" {ctx.author.name}'s winner rate", description=f" :tada: Your winner rate is {win}. You're a loser!", color=0xff99cc)
  await ctx.send(embed = embedv)

@client.command()
async def iq(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    iq = randint(1,250)
    if iq > 125:
      embedv = discord.Embed(title=f" {ctx.author.name}'s IQ :nerd:", description=f" Your IQ is {iq}, you're a genius!", color=0x75162F)
    else:
      embedv = discord.Embed(title=f" {ctx.author.name}'s IQ ", description=f" Your IQ is {iq}, you're literally dumb!", color=0x75162F)
  await ctx.send(embed = embedv)

@client.command()
async def height(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    tall = randint(1,108)
    if tall > 72:
      embedv = discord.Embed(title=f" {ctx.author.name}'s Height", description=f"Your height is {tall} inches, sheesh you're tall.", color=0xc44dff)
    else:
      embedv = discord.Embed(title=f" {ctx.author.name}'s Height", description=f"Your height is {tall} inches, imagine being short.", color=0x1a0000)
  await ctx.send(embed = embedv)
# DEFINE MATH
def sub(x: float, y: float):
  return x - y

def add(x: float, y: float):
  return x + y

def div(x: float, y: float):
  return x / y


def sqrt(x :float):
  return math.sqrt(x)

def mult(x: float, y: float):
	return x * y

#COMMANDS MATH
@client.command(aliases=['add','mathsum','sum','increase','mathincrease','total','addition','plus'])
async def mathadd(ctx, x: float, y: float):
  res = add(x, y)
  embedv = discord.Embed(title=f" Addition Answer", description=f"{ctx.author.name}, the answer to your problem is {res}.", color=0x36A00A)
  await ctx.send(embed = embedv)

@client.command(aliases=['minus','subtraction','sub','decrease','difference','deduct','diff','subtract'])
async def mathsub(ctx, x: float, y: float):
  res = sub(x,y)
  embedv = discord.Embed(title=f"  Subtraction Answer", description=f"{ctx.author.name}, the answer to your problem is {res}.", color=0x0AA092)
  await ctx.send(embed = embedv)

@client.command(aliases=['divide','division','half','quotient','div'])
async def mathdiv(ctx, x: float, y: float):
  res = div(x, y)
  embedv = discord.Embed(title=f" Division Answer", description=f"{ctx.author.name}, the answer to your problem is {res}.", color=0x0A57A0)
  await ctx.send(embed = embedv)

@client.command(aliases=['squareroot','sqrt','root'])
async def mathsqrt(ctx, x: int):
  res = sqrt(x)
  embedv = discord.Embed(title=f" :nerd: Square Root Answer", description=f"{ctx.author.name}, the answer to your problem is {res}.", color=0x7C0AA0)
  await ctx.send(embed = embedv)

@client.command(aliases=['product','mult','multiply','multiplication'])
async def mathmult(ctx, x: float, y: float):
  res = mult(x,y)
  embedv = discord.Embed(title=f" :nerd: Multiplication Answer", description=f"{ctx.author.name}, the answer to your problem is {res}.", color=0x7C0AA0)
  await ctx.send(embed = embedv)


@client.command()
async def math(ctx):
    embedv = discord.Embed(title="Math command info!", description=" :nerd: Addition - heat add, sum, increase, total, addition, plus - Ex: heat add 2 2\n  :nerd: Subtraction - heat minus, subtraction, sub, decrease, difference, deduct, diff, subtract - Ex: heat subtract 2 1 \n  :nerd: Division - heat divide, division, half, quotient, div - Ex: heat divide 4 2 \n ~~:nerd: Square Root - heat sqrt,squareroot, root - Ex: heat root 4~~ WIP \n :nerd: Multiply - heat multiply, mult, product, multiplication - Ex: heat multiply 2 2\n :nerd: Must have at least 2 digits (only 1 for square root) Do not put any symbols, space out the numbers." , color=0xFF0000)
    await ctx.send(embed = embedv)



#END OF COMMANDS MATH




@client.command()
async def straferate(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 7 or new):
    strafe = randint(1,100)
    if strafe > 50:
      embedv = discord.Embed(title=f" {ctx.author.name}'s Strafe Rate", description=f"Your strafe rate is {strafe} ,  you're a lot like Strafe.", color=0xc44dff)
    else:
      embedv = discord.Embed(title=f"{ctx.author.name}'s Strafe Rate", description=f"Your strafe rate is {strafe} , imagine not being like the legendary Strafe.", color=0x1a0000)
  await ctx.send(embed = embedv)

@client.command()
async def invest(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['investtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    investAdd = randint(-200,400)
    investment = ['Bitcoin','Apple','Amazon','Currency Bot','HeatCoin','Fortnite','Doge Coin','Mrbeast Burger']
    #user = Query()
    #accounts.update({"balance": person['balance'] + investAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, investtime = %s
      WHERE id = %s;
    ''', (person['balance'] + investAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if investAdd > 0:
      embedv = discord.Embed(title=f" {ctx.author.name} made a serious investment!", description=f"You made <:pd_heatcoin:858357730951823360> {investAdd} , keep investing into {random.choice(investment)}!", color =0x008000) 
    else:
      embedv = discord.Embed(title=f" {ctx.author.name} invested into BitCoin!", description=f"You lost <:pd_heatcoin:858357730951823360> {investAdd} . Next time invest into HeatCoin :sob:", color =0xFF0000) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command(aliases=['draw'])
async def art(ctx):
  person, new = findPerson(ctx.author.id)
  artists = ['Leonardo da Vinci','Michelangelo','Rembrandt','Eugene Delacroix','Claude Monet','Vincent van Gogh','Pablo Picasso']
  current = datetime.now()
  difference = current - dateObject(person['arttime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    artAdd = randint(-100,300)
    #user = Query()
    #accounts.update({"balance": person['balance'] + artAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, arttime = %s
      WHERE id = %s;
    ''', (person['balance'] + artAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if artAdd > 0:
      embedv = discord.Embed(title=f"{ctx.author.name} drew an art piece!", description=f" {random.choice(artists)} bought {ctx.author.name}'s  art piece for <:pd_heatcoin:858357730951823360> {artAdd} !", color =0x008000) 
    else:
      embedv = discord.Embed(title=f" {ctx.author.name} made a bad art piece!  ", description=f"You lost <:pd_heatcoin:858357730951823360> {artAdd} . Next time don't make a piece of garbage!", color =0xFF0000) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command()
async def reddit(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['reddittime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    redditAdd = randint(-100,300)
    memetype = ['Stupid','Repost','Dank','Bad','Funny']
    #user = Query()
    #accounts.update({"balance": person['balance'] + redditAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, reddittime = %s
      WHERE id = %s;
    ''', (person['balance'] + redditAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if redditAdd > 0:
      embedv = discord.Embed(title=f"{ctx.author.name} posted a {random.choice(memetype)} to Reddit", description=f"Your post had  {redditAdd} upvotes, so you got <:pd_heatcoin:858357730951823360> {redditAdd} .", color =0x10E06F) 
    else:
      embedv = discord.Embed(title=f"{ctx.author.name} posted a {random.choice(memetype)} to Reddit", description=f"Your post had {redditAdd} downvotes, so you lost <:pd_heatcoin:858357730951823360> {redditAdd} .", color =0xFFB6C1)
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command()
async def song(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['songtime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    songAdd = randint(-100,250)
    songViews = randint(10000,1000000)
    songPpl = ['Michael Jackson','Dababy','Jay Z','Freddie Murcery','Drake','Bruno Mars','KSI','Marshmello']
    #user = Query()
    #accounts.update({"balance": person['balance'] + songAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, songtime = %s
      WHERE id = %s;
    ''', (person['balance'] + songAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if songAdd > 0:
      embedv = discord.Embed(title=f"{ctx.author.name} posted a song to Soundcloud", description=f"You got {songViews} views on your new hit song with {random.choice(songPpl)} and made <:pd_heatcoin:858357730951823360> {songAdd} .", color =0x10E06F) 
    else:
      embedv = discord.Embed(title=f"{ctx.author.name} posted a song to Soundcloud", description=f"You got 0  views because you have bad music. You lost <:pd_heatcoin:858357730951823360> {songAdd}  that you used on advertising.", color =0xFFA500) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command()
async def travel(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['traveltime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    travelAdd = randint(-200,350)
    travelReason = ['Your plane crashed.','There were hidden fees.', 'You got stolen from while on your trip.','You got shot while on your trip, the hospital fees were high.']
    locationThings = ['Florida','New York','Africa','Canada','China','North Korea','India','Amercia','Mexico','the United Kingdom']
    #user = Query()
    #accounts.update({"balance": person['balance'] + travelAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, traveltime = %s
      WHERE id = %s;
    ''', (person['balance'] + travelAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if travelAdd > 0:
      embedv = discord.Embed(title=f" {ctx.author.name} went on vacation!", description=f"You travelled {travelAdd} miles to {random.choice(locationThings)} and made <:pd_heatcoin:858357730951823360> {travelAdd}.", color =0x10E06F) 
    else:
      embedv = discord.Embed(title=f" {ctx.author.name} went on vacation!", description=f"Your travel to {random.choice(locationThings)} made you lose <:pd_heatcoin:858357730951823360> {travelAdd} instead of gaining. {random.choice(travelReason)} ", color =0x10E06F) 

  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command(aliases=['8ball','8b'])
async def eightball(ctx):
  responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
  embedv = discord.Embed(title="Answer:", description=f':8ball: {random.choice(responses)}.', color =0x170B0C) 
  await ctx.send(embed = embedv)           


@client.command(aliases=['yt'])
async def youtube(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['yttime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    youtubeViews = randint(100,300)
    youtubeAdd = youtubeViews / 1
    videoidea = ['Drama','Fortnite','Minecraft','Animation','Coding','Makeup','Vlogging']
    #user = Query()
    #accounts.update({"balance": person['balance'] + youtubeAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, yttime = %s
      WHERE id = %s;
    ''', (person['balance'] + youtubeAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    embedv = discord.Embed(title=f" {ctx.author.name} posted a video!", description=f"You posted a video about {random.choice(videoidea)} that got {youtubeViews} views and cashed out with <:pd_heatcoin:858357730951823360> {youtubeAdd}.", color =0x10E06F) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

@client.command(aliases=['tweet'])
async def twitter(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['twittertime'])
  seconds = round(difference.total_seconds())
  if (seconds > 3 or new):
    twitterAdd = randint(-200,400)
    twitterLikes = randint(2500,5000)
   # user = Query()
    #accounts.update({"balance": person['balance'] + twitterAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, twittertime = %s
      WHERE id = %s;
    ''', (person['balance'] + twitterAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    if twitterAdd > 0:
      embedv = discord.Embed(title=f" {ctx.author.name} posted a video!", description=f"{ctx.author.name} posted a tweet about cats that got {twitterLikes} likes and cashed out with <:pd_heatcoin:858357730951823360> {twitterAdd} .", color =0x10E06F) 
    else: 
      embedv = discord.Embed(title=f"{ctx.author.name} made a tweet!!", description=f"You got cancelled for saying bad words, you got fined <:pd_heatcoin:858357730951823360> {twitterAdd} .", color =0x0000FF) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)



@client.command(aliases=['insta','ig'])
async def instagram(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['igtime'])
  seconds = difference.total_seconds()
  if round((seconds > 3 or new)):
    instaViews = randint(50,300)
    instaAdd = instaViews / 1
    #user = Query()
    #accounts.update({"balance": person['balance'] + instaAdd, "begtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, igtime = %s
      WHERE id = %s;
    ''', (person['balance'] + instaAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    embedv = discord.Embed(title=f" {ctx.author.name} posted a story!", description=f"You posted a swipe up story that got {instaViews},000 views and made <:pd_heatcoin:858357730951823360> {instaAdd} .", color =0x10E06F) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

#daily cmd
@client.command()
async def daily(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['dailytime'])
  seconds = round(difference.total_seconds())
  if (seconds > 86400 or new):
    dailyAdd = randint(5000,15000)
    #user = Query()
    #accounts.update({"balance": person['balance'] + dailyAdd, "dailytime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, dailytime = %s
      WHERE id = %s;
    ''', (person['balance'] + dailyAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    embedv = discord.Embed(title=f"{ctx.author.name}'s' daily claim!", description=f"You gained <:pd_heatcoin:858357730951823360> {dailyAdd}  as your daily claim. ", color =0x10E06F) 
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {86400 - seconds} seconds.", color =0x170B0C) 
  await ctx.send(embed = embedv)

#hourly cmd

@client.command()
async def hourly(ctx):
  person, new = findPerson(ctx.author.id)
  current = datetime.now()
  different = current - dateObject(person['hourtime'])
  seconds = round(different.total_seconds())
  if (seconds > 3600 or new):
    hourlyAdd = (1000)
    #user = Query()
    #accounts.update({"balance": person['balance'] + hourlyAdd, "hourtime": dateString(current)}, user.id == ctx.author.id)
    cursor = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
      UPDATE accounts
      SET balance = %s, hourtime = %s
      WHERE id = %s;
    ''', (person['balance'] + hourlyAdd, dateString(current), ctx.author.id))
    database.commit()
    cursor.close()
    embedv = discord.Embed(titel=f"{ctx.author.name}'s hourly claim!", description = f"You gained <:pd_heatcoin:858357730951823360> {hourlyAdd} as your hourly claim. ", color = 0x69690)
  else:
    embedv = discord.Embed(title="Cooldown", description=f"please wait {3600 - seconds} seconds", color = 0x170B0C)
  await ctx.send(embed =embedv)


@client.command()
async def prorate(ctx):
  person, new = findPerson(ctx.author.id)

  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    pro = randint(1,100)
    if pro > 50:
     embedv = discord.Embed(title=f"{ctx.author.name}'s prorate", description=f"  You're very pro with a prorate of {pro}.", color=0x75162F)
    else:
      embedv = discord.Embed(title=f":slight_frown:  {ctx.author.name}'s prorate", description=f" You're not very pro with a prorate of {pro}.", color=0x75162F)
  await ctx.send(embed = embedv)


@client.command()
async def slap( ctx, member : discord.Member ):
  person, new = findPerson(ctx.author.id)
  current = datetime.now()
  difference = current - dateObject(person['begtime'])
  seconds = difference.total_seconds()
  if (seconds > 3 or new):
    embedv = discord.Embed(title=None, description = f" {ctx.author.mention} slapped {member.mention} in the face!", color=0x3498db)
  else:
    embedv = discord.Embed(title="Cooldown", description=f"Please wait {3 - seconds} seconds.", color =0x170B0C) 
  await ctx.send( embed = embedv )

#gamble 
'''
@client.command(aliases = ['bet'])
async def gamble(ctx, bet = 0):
  print(bet)
  if bet != 0:
    bett = int(bet)
    print(bett)
    #find author
    person, new = findPerson(ctx.author.id)
    current = datetime.now()
    gambleMoney = randint(0,4)
    print(gambleMoney)
    #find author again?
    better, newAuthor = findPerson(ctx.author.id)
    if bett < 0:
      cembed = discord.Embed(title=f"You can't bet negatives.",description = f"You need to bet a higher amount.", color = 0x12345 )
    if bett > 10000:
      cembed = discord.Embed(title=f"You can't bet that much.",description = f"You need to bet a lower amount, before you go broke (10k maximum)", color = 0x12345 )
    else:
      if better['balance']<bett:
        cembed = discord.Embed(title="You're to poor.", description = f"You only have {better['balance']}", color = 0x69690)
      else:
        if gambleMoney == 3:
          user = Query()
          accounts.update({"balance": person['balance'] + bett, "begtime": dateString(current)}, user.id == ctx.author.id)
          cembed = discord.Embed(title=f"{ctx.author.name}'s gamble!", description = f"You gained  <:pd_heatcoin:858357730951823360>  {bett} ", color = 0x69690)
        else:
          user = Query()
          accounts.update({"balance": person['balance'] - bett, "begtime": dateString(current)}, user.id == ctx.author.id)
          cembed = discord.Embed(title=f"{ctx.author.name}'s gamble!", description = f"You lost  {bett}, rip :(  ", color = 0x69690)
  else:
    cembed = discord.Embed(title=f"You need to enter a number to bet.",description = f"How can you bet without a number :man_facepalming: ", color = 0x12345 )
    await ctx.send(embed = cembed)
'''



client.run(token)
