import discord
import time
import random
import database

token=open("stoken.txt",'r').read()

client=discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")
    global participants,scores,guild,log, all_done,ques,ques_list
    participants=[]
    scores=[]
    all_done=[]
    guild=client.get_guild()
    log=client.get_channel()
    print(guild)
    ques={database.ques}
    ques_list={database.ques_list}    

def newlist(scores,chnl,rle):
    scores.extend([{'start':0,'stop':0,'count':0,'ans':0,'channel':chnl,'role':rle,'quesno':0,'skip':0}])
    return scores
def newpar(m,l):
    m.extend([l])
    return m

def practice_embed(author,QuesNo,desc,chnl):
    ques=discord.Embed(title=f"Question {QuesNo+1}", description=f"{desc}", color=discord.Color.blue())
    ques.set_footer(text="You'll have to spell 50 words. The more time you consume, the lesser you score.")
    ques.add_field(name="To answer", value='Just write down the letter that represents the answer. Write **Skip** if you want to skip the answer', inline=False)
    ques.add_field(name="To end this session",value="You'll have to get to the last question",inline=False)
    ques.add_field(name="You may skip the question you don't know.", value="Skipping a question gives you partial marking while submitting wrong answer does not.",inline=False)
    return chnl.send(embed=ques)

@client.event
async def on_message(message):
    global participants,scores,ques_list,ques,all_done
    quiz=client.get_channel()

    if message.channel==quiz and f'{message.author}' in all_done:
        await quiz.send(f"Sorry <@{message.author.id}> you cannot try more than once.")
        return

    if message.channel==quiz and message.content.lower()=="i am ready":
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
        await practice_embed(message.author.id,scores[participants.index(f'{message.author}')]['quesno'],ques_list[scores[participants.index(f'{message.author}')]['quesno']],message.channel)
    if  f'{message.author}' in participants and message.channel==scores[participants.index(f'{message.author}')]['channel'] and message.content.upper() in ['A','B','C','D','SKIP']:
        scores[participants.index(f'{message.author}')]['quesno']+=1
            
            

        if message.content.upper()==ques[ques_list[scores[participants.index(f'{message.author}')]['quesno']-1]]:
            scores[participants.index(f'{message.author}')]['count']+=1
        elif message.content.upper()=="SKIP":
            scores[participants.index(f'{message.author}')]['skip']+=1

        if scores[participants.index(f'{message.author}')]['quesno']<len(ques):
            await practice_embed(message.author.id,scores[participants.index(f'{message.author}')]['quesno'],ques_list[scores[participants.index(f'{message.author}')]['quesno']],message.channel)
        else:
            scores[participants.index(f'{message.author}')]['stop']=time.perf_counter()
            timer=round(scores[participants.index(f'{message.author}')]['stop']-scores[participants.index(f'{message.author}')]['start'])
            attempt=scores[participants.index(f'{message.author}')]['quesno']
            await log.send(f"<@{message.author.id}> has spelled {scores[participants.index(f'{message.author}')]['count']} words among {attempt-scores[participants.index(f'{message.author}')]['skip']} correctly, within {timer} seconds.\n**Skipped:** {scores[participants.index(f'{message.author}')]['skip']}\nScore ```{round((((scores[participants.index(f'{message.author}')]['count'])*2)+scores[participants.index(f'{message.author}')]['skip'])*100000/timer)}```")
            await scores[participants.index(f'{message.author}')]['channel'].delete()
            await scores[participants.index(f'{message.author}')]['role'].delete()
            scores.remove(scores[participants.index(f'{message.author}')])
            participants.remove(participants[participants.index(f'{message.author}')])
            return

    
    

client.run(token)