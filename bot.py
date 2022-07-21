import discord
from discord.ext import commands
import discord.utils
import random
import json
from pprint import pprint
import os

bot = commands.Bot(command_prefix='!')
channel = None
absdir = os.path.dirname(__file__)
jsondir = 'data.json'
jsondir = os.path.join(absdir,jsondir)
channeldir = 'channel_data.json'
channeldir = os.path.join(absdir,channeldir)
with open(jsondir,'r') as infile:
    data = json.  load(infile)

def validate_channel(ctx):
    if channel is None:
        if ctx.message.server is None:
            return False
        else:
            return True
    else:
        if ctx.message.channel.name == channel:
            return False
        else:
            return True

def validate_poll(poll_name:str):
    for key in data.keys():
        if poll_name == key:
            return True
    return False

def json_write():
    with open(jsondir,'w') as outfile:
            json.dum p(data,infile)

def info_print(poll_name:str,made_by:str,results:bool,final = False):
    poll_info = '** {} **\n\n'.format(poll_name)
    it = 0

    if not results and not final:

        for choice in data[poll_name]['choices']:
            it += 1
            poll_info += '` {}.` ** {} **\n'.format(str(it),choice)

        poll_info += '\n Created by ** {} **.\n Voting for this poll has **not started** yet!'.format(made_by)
        return poll_info

    elif results and not final:
        tuple_list = []

        for choice in data[poll_name]['choices']:
            it += 1
        for i in range(0,it):
            tuple_list.append((data[poll_name]['votes'][i],data[poll_name]['choices'][i]))

        #tuple_list.sort(key=lambda tup: tup[0], reverse=True)
        poll_info += '**Standings:**\n\n'

        it = 0
        for choice in tuple_list:
            it += 1
            poll_info += '` {}.` ** {}    `Votes : {} `**\n'.format(str(it),choice[1],int(choice[0]))

        poll_info += '\n Created by ** {} **.\n Voting for this poll has **started**.\n'.format(made_by)
        '''
        it=0
        for choice in data[poll_name]['choices']:
            it += 1
            poll_info += '`{}.` **{}**\n'.format(str(it),choice)
        '''
        poll_info += '\nTo vote use `!poll_vote` command.'

        return poll_info

    else:
        tuple_list = []

        for choice in data[poll_name]['choices']:
            it += 1
        for i in range(0,it):
            tuple_list.append((data[poll_name]['votes'][i],data[poll_name]['choices'][i]))

        tuple_list.sort(key=lambda tup: tup[0], reverse=True)
        if tuple_list[0][0]>tuple_list[1][0]:
            poll_info += '**The winner is >>> {} <<<** \n\n'.format(tuple_list[0][1])
            it = 0
            for choice in tuple_list:
                it += 1
                poll_info += '` {}.` ** {}    `Votes : {} `**\n'.format(str(it),choice[1],int(choice[0]))
        else:
            it = 0
            poll_info += '**The winners are >>> {}** '.format(tuple_list[it][1])
            while True:
                try:
                    if tuple_list[it][0] == tuple_list[it+1][0]:
                        poll_info += ' **, {} **'.format(tuple_list[it+1][1])
                        it += 1
                    else:
                        break
                except Exception:
                    break

            poll_info += ' **<<<**\n\n'
            it = 0
            for choice in tuple_list:
                it += 1
                poll_info += '` {}.` ** {}    `Votes : {} `**\n'.format(str(it),choice[1],int(choice[0]))


        return poll_info

@bot.event
async def on_ready():
    await bot.change_status(game=discord.Game(name='!poll_howto'))
    with open(channeldir,'r') as infile:
        chan = json.load(infile)
    global channel
    if chan['channel'] == 'None':
        channel = None
    else:
        channel = chan['channel']
    print(channel)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context = True)
async def poll_howto(ctx):
    if validate_channel(ctx):
        return
    userid=ctx.message.author.id
    msg='Hello, Im PollBot. Here is the list of commands you can use:\n\n`!poll_channel [argument]` -> Sets where bot commands will be usable. For server owners only. Available arguments: None - for PMs, [channel_name] - for channel on the server.\nExample: `!poll_channel None` for PMs only, or `!poll_channel examplechannel` for examplechannel only.\n\n`!poll_create [poll_name]<[option1],[option2],[option3],[opt]...` -> Creates poll with set name and with stated options. The poll will not start untill you use !poll_start command.\nExample: `!poll_create example poll<SAO,snk,M a g i, Re ;zero`\n\n`!poll_add [poll_name]<[option1],[option2],[option3],[opt]...` -> Adds stated options to poll. Can only be used by creator of the poll.\nExample: `!poll_add example poll<haruhi`\n\n`!poll_modify [poll_name]` -> Modifies name of stated poll or one of it\'s options. Can only be used by creator of the poll.\nExample:`!poll_modify example poll`\n\n`!poll_delete [poll_name]` -> Deletes stated poll. Can only be used by creator of the poll.\nExample:`!poll_delete example poll`\n\n`!poll_start [poll_name]` -> Starts stated poll. Can only be used by creator of the poll.\nExample:`!poll_start example poll`\n\n`!poll_end [poll_name]` -> Ends stated poll. Can only be used by creator of the poll. Sends results to creator of the poll. Deletes the poll afterwards.\nExample:`!poll_end example poll`\n\n`!poll_vote` -> Starts the voting process. You can only vote for each poll once.\nExample:`!poll_vote`\n\n`!poll_list` -> Lists currently opened and currently closed polls.\nExample:`!poll_list`\n\n`!poll_info [poll_name]` -> Sends you information and stats of the stated poll.\nExample:`!poll_info example poll`'
    await bot.send_message(discord.User(id=userid),msg)


@bot.command(pass_context = True)
async def poll_create(ctx,*,line:str):
    if validate_channel(ctx):
        return

    exists = False
    poll_id = ctx.message.author.id
    poll_user = ctx.message.author.name

    try:
        poll_name,poll_options = line.split('<')
    except Exception:
        await bot.say('Wrong format! Use < between poll name and poll options')
        return

    try:
        poll_options = poll_options.split(',')
    except Exception:
        await bot.say('Wrong format! Use , inbetween each of options')
        return

    if validate_poll(poll_name):
        await bot.say('**Poll `{}` can not be created because it already exists! Please use a different name.**'.format(poll_name))
    else:
        poll_votes=[]
        poll_users=[]
        for key in poll_options:
            poll_votes.append(0)
        data.update({poll_name: {'choices':poll_options,'votes':poll_votes,'userid': poll_id,'username':poll_user,'name':poll_name,'started_voting':False,'users_voted':poll_users}})
        json_write()
        await bot.say('**Poll `{}` has been created!**'.format(poll_name))

@bot.command(pass_context = True)
async def poll_add(ctx,*,line:str):
    if validate_channel(ctx):
        return

    poll_id = str(ctx.message.author.id)

    try:
        poll_name,poll_options = line.split('<')
    except Exception:
        await bot.say('Wrong format! Use < between poll name and poll options')
        return
    if(poll_options == ''):
        await bot.say('Options to add have not been stated!')
        return
    try:
        poll_options = poll_options.split(',')
    except Exception:
        await bot.say('Wrong format! Use , inbetween each of options')
        return

    if validate_poll(poll_name):
        if data[poll_name]['started_voting']:
            await bot.say('Voting for this poll has already started and thus you can not add options to it')
            return
        if poll_id == data[poll_name]['userid']:
            poll_votes=[]
            for key in poll_options:
                poll_votes.append(0)
            data[poll_name]['choices'].extend(poll_options)
            data[poll_name]['votes'].extend(poll_votes)
            json_write()
            await bot.say('**Options have been added to poll `{}`!**'.format(poll_name))
        else:
            await bot.say('**Options can not be added to poll `{}` by you because you have not created it.**'.format(poll_name))
    else:
        await bot.say('**Poll `{}` does not exist!**'.format(poll_name))

@bot.command(pass_context = True)
async def poll_modify(ctx,*,poll_name:str):
    if validate_channel(ctx):
        return

    poll_id=ctx.message.author.id

    if validate_poll(poll_name):
        if data[poll_name]['started_voting']:
            await bot.say('Voting for this poll has already started and thus you can not modify it')
            return
        if poll_id == data[poll_name]['userid']:

            def check(msg):
                return msg.content.startswith('')

            await bot.say('Please enter what you want to modify: \n 1. Modify poll name \n 2. Modify poll option')
            while True:
                new_msg = await bot.wait_for_message(author = ctx.message.author,timeout = 0,check = check)
                if new_msg:
                    break
            modify_what=new_msg.content;

            if modify_what == '1':
                await bot.say('Please enter new name for poll `{}`'.format(poll_name))
                while True:
                    new_msg = await bot.wait_for_message(author = ctx.message.author,timeout = 0,check = check)
                    if new_msg:
                        modify_what=new_msg.content
                        data[modify_what] = data.pop(poll_name)
                        data[modify_what]['name'] = modify_what
                        json_write()
                        await bot.say('The poll name has been changed to `{}`'.format(modify_what))
                        break

            elif modify_what == '2':
                await bot.say('Please enter the number of option you want to change and it\'s new name in this format `[number],[new name]`')
                while True:
                    new_msg = await bot.wait_for_message(author = ctx.message.author,timeout = 0,check = check)
                    if new_msg:
                        modify_what = new_msg.content
                        option_number,option_new = modify_what.split(',')
                        if int(option_number) <= len(data[poll_name]['choices']):
                            data[poll_name]['choices'][int(option_number)-1] = option_new
                            json_write()
                            await bot.say('Option number `{}` has been changed to `{}`'.format(option_number,option_new))
                            break
                        else:
                            await bot.say('Option number `{}` does not exist'.format(option_number))
                            break
            else:
                await bot.say('Invalid choice.')

        else:
            await bot.say('**Poll `{}` can not be modified by you because you have not created it.**'.format(poll_name))

    else:
        if poll_name == '':
            await bot.say('**Please enter valid poll name.**')
        else:
            await bot.say('**That poll does not exist! Please enter valid poll name.**')

@bot.command(pass_context = True)
async def poll_delete(ctx,*,poll_name:str):
    if validate_channel(ctx):
        return

    poll_id = str(ctx.message.author.id)

    if validate_poll(poll_name):
        if poll_id == data[poll_name]['userid']:
            del data[poll_name]
            json_write()
            await bot.say('**Poll `{}` has been deleted!**'.format(poll_name))
        else:
            await bot.say('**Poll `{}` can not be deleted by you because you have not created it.**'.format(poll_name))
    else:
        await bot.say('**Poll `{}` does not exist!**'.format(poll_name))

@bot.command(pass_context = True)
async def poll_vote(ctx):
    if validate_channel(ctx):
        return

    def check(msg):
        return msg.content.startswith('')

    current_user = ctx.message.author.id
    validate_user = False
    it = 0
    polls = []

    line = 'Please enter the number of poll which you want to vote for:\n\n'
    for key in data:
        if data[key]['started_voting'] is True:
            it += 1
            polls.append(key)
            line += '`{}.` **{}**\n'.format(str(it),key)
    await bot.say(line)

    while True:
        new_msg = await bot.wait_for_message(author = ctx.message.author,timeout = 0,check = check)
        if new_msg:
            break
    try:
        poll_no = int(new_msg.content)
    except Exception:
        await bot.say('**It has to be a number!**')
        return
    if poll_no > it:
        await bot.say('**It has to be a number from 1 to {}!**'.format(str(it)))
        return

    poll_name=polls[poll_no-1]

    for user in data[poll_name]['users_voted']:
            if user == current_user:
                validate_user = True
                break

    if validate_user:
        await bot.say('**You have already voted in this poll!**'.format(poll_name))
        return

    line = 'Please enter the number of option which you want to vote for:\n\n'
    it = 0
    for choice in data[poll_name]['choices']:
            it += 1
            line += '`{}.` **{}**\n'.format(str(it),choice)
    await bot.say(line)

    while True:
        new_msg = await bot.wait_for_message(author = ctx.message.author,timeout = 0,check = check)
        if new_msg:
            break
    try:
        vote_option = int(new_msg.content)
    except Exception:
        await bot.say('**It has to be a number!**')
        return
    if vote_option > it:
        await bot.say('**It has to be a number from 1 to {}!**'.format(str(it)))
        return

    data[poll_name]['votes'][int(vote_option) - 1] += 1
    data[poll_name]['users_voted'].append(current_user)
    json_write()
    await bot.say('**You have successfully voted for option `{}` in poll `{}`!**'.format(str(vote_option),poll_name))

@bot.command(pass_context = True)
async def poll_start(ctx,*,poll_name:str):
    if validate_channel(ctx):
        return

    poll_id = str(ctx.message.author.id)
    if validate_poll(poll_name):
        if poll_id == data[poll_name]['userid']:
            data[poll_name]['started_voting']=True
            json_write()
            await bot.say('**Poll `{}` has been opened for voting!**'.format(poll_name))
        else:
            await bot.say('**You can not open poll `{}` for voting because you have not created it.**'.format(poll_name))
    else:
        await bot.say('**Poll `{}` does not exist!**'.format(poll_name))


@bot.command(pass_context = True)
async def poll_end(ctx,*,poll_name:str):
    if validate_channel(ctx):
        return

    if validate_poll(poll_name):
        poll_id = str(ctx.message.author.id)
        made_by= data[poll_name]['username']
        results=data[poll_name]['started_voting']
        if poll_id == data[poll_name]['userid']:
            await bot.say(info_print(poll_name,made_by,results,final=True))
            await bot.send_message(discord.User(id=data[poll_name]['userid']),info_print(poll_name,made_by,results,final=True))
            del data[poll_name]
            json_write()
        else:
            await bot.say('**You can not open poll `{}` for voting because you have not created it.**'.format(poll_name))
    else:
        await bot.say('**Poll `{}` does not exist!**'.format(poll_name))

@bot.command(pass_context = True)
async def poll_list(ctx):
    if validate_channel(ctx):
        return

    lists = 'Ongoing polls:\n\n'
    it = 0
    for key in data:
        if data[key]['started_voting'] is True:
            it += 1
            lists += '`{}.` **{}**\n'.format(str(it),key)

    lists += '\nClosed polls:\n\n'
    it = 0
    for key in data:
        if data[key]['started_voting'] is False:
            it += 1
            lists += '`{}.` **{}**\n'.format(str(it),key)
    await bot.say(lists)

@bot.command(pass_context = True)
async def poll_info(ctx,*,poll_name:str):
    if validate_channel(ctx):
        return


    if validate_poll(poll_name):
        made_by = data[poll_name]['username']
        results=data[poll_name]['started_voting']
        await bot.say(info_print(poll_name,made_by,results))
    else:
        await bot.say('**Poll `{}` does not exist!**'.format(poll_name))

@bot.command(pass_context = True)
async def poll_channel(ctx,*,channel_name):

    if ctx.message.author.id == ctx.message.server.owner.id:
        global channel
        channel_exists = False
        with open(channeldir,'r') as infile:
            chan = json.load(infile)

        if channel_name == 'None':
            chan['channel'] = channel_name
            channel = None
            await bot.say('Successfully changed interaction with bot to **PMs** only.')
        else:
            for key in ctx.message.server.channels:

                if key.type is discord.ChannelType.text:
                    if channel_name == key.name:
                        channel_exists = True
                        break
            if channel_exists:
                chan['channel'] = channel_name
                channel = channel_name
                await bot.say('Successfully changed interactions with bot to channel **{}** only.'.format(channel_name))
            else:
                await bot.say('Channel **{}** does not exist!'.format(channel_name))
        with open(channeldir,'w') as outfile:
                json.dump(chan,outfile)
    else:
        await bot.say('Only server owners can use this command!')

bot.run('Your token goes here')