import discord
#save the token in a text file named token.txt in the same folder
token=open("token.txt","r").read()

client=discord.Client()


@client.event
async def on_ready():
    print("Logged in as:",client.user)

@client.event
async def on_member_join(member):
	global guild, regbooth, unregistered
	
	#You need to get all the ids manually. 
    guild = client.get_guild()
    regbooth=client.get_channel()
    rules=client.get_channel()
    entrance=client.get_channel()
    unregistered=guild.get_role()
    
    #giving the member unregistered role
    await member.add_roles(unregistered)
    #changable
    await entrance.send(f"**Welcome**, <@{member.id}>.\n*Make sure you've read the rules in <#{rules.id}> before proceeding to <#{regbooth.id}>.* \nAll the best for the event! \n\n#AnEnglishAffair ")

@client.event
async def on_message(message):
	global guild, regbooth, unregistered
	
	#You need to get all the ids manually. 
    reglog=client.get_channel()
    complain=client.get_channel()
    default=guild.get_role()
    
    if message.author==client.user:
        return

    if message.channel==regbooth:
        await message.delete() # deletes the entry in registration channel to keep everything clean
        #Changable
        await reglog.send(f"{message.author.id} aka {message.author} submitted his response: {message.content}")
    
    if message.channel==reglog:
        if message.content.lower().startswith("approve"): #prefix
            await message.delete()
            m=list(map(str,message.content.split()))
            b=int(m[1])
            await guild.get_member(b).remove_roles(unregistered)
            awaut guild.get_member(b).add_roles(default)
    
    if message.content.lower().startswith("complain"): #prefix
        await message.delete()
        #changable
        await complain.send(f"{message.author} said '{message.content[9:]}'")


client.run(token)