import discord
from discord.ext import commands, tasks
import os
import B
import random
#from replit import db
import dbm
import shelve

dukeDefault = ["Footman", "Marshall", "Champion",
               "Ranger", "Longbowman", "Seer", 
               "Knight", "General", "Wizard",
               "Dragoon", "Duchess", "Oracle",
               "Priest", "Pikeman", "Bowman",
               "Pikeman", "Pikeman", "Assassin"]

centurionDefault = ["Equites", "Equites", "Velites",
                    "Triarii", "Funditores", "Optio", 
                    "CaneCorso", "Legionarii", "Legionarii",
                    "Legionarii", "Legionarii", "PrimusPilus",
                    "Onager", "Hastati", "Tribunus",
                    "Exploratores"]

jarlDefault = ["Freeman", "Spearman", "Spearman",
               "Spearman", "ShieldMaiden", "Warlord", 
               "Huscarl", "Vala", "Archer",
               "Huntsman", "Gothi", "AxeWarrior",
               "Ulfberht", "SwordWarrior", "Berserker",
               "Chieftain"]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

### Commands start here

@bot.command(name='pull', help='pull <bag name> : Pulls a random tile from the bag')
async def pull(ctx, arg):
  bag = db[arg]
  if len(bag) > 0:
    tile = random.choice(bag)
    bag.remove(tile)
    db[arg] = bag
    await ctx.send(tile)
  else:
    await ctx.send("Bag Empty!")
  print("pull  command received  " + str(arg))

@bot.command(name='add', help='add <bag name> <tile name> : Adds the named tile into the bag')
async def add(ctx, arg, tile):
  bag = db[arg]
  bag.append(tile)
  db[arg] = bag
  await ctx.send(bag)
  print("add   command received  " + str(arg) + " " + str(tile))

@bot.command(name='remove', help='remove <bag name> <tile name> : Removes the named tile from the bag')
async def remove(ctx, arg, tile):
  bag = db[arg]
  bag.remove(tile)
  db[arg] = bag
  await ctx.send(bag)
  print("remove   command received  " + str(arg) + " " + str(tile))

@bot.command(name='list', help='list <bag name> : Lists the tiles remaining in the bag')
async def list(ctx, arg):
  await ctx.send(db[arg])
  print("list  command received  " + str(arg))

@bot.command(name='bags', help='bags : Lists all the available bag names')
async def bags(ctx):
  bags = " ".join(db.keys())
  if bags:
    await ctx.send(bags)
  else:
    await ctx.send("No Bags Present!")
  print("bags  command received  ")

@bot.command(name='reset', help='reset <bag name> <set name> : Resets the bag to the default tile list. Sets: Duke, Centurion, Jarl')
async def reset(ctx, bag, set):
  if set == "Duke":
    random.shuffle(dukeDefault)
    db[bag] = dukeDefault
  elif set == "Centurion":
    random.shuffle(centurionDefault)
    db[bag] = centurionDefault 
  elif set == "Jarl":
    random.shuffle(jarlDefault)
    db[bag] = jarlDefault 
  await ctx.send(db[bag])
  print("reset command received  " + str(bag) + " " + str(set))

@bot.command(name='delete', help='delete <bag name> : Deletes a bag')
async def delete(ctx, arg):
  del db[arg]
  bags = " ".join(db.keys())
  if bags:
    await ctx.send(bags)
  else:
    await ctx.send("No Bags Present!")
  print("delete command received  " + str(arg))

### Commands end here
with shelve.open('dukeStore', 'c') as db:
  B.keep_alive()

  my_secret = os.environ['DUKETOKEN']
  bot.run(my_secret)
