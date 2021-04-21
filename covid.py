import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

TOKEN = '' # your bot token here

mylist = ["Maharashtra", "Kerala", "Karnataka", "Andhra Pradesh", "Tamil Nadu", "Delhi", "Uttar Pradesh", "West Bengal", "Odisha", "Rajasthan", "Chhattisgarh", "Telangana", "Haryana", "Gujarat", "Bihar", "Madhya Pradesh", "Assam", "Punjab", "Jammu And Kashmir", "Jharkhand", "Uttarakhand", "Himachal Pradesh", "Goa", "Puducherry", "Tripura", "Manipur", "Chandigarh", "Arunachal Pradesh", "Meghalaya", "Nagaland", "Ladakh", "Sikkim", "Andaman And Nicobar Islands", "Mizoram", "Dadra And Nagar Haveli And Daman And Diu", "Lakshadweep", "Total"]

def log(info):
    t = datetime.datetime.now()
    print("log : " + str(t) + " : " + info)

sep = ("-" * 70)

BOT = commands.Bot(command_prefix = '$', help_command=None) # ucan replace the command prefix with what ever u want

if os.path.exists("graph.png"):
    os.remove("graph.png")

@BOT.event
async def on_ready():
    log("logged on, ready to accpect commands")
    print(sep)

#u cant also change the commands
@BOT.command(name="covid-info")
async def corona(ctx):
    #log
    log("data fetch requested")

    #setting url variable
    url = r'https://api.covid19india.org/csv/latest/state_wise.csv'

    #reading the url for covid data to a pandas dataframe
    df = pd.read_csv(url)

    #log
    log("cleaning the data")

    #dropping all uneeded data(cleaning the dataframe)
    df_clean = df.drop(columns=['Last_Updated_Time', 'Migrated_Other', 'State_code', 'State_Notes', 'Delta_Deaths', 'Delta_Recovered', 'Delta_Confirmed'])

    df_clean["State"]= df_clean["State"].str.upper().str.title()

    await ctx.reply("Please Enter Your State")

    #log
    log("taking input from user")

    #taking user input for state
    def check(msg):
        return (msg.author == ctx.author) and (msg.channel == ctx.channel)

    msg = await BOT.wait_for("message", check=check)

    state = msg.content.title()

    id = "no"

    for x in mylist:
        if state == x:
            id = "yes"
            break

    if id == "no":
        #log
        log("invalid input recived from the user")
        print(sep)
        #Reply the user with a error message
        await ctx.reply("Invalid input, please use '$list-states' to check available inputs")
        return

    #log
    log("input recived, proceeding")
    #selecting particular State's data which was requested by the user
    df1 = df_clean[df_clean['State'] == state]

    confirmed = df1.iloc[0]['Confirmed']
    recovered = df1.iloc[0]['Recovered']
    deaths = df1.iloc[0]['Deaths']
    active = df1.iloc[0]['Active']
    values =[confirmed, recovered, deaths, active]
    header = ['Confirmed', 'Recovered', 'Deaths', 'Active']
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    await ctx.reply("Please mention the format of data you want, Text or Graph?")

    def check(msg):
        return (msg.author == ctx.author) and (msg.channel == ctx.channel)

    msg = await BOT.wait_for("message", check=check)

    msg.content = msg.content.title()

    if (msg.content) == "Text":
        #log
        log("Text format choosen, genrating text message")
        embedVar = discord.Embed(title="Covid19 Info For " + state, description="", color=discord.Colour.red())
        embedVar.add_field(name="Confirmed", value=confirmed, inline=False)
        embedVar.add_field(name="Recovered", value=recovered, inline=False)
        embedVar.add_field(name="Deaths", value=deaths, inline=False)
        embedVar.add_field(name="Active", value=active, inline=False)
        await ctx.reply(embed=embedVar)
        #log
        log("Final reply sent!")
        print(sep)

    elif (msg.content) == "Graph":
        log("genrating graph")
        for index, value in enumerate(values):

            plt.text(value, index, str(value))

        ax.set_xticklabels([])
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.title("Covid Info Bar Graph For " + state)
        my_colors = ['r', 'g', 'k', 'b']  #red, green, blue, black

        plt.barh(header, values, color=my_colors)

        fig.savefig('graph.png', bbox_inches='tight') 
        plt.close(fig)

        await ctx.reply(file=discord.File('graph.png'))

        os.remove("graph.png")
        #log
        log("Final reply sent!")
        print(sep)

    else:
        log("Invalid format input recived, end request")
        print(sep)
        await ctx.reply("Please type a valid option, start again")
        return

@BOT.command(name="help")
async def help(ctx):
    embedVar1 = discord.Embed(title="Help Dialogue", description="all covid india info bot commands", color=discord.Colour.red())
    embedVar1.add_field(name="$covid-info", value="displays current covid19 case data in Text or Graph format", inline=True)
    embedVar1.add_field(name="$list-states", value="lists all possible state names that you can use with $covid-info command", inline=True)
    embedVar1.add_field(name="$author", value="Displays info about author", inline=True)
    await ctx.reply(embed=embedVar1)

@BOT.command(name="list-states")
async def state(ctx):
    poped = mylist[:-1]
    linear = ('\n'.join(map(str, poped)))
    field = (linear + '\n' + "Total " + "-> Note that this input is for getting total case data for whole India which includes all States")

    embedVar2 = discord.Embed(color=discord.Colour.red())
    embedVar2.title = "The available States input are: "
    embedVar2.description = field
    await ctx.reply(embed=embedVar2)

@BOT.command(name="author")
async def author(ctx):
    embedVar3 = discord.Embed(color=discord.Colour.red())
    embedVar3.title = "This bot was made by: "
    embedVar3.description = 'Dakkshesh'
    await ctx.reply(embed=embedVar3)

@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        log("Unknown command by user, ignoring")
        print(sep)
        return
    raise error

BOT.run(TOKEN)

#------------------------------- STAY HOME , STAY SAFE -------------------------------#
