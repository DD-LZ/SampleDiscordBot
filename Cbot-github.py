# Discord community coaching bot
# Works with Python 3.6
# Made by Leon Zhu - LZhu7080@gmail.com
# Github: DD-LZ

# MANY SIGNIFICANT PARTS OF CODE ARE LEFT OUT FOR PRIVACY
# THIS CODE BY ITSELF WILL NOT RUN

import copy
import asyncio
import time
import random
import datetime
import os
from datetime import datetime
import discord
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot
import lists

TOKEN = #Removed for privacy

Client = #Removed for privacy
client = commands.Bot(command_prefix = '!', case_insensitive = True)
client.remove_command('help')

botResponse = #Removed for privacy
activityLog = #Removed for privacy

#BOT READY--------------------------------------------------------------------------------
@client.event
async def on_ready():
   
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name='!help for commands'))

#check (for when replying)
def check(userMsg, author):
    return userMsg.author == author

#BOT FUNCTIONS---------------------------------------------------------------------------
#provides a full list of all categories
@client.command(aliases = ["fl"])
async def fullList(ctx):

    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    coachRole = discord.utils.get(ctx.guild.roles, name="Coach")

    await ctx.message.delete()
    if ctx.message.channel.name != "": #Removed for privacy
        embedMsg = discord.Embed(
            title = "", #Removed for privacy
            colour = discord.Colour.red()
        )
        await ctx.message.channel.send(embed=embedMsg)

    else:
        embedMsg = discord.Embed(
            title = "", #Removed for privacy
            colour = discord.Colour.purple()
        )
        embedMsg.add_field(name="", value="", inline=True)  #Removed for privacy
        embedMsg.add_field(name="", value="", inline=True)  #Removed for privacy
        embedMsg.add_field(name="", value="", inline=False) #Removed for privacy

        if staffRole in cmdAuthor.roles or coachRole in cmdAuthor.roles:
            embedMsg.add_field(name="", value="") #Removed for privacy

        embedMsg.set_footer(text="")   #Removed for privacy
        embedMsg.set_thumbnail(url="") #Removed for privacy
        await cmdAuthor.send(embed=embedMsg)

        logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)
        print(logMsg)
        with open(activityLog, 'a') as aLog:
            aLog.write(logMsg + '\n')

   


#return list of coaches in a specific list
@client.command(aliases = ["f"])
async def find(ctx, listChoice):

    await ctx.message.delete()
    if ctx.message.channel.name != "": #Removed for privacy
        embedMsg = discord.Embed(
            description = "", #Removed for privacy
            colour = discord.Colour.red()
        )
        await ctx.message.channel.send(embed=embedMsg)
    else:
        cmdAuthor = ctx.message.author

        #create list of requested coaches
        coachFileStr = lists.getFile(listChoice) 
        if coachFileStr == 0:
            embedMsg = discord.Embed(
                title = "", #Removed for privacy
                colour = discord.Colour.red()
            )
            await cmdAuthor.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ATTEMPTED TO run [%s]"  % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)
            print(logMsg)
            with open(activityLog, 'a') as aLog:
                aLog.write(logMsg + '\n')

        else:
            #get names and randomize a list
            coachList = lists.getNames(coachFileStr)
            tempCoachList = []

            #for i in range(3): (get max 3 random names)
            while coachList != []:
                randChoice = random.choice(coachList)
                tempCoachList.append(randChoice)
                coachList.remove(randChoice)
            coachList = tempCoachList

            embedMsg = discord.Embed(
                title = "", #Removed for privacy
                colour = discord.Colour.purple()
            )

            if coachList == []:
                embedMsg.title =  "" #Removed for privacy
                embedMsg.colour = discord.Colour.red()

            else:
                #compile final message to send
                finalList = ""
                for each in coachList:
                    coachName  = await client.fetch_user(int(each.replace("\n", "")))
                    finalList += "<@%s - %s\n" % (each.replace("\n", ">"), str(coachName)) 
 
                finalList += "" #Removed for privacy
                embedMsg.description = finalList

            embedMsg.set_footer(text="")   #Removed for privacy
            embedMsg.set_thumbnail(url="") #Removed for privacy
            await cmdAuthor.send(embed=embedMsg)

            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)
            print(logMsg)
            with open(activityLog, 'a') as aLog:
                aLog.write(logMsg + '\n')


#add/remove user to the inactive list
@client.command(aliases = ["ia"])
async def inactive(ctx):

    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    coachRole = discord.utils.get(ctx.guild.roles, name="Coach")

    #check authorization
    if staffRole in cmdAuthor.roles or coachRole in cmdAuthor.roles:

        #store all users temporarily and check if user exists on inactive list
        exist = False
        coachList = []
        with open(lists.inactiveList, 'r') as inactiveFile:
            line = inactiveFile.readline()
            while line != "":
                if line == (str(cmdAuthor.id) + '\n'):
                    exist = True
                else:
                    coachList.append(line)
                line = inactiveFile.readline()

        #create final message and remove or add user from inactive list
        embedMsg = discord.Embed(
            title = 'You are now **Inactive**',
            description = cmdAuthor.mention,
            colour = discord.Colour.red()
        )

        if exist == False:
            inactiveFile = open(lists.inactiveList, 'a')
            inactiveFile.write(str(cmdAuthor.id) + '\n')
            inactiveFile.close()

        else:
            with open(lists.inactiveList, 'w') as inactiveFile:
                for each in coachList:
                    inactiveFile.write(each)
            embedMsg.title = 'you are now **Active**'
            embedMsg.colour = discord.Colour.green()

        embedMsg.set_footer(text="")  #Removed for privacy
        embedMsg.set_thumbnail(url="") #Removed for privacy
        await ctx.message.channel.send(embed=embedMsg)
        logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    else:
        logMsg = "%s - %s (ID:%s) ATTEMPTED TO run [%s]"  % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#add user to a specific list
@client.command(aliases = ["a"])
async def add(ctx, listChoice):

    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    coachRole = discord.utils.get(ctx.guild.roles, name="Coach")

    #check authorization
    if staffRole in cmdAuthor.roles or coachRole in cmdAuthor.roles:

        #get correct file
        coachFileStr = lists.getFile(listChoice)

        if coachFileStr == 0:
            embedMsg = discord.Embed(
                title = "", #Removed for privacy
                description = cmdAuthor.mention,
                colour = discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s] but file not found" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

        elif "all" in listChoice.lower() and "ball" not in listChoice.lower():

            coachFileStr = copy.deepcopy(coachFileStr)

            while coachFileStr != []:
                fileStr = coachFileStr[0]

                #check if user exists on list
                exist = False
                with open(fileStr, 'r') as coachFile:
                    line = coachFile.readline()
                    while line != "":
                        if line == (str(cmdAuthor.id) + '\n'):
                            exist = True
                        line = coachFile.readline()

                if exist != True:
                    coachFile = open(fileStr, 'a')
                    coachFile.write(str(cmdAuthor.id) + '\n')
                    coachFile.close()

                coachFileStr.remove(coachFileStr[0])

            embedMsg = discord.Embed(
                title = "You have been added to %s" % listChoice.upper(),
                description = cmdAuthor.mention,
                colour = discord.Colour.green()
            )
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

        else:
            #check if user exists on list
            exist = False
            with open(coachFileStr, 'r') as coachFile:
                line = coachFile.readline()
                while line != "":
                    if line == (str(cmdAuthor.id) + '\n'):
                        exist = True
                    line = coachFile.readline()

            #create final message and add user specified
            embedMsg = discord.Embed(
                title = "You have been added to %s" % listChoice.upper(),
                description = cmdAuthor.mention,
                colour = discord.Colour.green()
            )

            if exist == True:
                embedMsg.title = "You already exist on %s" % listChoice.upper()
                embedMsg.colour = discord.Colour.red()

            else:
                coachFile = open(coachFileStr, 'a')
                coachFile.write(str(cmdAuthor.id) + '\n')
                coachFile.close()

            embedMsg.set_footer(text="")  #Removed for privacy
            embedMsg.set_thumbnail(url="") #Removed for privacy
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    else:
        logMsg = "%s - %s (ID:%s) ATTEMPTED TO run [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#remove user to a specific list
@client.command(aliases = ["r"])
async def remove(ctx, listChoice):

    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    coachRole = discord.utils.get(ctx.guild.roles, name="Coach")

    #check authorization
    if staffRole in cmdAuthor.roles or coachRole in cmdAuthor.roles:

        #get correct file
        coachFileStr = lists.getFile(listChoice)

        if coachFileStr == 0:
            embedMsg = discord.Embed(
                title = "t", #Removed for privacy
                description = cmdAuthor.mention,
                colour = discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s] but file not found" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

        elif "all" in listChoice.lower() and "ball" not in listChoice.lower():
            coachFileStr = copy.deepcopy(coachFileStr)

            while coachFileStr != []:
                fileStr = coachFileStr[0]

                #check if user exists on list
                exist = False
                coachList = []
                with open(fileStr, 'r') as coachFile:
                    line = coachFile.readline()
                    while line != "":
                        if line == (str(cmdAuthor.id) + '\n'):
                            exist = True
                        else:
                            coachList.append(line)
                        line = coachFile.readline()

                if exist == True:
                    with open(fileStr, 'w') as coachFile:
                        for each in coachList:
                            coachFile.write(each)

                coachFileStr.remove(coachFileStr[0])

            embedMsg = discord.Embed(
                title = "You have been removed from %s" % listChoice.upper(),
                description = cmdAuthor.mention,
                colour = discord.Colour.green()
            )
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

        else:
            #store all users temporarily and check if user exists on list
            exist = False
            coachList = []
            with open(coachFileStr, 'r') as coachFile:
                line = coachFile.readline()
                while line != "":
                    if line == (str(cmdAuthor.id) + '\n'):
                        exist = True
                    else:
                        coachList.append(line)
                    line = coachFile.readline()

            #create final message and rewrite file without user specified
            embedMsg = discord.Embed(
                title = "You have been removed from %s" % listChoice.upper(),
                description = cmdAuthor.mention,
                colour = discord.Colour.green()
            )

            if exist == False:
                    embedMsg.title = "You do not exist on %s" % listChoice.upper()
                    embedMsg.colour = discord.Colour.red()
            else:
                with open(coachFileStr, 'w') as coachFile:
                    for each in coachList:
                        coachFile.write(each)

            embedMsg.set_footer(text="")   #Removed for privacy
            embedMsg.set_thumbnail(url="") #Removed for privacy
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    else:
        logMsg = "%s - %s (ID:%s) ATTEMPTED TO run [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#send user the list(s) they are in
@client.command(aliases = ["l"])
async def list(ctx, user:User = "NULL#0000"):

    inactiveNames = []
    names = []
    tempList = []
    inactive = False
    adminCmd = False
    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    coachRole = discord.utils.get(ctx.guild.roles, name="Coach")

    #check authorization
    if staffRole in cmdAuthor.roles or coachRole in cmdAuthor.roles:

        if str(user) == "": #Removed for privacy
            await client.send_message(ctx.message.channel, "") #Removed for privacy
 
        else:
            if str(user) != "NULL#0000" and staffRole in cmdAuthor.roles:
                cmdAuthor = user
                adminCmd = True

            #check if user is inactive
            with open(lists.inactiveList, 'r') as inactiveFile:
                inactiveNames = inactiveFile.readlines()
            if (str(cmdAuthor.id) + '\n') in inactiveNames:
                inactive = True

            #loop through all lists and find ones currently present in
            for entry in os.scandir(""): #Removed for privacy
                with open(entry.path, 'r') as listFile:
                    names = listFile.readlines()
                    if (str(cmdAuthor.id) + '\n') in names:
                        tempList.append(entry.name.replace(".txt", ""))

            for entry in os.scandir(""):  #Removed for privacy
                with open(entry.path, 'r') as listFile:
                    names = listFile.readlines()
                    if (str(cmdAuthor.id) + '\n') in names:
                        tempList.append(entry.name.replace(".txt", ""))

            #create final list message and send
            embedMsg = discord.Embed(
                title = "", #Removed for privacy
                colour = discord.Colour.teal()
            )

            #create final message
            finalList = ""
            if adminCmd == True:
                embedMsg.title = "%s (ID:%s) \nis currently listed in these categories:" % (str(cmdAuthor), str(cmdAuthor.id))
                colour = discord.Colour.teal()
                if inactive == True:
                    finalList += "Note: <@%s> is currently **INACTIVE**\n\n" % str(cmdAuthor.id)
                cmdAuthor = ctx.message.author

            elif inactive == True:
                finalList += "Note: You are currently **INACTIVE**\n\n"
                embedMsg.colour = discord.Colour.red()

            if tempList == []:

                if adminCmd == True:
                    finalList = "Note: <@%s> is currently not in any lists" % str(cmdAuthor.id)
                else:
                    finalList = "You are currently not in any lists"
                embedMsg.colour = discord.Colour.red()

            else:
                for each in tempList:
                    finalList += each.upper() + '\n'

            embedMsg.description = finalList
            embedMsg.set_footer(text="")   #Removed for privacy
            embedMsg.set_thumbnail(url="") #Removed for privacy
            await cmdAuthor.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    else:
        logMsg = "%s - %s (ID:%s) ATTEMPTED TO run [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#set user on the specified list
@client.command(aliases = ["s"])
async def set(ctx, user:User, listChoice):

    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")

    #check authorization
    if staffRole in cmdAuthor.roles:

        if str(user) == "": #Removed for privacy
            await ctx.message.channel.send("") #Removed for privacy
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

        else:
            #get correct file
            if listChoice.lower() == "inactive":
                coachFileStr = lists.inactiveList

            else:
                coachFileStr = lists.getFile(listChoice)
                if coachFileStr == 0:
                    embedMsg = discord.Embed(
                        title = "", #Removed for privacy
                        description = cmdAuthor.mention,
                        colour = discord.Colour.red()
                    )
                    await ctx.message.channel.send(embed=embedMsg)

            #check if user exists on list
            exist = False
            coachList = []
            with open(coachFileStr, 'r') as coachFile:
                line = coachFile.readline()
                while line != "":
                    if line == (str(user.id) + '\n'):
                        exist = True
                    else:
                        coachList.append(line)
                    line = coachFile.readline()

            #create final message and add user specified
            embedMsg = discord.Embed(
                title = str(user) + " has been added to %s" % listChoice.upper(),
                description = cmdAuthor.mention,
                colour = discord.Colour.green()
            )

            if exist == True:
                with open(coachFileStr, 'w') as coachFile:
                    for each in coachList:
                        coachFile.write(each)
                embedMsg.title = str(user) + " has been removed from %s" % listChoice.upper()
                embedMsg.colour = discord.Colour.red()

            else:
                coachFile = open(coachFileStr, 'a')
                coachFile.write(str(user.id) + '\n')
                coachFile.close()

            embedMsg.set_footer(text="")   #Removed for privacy
            embedMsg.set_thumbnail(url="") #Removed for privacy
            await ctx.message.channel.send(embed=embedMsg)
            logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    else:
        logMsg = "%s - %s (ID:%s) ATTEMPTED TO run [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)

    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#help list
@client.command(aliases = ["h"])
async def help(ctx):

    await ctx.message.delete()
    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    coachRole = discord.utils.get(ctx.guild.roles, name="Coach")

    embedMsg = discord.Embed(
        title = "**Heres what i can do!**",
        colour = discord.Colour.purple()
    )
    if staffRole in cmdAuthor.roles:
        embedMsg.add_field(name="", value="", inline=False) #Removed for privacy
        embedMsg.add_field(name="", value="", inline=False) #Removed for privacy
    elif coachRole in cmdAuthor.roles:
        embedMsg.add_field(name="", value="", inline=False) #Removed for privacy    
    embedMsg.add_field(name="", value="", inline=False) #Removed for privacy

    embedMsg.set_footer(text="") #Removed for privacy
    embedMsg.set_thumbnail(url="") #Removed for privacy
    await cmdAuthor.send(embed=embedMsg)

    logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)
    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#post instructions
@client.command()
async def instructions(ctx):

    cmdAuthor = ctx.message.author
    staffRole = discord.utils.get(ctx.guild.roles, name="Staff")
    await ctx.message.delete()

    #check authorization
    if staffRole in cmdAuthor.roles:

        embedMsg = discord.Embed(
            title = "", #Removed for privacy
            description = "", #Removed for privacy
            colour = discord.Colour.purple()
        )
        embedMsg.set_thumbnail(url="") #Removed for privacy
        await ctx.message.channel.send(embed=embedMsg)

        embedMsg = discord.Embed(
            colour = discord.Colour.purple()
        )
        embedMsg.set_image(url="") #Removed for privacy
        await ctx.message.channel.send(embed=embedMsg)

        embedMsg = discord.Embed(
            description = "", #Removed for privacy
            colour = discord.Colour.purple() 
        )

        embedMsg.set_footer(text="") #Removed for privacy
        await ctx.message.channel.send(embed=embedMsg)

        embedMsg = discord.Embed(
            title = "", #Removed for privacy
            colour = discord.Colour.gold()
        )
        await ctx.message.channel.send(embed=embedMsg)


#post instructions
@client.command()
async def coaching(ctx):

    cmdAuthor = ctx.message.author

    embedMsg = discord.Embed(
        description = "", #Removed for privacy
        colour = discord.Colour.purple() 
    )
    await ctx.message.channel.send(embed=embedMsg)

    logMsg = "%s - %s (ID:%s) ran [%s]" % (str(datetime.now()), str(cmdAuthor), str(cmdAuthor.id), ctx.message.content)
    print(logMsg)
    with open(activityLog, 'a') as aLog:
        aLog.write(logMsg + '\n')


#EVENT DETECTION--------------------------------------------------------------------------
@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #variables and hold message contents
    user = message.author
    contents = message.content.split(" ")

    #someone @ me-----
    if client.user.mentioned_in(message) and message.mention_everyone is False:
        await message.channel.send(random.choice(botResponse))

#-----------------------------------------------------------------------------------------    
    #prevents client.event overriding
    await client.process_commands(message)
#-----------------------------------------------------------------------------------------    

#run bot
client.run(TOKEN) 

    
