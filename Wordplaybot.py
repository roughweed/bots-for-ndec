import discord
import time
import random
import database

token=open("token.txt","r").read()

client=discord.Client()


@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")
    global participants,scores,guild,log, all_done
    participants=[]
    scores=[]
    all_done=[]
    guild=client.get_guild()
    print(guild)

def practice_embed1(author,chnl):
    ques=discord.Embed(title="Question 1", description="Write down all of the words you can find here. One word in each message. Words with less than 4 letters would not be counted.", color=discord.Color.blue())
    ques.set_footer(text="Write 'next' when you cannot find any more words. You've got another question.")
    ques.set_image(database.ques)
    ques.add_field(name="Question for", value='<@{}>'.format(author), inline=False)
    ques.add_field(name="NOTE", value="The more time you consume, the less point you get.", inline=False)
    return chnl.send(embed=ques1)
def practice_embed2(author,chnl):
    ques=discord.Embed(title="Question 2", description="Write down all of the words you can find here. One word in each message. Words with less than 4 letters would not be counted.", color=discord.Color.blue())
    ques.set_footer(text="Write 'end' when you cannot find any more words. You're marks will be sent to the judges.")
    ques.set_image(url=database.ques2)
    ques.add_field(name="Question for", value='<@{}>'.format(author), inline=False)
    ques.add_field(name="NOTE", value="The more time you consume, the less point you get.", inline=True)
    ques.add_field(name="NOTE", value="If you suddenly find out a word from the previous question, just write that down", inline=True)
    return chnl.send(embed=ques)

def newlist(scores,chnl,rle):
    scores.extend([{'start':0,'stop':0,'count':0,'ans':[],'channel':chnl,'role':rle}])
    return scores 
def newpar(m,l):
    m.extend([l])
    return m
@client.event
async def on_message(message):
    if message.author==client.user:
        return
    global scores,participants, guild,log,all_done
    log=client.get_channel()
    wordplay=client.get_channel()
    answer1=[database.answer1]
    answer2=[database.answer2]

    if message.channel==wordplay and f'{message.author}' in all_done:
        await wordplay.send(f"Sorry <@{message.author.id}> you cannot try more than once.")
        return
    if message.channel==wordplay and message.content.lower()=="i am ready":
        name=f'{random.randrange(1000,9999)}-{random.randrange(1000,9999)}-{random.randrange(1000,9999)}-{random.randrange(1000,9999)}'
        await guild.create_role(name=name)
        await message.channel.send(f"<@{message.author.id}> wait a bit. Your virtual exam channel is being generated.")
        time.sleep(1)
        roleid=discord.utils.get(guild.roles, name=name)
        await guild.create_text_channel(name=name, overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), roleid: discord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True)})
        channelid=discord.utils.get(guild.channels, name=name)
        await message.author.add_roles(roleid)
        await message.channel.send(f"<@{message.author.id}> head to channel <#{channelid.id}> to continue.")
        await channelid.send("When you are ready for this, type ```start now```")
        participants=newpar(participants,f'{message.author}')
        all_done=participants.copy()
        scores=newlist(scores,channelid,roleid)
    

    
    if f'{message.author}' in participants and message.channel==scores[participants.index(f'{message.author}')]['channel'] and message.content.lower()=="start now":
        scores[participants.index(f'{message.author}')]['start']=time.perf_counter()
        await practice_embed1(message.author.id,message.channel)

    if f'{message.author}' in participants and message.channel==scores[participants.index(f'{message.author}')]['channel'] and message.content.lower()=="next":
        await practice_embed2(message.author.id,message.channel)

    if f'{message.author}' in participants and message.channel==scores[participants.index(f'{message.author}')]['channel'] and (message.content.upper() in answer1 or message.content.upper() in answer2) and message.content.upper() not in scores[participants.index(f'{message.author}')]['ans']:
        scores[participants.index(f'{message.author}')]['count']+=1
        scores[participants.index(f'{message.author}')]['ans'].extend([message.content.upper()])
    
    if f'{message.author}' in participants and message.channel==scores[participants.index(f'{message.author}')]['channel'] and message.content.lower()=="end":
        scores[participants.index(f'{message.author}')]['stop']=time.perf_counter()
        timer=round(scores[participants.index(f'{message.author}')]['stop']-scores[participants.index(f'{message.author}')]['start'])
        await log.send(f"<@{message.author.id}> has found {scores[participants.index(f'{message.author}')]['count']} words in {timer} seconds.\nScore ```{round(((scores[participants.index(f'{message.author}')]['count'])**2)*1000000/timer)}```")
        await scores[participants.index(f'{message.author}')]['channel'].delete()
        await scores[participants.index(f'{message.author}')]['role'].delete()
        scores.remove(scores[participants.index(f'{message.author}')])
        participants.remove(participants[participants.index(f'{message.author}')])


client.run(token)