# import discord
# # from discord_components import Select, SelectOption, Button
# #to allow our bot to recognize that something is a command
# from discord.ext import commands
# #asynchronous function tool
# import asyncio
# #this will allow us to run asynchronous fucntion from inside synchronous function
# from asyncio import run_coroutine_threadsafe
# #will allow us to take a youtube link and do other things
# from urllib import parse, request
# #to do stuffs with links
# import re
# import json
# import os
# #this will download audio from youtube video and let us listen
# from youtube_dl import YoutubeDL

# class music_cog(commands.Cog):
#     def __init__(self,bot):
#         self.bot=bot
        
#         self.is_playing={}
#         self.is_paused={}
#         self.musicQueue={}
#         self.queueIndex={}
        
#         self.YTDL_OPTIONS={'format':'bestaudio','nonplaylist':'True'}
#         self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        
#         #for generating an embed
#         self.embedBlue=0x2c76dd
#         self.embedRed=0xdf1141
#         self.embedGreen=0x0eaa51
        
#         self.vc={}
    
#     @commands.Cog.listener()
#     #this function is run whenever the bot is made online
#     async def on_ready(self):
#         #for every server the bot has joined we will do something
#         print("in the ready state")
#         for guild in self.bot.guilds:
#             id=int(guild.id)
#             #it is a list of (lists of musics ques) of all the servers jime bot present h
#             self.musicQueue[id]=[]
#             #queueIndex matlb jo bhi saare servers m h bot usme music queue m se konse number ka gana chlana h
#             self.queueIndex[id]=0
#             self.vc[id]=None
#             self.is_paused[id]=self.is_playing[id]=False
#     def now_playing_embed(self,ctx,song):
#         title=song['title']
#         link=song['link']
#         thumbnail=song['thumbnail']
#         author=ctx.author
#         avatar=author.avatar_url
        
#         embed=discord.Embed(
#             title="Now Playing",
#             description=f'[{title}]({link})',
#             color=self.embedBlue
            
#         )
#         embed.set_thumbnail(url=thumbnail)
#         embed.set_footer(text=f'Song added by: {str(author)}',icon_url=avatar)
#         return embed
        
        
#     async def join_vc(self,ctx,channel):
#         print("in the join vc")
#         #ctx is context when message was sent
#         #channel is the server
#         id=int(ctx.guild.id)
#         if self.vc[id]==None or not self.vc[id].is_connected():
#             self.vc[id]==await channel.connect()
            
#             if(self.vc[id]==None):
#                 await ctx.send("Could not connect to the voice channel")
#                 return
#         else:
#             #if it si already connect to the channel then move to a different one
#             await self.vc[id].move_to(channel)
    
#     def search_YT(self,search):
#         queryString=parse.urlencode({'search_query':search})
#         htmContent = request.urlopen('http://www.youtube.com/results?' + queryString)
#         searchResults=re.findall('/watch\?v=(.{11})',htmContent.read().decode())
#         return searchResults[0:10]
    
#     def extract_YT(self,url):
#           with YoutubeDL(self.YTDL_OPTIONS) as ydl:
#               try:
#                   info=ydl.extract_info(url,download=False)
#               except:
#                   return False
#           return {
#             'link': 'https://www.youtube.com/watch?v=' + url,
#             'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD5uL4xKN-IUfez6KIW_j5y70mlig',
#             'source': info['formats'][0]['url'],
#             'title': info['title']
#           }
        
#     def play_next(self,ctx):
#         id=int(ctx.guild.id)
#         if not self.is_playing[id]:
#             return 
#         if self.queueIndex[id]+1<len(self.musicQueue[id]):
#             self.is_playing[id]=True
#             self.queueIndex[id]+=1
            
#             song=self.musicQueue[id][self.queueIndex[id]][0]
#             message=self.now_playing_embed(ctx,song)
#             #to send message in non-async function
#             coroutine=ctx.send(embed=message)
#             fut=run_coroutine_threadsafe(coroutine,self.bot.loop)
#             try:
#                 fut.result()
#             except:
#                 pass
            
#             self.vc[id].play(discord.FFmpegPCMAudio(
#                 song['source'],**self.FFMPEG_OPTIONS), after=lambda e:self.play_next(ctx))
#         else:
#             self.queueIndex[id]+=1
#             self.is_playing=False    
#     async def play_music(self,ctx):
#         id=int(ctx.guild.id)
#         #to check if there are more songs to play in the music queue
#         if(self.queueIndex[id]<len(self.musicQueue[id])):
#             self.is_playing=True
#             self.is_paused=False
            
#             #second parameter will return the channel
#             await self.join_VC(ctx,self.musicQueue[id][self.queueIndex[id]][1])
#             song=self.musicQueue[id][self.queueIndex[id]][0]
#             message=self.now_playing_embed(ctx,song)
#             await ctx.send(embed=message)
#             self.vc[id].play(discord.FFmpegPCMAudio(
#                 song['source'],**self.FFMPEG_OPTIONS), after=lambda e:self.play_next(ctx))
        
#         else:
#             await ctx.send("There are no songs in the queue to be played.")    
#             self.queueIndex[id]+=1
#             self.is_playing=False
             
#     @ commands.command(
#         name="join",
#         aliases=["j"],
#         help=""
#     )
    
#     async def join(self,ctx):
#         print("join command given")
#         if ctx.author.voice:
#             userChannel=ctx.author.voice.channel
#             await self.join_vc(ctx,userChannel)
#             await ctx.send(f'Bot has joined {userChannel}')
#         else:
#             await ctx.send("You need to be connected to a voice channel")    
    
#     @ commands.command(
#         name="leave",
#         aliases=["l"],
#         help=""
#     )
#     async def leave(self,ctx):
#         id=int(ctx.guild.id)
#         self.is_playing[id]=self.is_paused[id]=False
#         self.musicQueue[id]=[]
#         self.queueIndex[id]=0
#         if self.vc[id]!=None:
#             await ctx.send("Bot has left the chat")
#             await self.vc[id].disconnect()

import discord
from discord.ext import commands
import asyncio
from asyncio import run_coroutine_threadsafe
from urllib import parse, request
import re
import json
# from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
# from discord_components import Select, SelectOption, Button

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = {}
        self.is_paused = {}
        self.musicQueue = {}
        self.queueIndex = {}
        self.vc = {}

        self.YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.FFMPEG_OPTIONS ={
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        # for generating an embed
        self.embedBlue = 0x2c76dd
        self.embedRed = 0xdf1141
        self.embedGreen = 0x0eaa51

    @commands.Cog.listener()
    async def on_ready(self):
        print("in the ready state")
        for guild in self.bot.guilds:
            id = int(guild.id)
            self.musicQueue[id] = []
            self.queueIndex[id] = 0
            self.vc[id] = None
            self.is_paused[id] = self.is_playing[id] = False
    #to make sure that bot leaves the vc when everyone has left
    #before is whatever the voice state before joining/leaving of a member
    #after is whatever the voice state after joining/leaving of the member
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        id=int(member.guild.id)
        #first conditon to check ki leave/join bot ne ni kia h na
        if member.id!=self.bot.user.id and before.channel!=None and after.channel!=before.channel:
            remainingChannelMembers=before.channel.members
            if(len(remainingChannelMembers)==1 and remainingChannelMembers[0].id==self.bot.user.id and self.vc[id].is_connected()):
                self.is_playing[id]=self.is_paused=False
                self.musicQueue[id]=[]
                self.queueIndex[id]=0
                await self.vc[id].disconnect()
            
        
    def now_playing_embed(self, ctx, song):
        title = song['title']
        link = song['link']
        thumbnail = song['thumbnail']
        author = ctx.author
        avatar = author.avatar.url if author.avatar else None

        embed = discord.Embed(
            title="Now Playing",
            description=f'[{title}]({link})',
            color=self.embedBlue
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f'Song added by: {str(author)}', icon_url=avatar)
        return embed
    def added_song_embed(self, ctx, song):
        title = song['title']
        link = song['link']
        thumbnail = song['thumbnail']
        author = ctx.author
        avatar = author.avatar.url if author.avatar else None

        embed = discord.Embed(
            title="Song Added To Queue!",
            description=f'[{title}]({link})',
            color=self.embedRed
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f'Song added by: {str(author)}', icon_url=avatar)
        return embed
    def removed_song_embed(self, ctx, song):
        title = song['title']
        link = song['link']
        thumbnail = song['thumbnail']
        author = ctx.author
        avatar = author.avatar.url if author.avatar else None

        embed = discord.Embed(
            title="Song Removed From The Queue!",
            description=f'[{title}]({link})',
            color=self.embedRed
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f'Song removed by: {str(author)}', icon_url=avatar)
        return embed
    async def join_vc(self, ctx, channel):
        id = int(ctx.guild.id)
        if self.vc[id] is None or not self.vc[id].is_connected():
            self.vc[id] = await channel.connect()
            if self.vc[id] is None:
                await ctx.send("Could not connect to the voice channel")
                return
        else:
            await self.vc[id].move_to(channel)
    
    def get_YT_title(self,videoId):
        params={"format":"json","url":"https://www.youtube.com/watch?v=%s" %videoId}
        #niche wla url is the link to the video
        url = "https://www.youtube.com/oembed"
        #now we are encoding the link
        query_string=parse.urlencode(params)
        url=url+"?"+query_string
        #now we are opening the url ans json m convert kr rhe
        with request.urlopen(url) as response:
            responseText=response.read()
            data=json.loads(responseText.decode())
            return data['title']
    
    def search_YT(self, search):
        queryString = parse.urlencode({'search_query': search})
        htmContent = request.urlopen(
            'http://www.youtube.com/results?' + queryString)
        searchResults = re.findall(
            '/watch\?v=(.{11})', htmContent.read().decode())
        return searchResults[0:10]

    # def extract_YT(self, url):
    #     with YoutubeDL(self.YTDL_OPTIONS) as ydl:
    #         try:
    #             info = ydl.extract_info(url, download=False)
    #         except:
    #             return False
    #     return {
    #         'link': 'https://www.youtube.com/watch?v=' + url,
    #         'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD5uL4xKN-IUfez6KIW_j5y70mlig',
    #         'source': info['formats'][0]['url'],
    #         'title': info['title']
    #     }
    def extract_YT(self, url):
       with YoutubeDL(self.YTDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [info])
            audio_url = None
            for f in formats:
                if f.get('ext') == 'm4a':
                    audio_url = f.get('url')
                    break
                elif f.get('ext') == 'webm' and not f.get('vcodec'):
                    audio_url = f.get('url')
                    break

            if audio_url is None:
                audio_url = formats[0].get('url')
        except Exception as e:
            print(f"Error extracting YT info: {e}")
            return False

       return {
        'link': 'https://www.youtube.com/watch?v=' + url,
        'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg',
        'source': audio_url,
        'title': info['title']
      }

    def play_next(self, ctx):
        id = int(ctx.guild.id)
        if not self.is_playing[id]:
            return
        if self.queueIndex[id] + 1 < len(self.musicQueue[id]):
            self.is_playing[id] = True
            self.queueIndex[id] += 1

            song = self.musicQueue[id][self.queueIndex[id]][0]
            message = self.now_playing_embed(ctx, song)
            coroutine = ctx.send(embed=message)
            fut = run_coroutine_threadsafe(coroutine, self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Error sending now playing message: {e}")


            self.player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song['source'], **self.FFMPEG_OPTIONS))
            self.vc[id].play(self.player, after=lambda e: self.play_next(ctx))
        else:
            self.queueIndex[id] += 1
            self.is_playing[id] = False

    async def play_music(self, ctx):
        id = int(ctx.guild.id)
        if self.queueIndex[id] < len(self.musicQueue[id]):
            self.is_playing[id] = True
            self.is_paused[id] = False

            await self.join_vc(ctx, self.musicQueue[id][self.queueIndex[id]][1])
            song = self.musicQueue[id][self.queueIndex[id]][0]
            message = self.now_playing_embed(ctx, song)
            await ctx.send(embed=message)
            self.player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song['source'], **self.FFMPEG_OPTIONS))
            print(song['source'])
            self.vc[id].play(self.player, after=lambda e: self.play_next(ctx))
        else:
            await ctx.send("There are no songs in the queue to be played.")
            self.queueIndex[id] += 1
            self.is_playing[id] = False
     
    @commands.command(name="add", aliases=["a"], help="To add a song to the queue")
    async def add(self,ctx,*args):
        search=" ".join(args)
        try:
            userChannel=ctx.author.voice.channel
        except:
            await ctx.send("You must be in a voice channel")
            return
        if not args:
            await ctx.send("You need to specify a song to be added.")
        else:
            song=self.extract_YT(self.search_YT(search)[0])
            if type(song)==type(False):
                await ctx.send("Could not download the song. Incorrect format, try different keyword.")
                return 
            else:
                self.musicQueue[ctx.guild.id].append([song,userChannel])
                message=self.added_song_embed(ctx,song)
                await ctx.send(embed=message)
         
    @commands.command(name="search", aliases=["find"], help="To search a song on youtube")
    async def search(self, ctx, *args):
        search = " ".join(args)
        songNames = []
        selectionOptions = []
        embedText = ""

        if not args:
            await ctx.send("You must specify search terms to use this command")
            return
        try:
            userChannel = ctx.author.voice.channel
        except:
            await ctx.send("You must be connected to a voice channel.")
            return
        await ctx.send("Fetching search results....")

        songTokens = self.search_YT(search)

        for i, token in enumerate(songTokens):
            url = 'https://www.youtube.com/watch?v=' + token
            name = self.get_YT_title(token)
            songNames.append(name)
            embedText += f"{i+1} - [{name}]({url})\n"

        for i, title in enumerate(songNames):
            selectionOptions.append(discord.SelectOption(
                label=f"{i+1} - {title[:95]}", value=str(i)
            ))

        searchResults = discord.Embed(
            title="Search Results",
            description=embedText,
            color=self.embedRed
        )

        class SearchSelect(discord.ui.Select):
            def __init__(self, cog, ctx, songTokens, userChannel):
                self.cog = cog
                self.ctx = ctx
                self.songTokens = songTokens
                self.userChannel = userChannel
                options = selectionOptions
                super().__init__(
                    placeholder="Choose a song...",
                    min_values=1,
                    max_values=1,
                    options=options,
                )

            async def callback(self, interaction: discord.Interaction):
                chosenIndex = int(self.values[0])
                songRef = self.cog.extract_YT(self.songTokens[chosenIndex])
                if not songRef:
                    await self.ctx.send("Could not download the song. Incorrect format, try different keywords")
                    return
                embedResponse = discord.Embed(
                    title=f"Option #{chosenIndex+1} Selected",
                    description=f"[{songRef['title']}]({songRef['link']}) added to the queue",
                    color=self.cog.embedRed
                )
                embedResponse.set_thumbnail(url=songRef['thumbnail'])
                await ctx.send(embed=embedResponse)
                self.cog.musicQueue[self.ctx.guild.id].append([songRef, self.userChannel])

        class SearchView(discord.ui.View):
            def __init__(self, cog, ctx, songTokens, userChannel):
                super().__init__()
                self.add_item(SearchSelect(cog, ctx, songTokens, userChannel))

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
            async def cancel_callback(self, button, interaction: discord.Interaction):
                searchResults.title = "Search Canceled"
                searchResults.description = ""
                await ctx.send(embed=searchResults)

        view = SearchView(self, ctx, songTokens, userChannel)
        await ctx.send(embed=searchResults)
    @commands.command(name="remove", aliases=["rm"], help="To remove the last added song") 
    async def remove(self,ctx):
        id=int(ctx.guild.id)
        if self.musicQueue[id]!=[]:
            song=self.musicQueue[id][-1][0]
            removeSongEmbed=self.removed_song_embed(ctx,song)
            await ctx.send(embed=removeSongEmbed)
        else:
            await ctx.send("There are no songs to be removed in the queue.")
        #removing the last song
        self.musicQueue[id]=self.musicQueue[id][:-1]
        if self.musicQueue[id]==[]:
            if self.vc[id]!=None and self.is_playing[id]:
                self.is_playing[id]=self.is_paused[id]=False
                await self.vc[id].disconnect()
                self.vc[id]=None
                
            self.queueIndex[id]=0
        #if we were at the end of the queue
        elif self.queueIndex[id]==len(self.musicQueue[id]) and self.vc[id]!=None and self.vc[id]:
            self.vc[id].pause()
            #to skip back the song
            self.queueIndex[id]-=1
            await self.play_music(ctx)
             
    @ commands.command(
        name="previous",
        aliases=["pre", "prev"],
        help="To Play the previous song in the queue"
    )
    async def previous(self, ctx):
        id = int(ctx.guild.id)
        if self.vc[id] == None:
            await ctx.send("You need to be in a VC to use this command.")
        elif self.queueIndex[id] <= 0:
            await ctx.send("There is no previous song in the queue. Replaying current song.")
            self.vc[id].pause()
            await self.play_music(ctx)
        elif self.vc[id] != None and self.vc[id]:
            self.vc[id].pause()
            self.queueIndex[id] -= 1
            await self.play_music(ctx)

    @ commands.command(
        name="skip",
        aliases=["sk","next"],
        help="Skips to the next song in the queue."
    )
    async def skip(self, ctx):
        id = int(ctx.guild.id)
        if self.vc[id] == None:
            await ctx.send("You need to be in a VC to use this command.")
        elif self.queueIndex[id] >= len(self.musicQueue[id]) - 1:
            await ctx.send("There is no next song in the queue. Replaying current song.")
            self.vc[id].pause()
            await self.play_music(ctx)
        elif self.vc[id] != None and self.vc[id]:
            self.vc[id].pause()
            self.queueIndex[id] += 1
            await self.play_music(ctx)
    @commands.command(name="clear", aliases=["cl"], help="To clear the songs queue")
    async def clear(self,ctx):
        id=int(ctx.guild.id)
        if(self.vc[id]!=None and self.is_playing[id]):
             
             self.is_paused[id]=self.is_playing[id]=False
             self.vc[id].stop()
        if(self.musicQueue[id]!=[]):
            await ctx.send("The music queue has been cleared.")
            self.musicQueue[id]=[]
        self.queueIndex[id]=0   
        
    @commands.command(name="resume", aliases=["start","re"], help="To resume a song") 
    async def resume(self,ctx):
        id=int(ctx.guild.id)
        if(not self.vc[id]):
            await ctx.send("There is no audio to be paused at the moment")
        elif self.is_paused[id]:
            await ctx.send("Audio resumed")
            self.is_playing[id]=True
            self.is_paused[id]=False
            self.vc[id].resume()
                   
    @commands.command(name="pause", aliases=["stop","pa"], help="To Pause a song")
    async def pause(self,ctx):
        id=int(ctx.guild.id)
        if(not self.vc[id]):
            await ctx.send("There is no audio to be paused at the moment")
        elif self.is_playing[id]:
            await ctx.send("Audio paused")
            self.is_playing[id]=False
            self.is_paused[id]=True
            #for actually pausing the audio
            self.vc[id].pause()
            
    @commands.command(name="play", aliases=["pl"], help="To play a song")
    async def play(self,ctx,*args):
        #* is used so that all the parameters are accepted in the song name
        search=" ".join(args)
        #server id
        id=int(ctx.guild.id)
        try:
            userChannel=ctx.author.voice.channel
        except:
            await ctx.send("You much be connected to a voice channel")
            return
        if not args:
            if(len(self.musicQueue[id])==0):
                await ctx.send("Ther are no songs to be played in the queue")
                return
            elif not self.is_playing[id]:
                if self.musicQueue[id] is None or self.vc[id] is None:
                    await self.play_music(ctx)
                else:
                    self.is_paused[id]=False
                    self.is_playing[id]=True
                    self.vc[id].resume()    
            else:
                return
            
        else:
            song=self.extract_YT(self.search_YT(search)[0])  
            #agr song ka type boolean h toh mtlb download ni hua h
            if type(song)==bool:
                await ctx.send("Could not download song. Incorrect format, try some different keywords")
            else:
                self.musicQueue[id].append([song,userChannel])
                if(not self.is_playing[id]):
                    await self.play_music(ctx)   
                else:
                    message=self.added_song_embed(ctx,song)
                    await ctx.send(embed=message)
    @ commands.command(
        name="queue",
        aliases=["list", "q"],
        help="To List the next few songs in the queue."
    )
    async def queue(self, ctx):
        id = int(ctx.guild.id)
        returnValue = ""
        if self.musicQueue[id] == []:
            await ctx.send("There are no songs in the queue.")
            return

        for i in range(self.queueIndex[id], len(self.musicQueue[id])):
            upNextSongs = len(self.musicQueue[id]) - self.queueIndex[id]
            print(len(self.musicQueue[id]))
            print(self.queueIndex[id])
            print(upNextSongs)
            if i > 5 + upNextSongs:
                break
            returnIndex = i - self.queueIndex[id]
            if returnIndex == 0:
                returnIndex = "Playing"
            elif returnIndex == 1:
                returnIndex = "Next"
            else:
                returnIndex = str(returnIndex)
            returnValue += f"{returnIndex} - [{self.musicQueue[id][i][0]['title']}]({self.musicQueue[id][i][0]['link']})\n"

            if returnValue == "":
                await ctx.send("There are no songs in the queue.")
                return

        queue = discord.Embed(
            title="Current Queue",
            description=returnValue,
            colour=self.embedGreen
        )
        await ctx.send(embed=queue)
    
    
    
    @commands.command(name="join", aliases=["j"], help="To Joins a voice channel")
    async def join(self, ctx):
        if ctx.author.voice:
            userChannel = ctx.author.voice.channel
            await self.join_vc(ctx, userChannel)
            await ctx.send(f'Bot has joined {userChannel}')
        else:
            await ctx.send("You need to be connected to a voice channel")

    @commands.command(name="leave", aliases=["l"], help="To Leave the voice channel")
    async def leave(self, ctx):
        id = int(ctx.guild.id)
        self.is_playing[id] = self.is_paused[id] = False
        self.musicQueue[id] = []
        self.queueIndex[id] = 0
        if self.vc[id] is not None:
            await ctx.send("Bot has left the chat")
            await self.vc[id].disconnect()
            self.vc[id]=None

def setup(bot):
    bot.add_cog(music_cog(bot))

# import discord
# # from discord_components import Select, SelectOption, Button
# #to allow our bot to recognize that something is a command
# from discord.ext import commands
# #asynchronous function tool
# import asyncio
# #this will allow us to run asynchronous fucntion from inside synchronous function
# from asyncio import run_coroutine_threadsafe
# #will allow us to take a youtube link and do other things
# from urllib import parse, request
# #to do stuffs with links
# import re
# import json
# import os
# #this will download audio from youtube video and let us listen
# from youtube_dl import YoutubeDL

# class music_cog(commands.Cog):
#     def __init__(self,bot):
#         self.bot=bot
        
#         self.is_playing={}
#         self.is_paused={}
#         self.musicQueue={}
#         self.queueIndex={}
        
#         self.YTDL_OPTIONS={'format':'bestaudio','nonplaylist':'True'}
#         self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        
#         #for generating an embed
#         self.embedBlue=0x2c76dd
#         self.embedRed=0xdf1141
#         self.embedGreen=0x0eaa51
        
#         self.vc={}
    
#     @commands.Cog.listener()
#     #this function is run whenever the bot is made online
#     async def on_ready(self):
#         #for every server the bot has joined we will do something
#         print("in the ready state")
#         for guild in self.bot.guilds:
#             id=int(guild.id)
#             #it is a list of (lists of musics ques) of all the servers jime bot present h
#             self.musicQueue[id]=[]
#             #queueIndex matlb jo bhi saare servers m h bot usme music queue m se konse number ka gana chlana h
#             self.queueIndex[id]=0
#             self.vc[id]=None
#             self.is_paused[id]=self.is_playing[id]=False
#     def now_playing_embed(self,ctx,song):
#         title=song['title']
#         link=song['link']
#         thumbnail=song['thumbnail']
#         author=ctx.author
#         avatar=author.avatar_url
        
#         embed=discord.Embed(
#             title="Now Playing",
#             description=f'[{title}]({link})',
#             color=self.embedBlue
            
#         )
#         embed.set_thumbnail(url=thumbnail)
#         embed.set_footer(text=f'Song added by: {str(author)}',icon_url=avatar)
#         return embed
        
        
#     async def join_vc(self,ctx,channel):
#         print("in the join vc")
#         #ctx is context when message was sent
#         #channel is the server
#         id=int(ctx.guild.id)
#         if self.vc[id]==None or not self.vc[id].is_connected():
#             self.vc[id]==await channel.connect()
            
#             if(self.vc[id]==None):
#                 await ctx.send("Could not connect to the voice channel")
#                 return
#         else:
#             #if it si already connect to the channel then move to a different one
#             await self.vc[id].move_to(channel)
    
#     def search_YT(self,search):
#         queryString=parse.urlencode({'search_query':search})
#         htmContent = request.urlopen('http://www.youtube.com/results?' + queryString)
#         searchResults=re.findall('/watch\?v=(.{11})',htmContent.read().decode())
#         return searchResults[0:10]
    
#     def extract_YT(self,url):
#           with YoutubeDL(self.YTDL_OPTIONS) as ydl:
#               try:
#                   info=ydl.extract_info(url,download=False)
#               except:
#                   return False
#           return {
#             'link': 'https://www.youtube.com/watch?v=' + url,
#             'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD5uL4xKN-IUfez6KIW_j5y70mlig',
#             'source': info['formats'][0]['url'],
#             'title': info['title']
#           }
        
#     def play_next(self,ctx):
#         id=int(ctx.guild.id)
#         if not self.is_playing[id]:
#             return 
#         if self.queueIndex[id]+1<len(self.musicQueue[id]):
#             self.is_playing[id]=True
#             self.queueIndex[id]+=1
            
#             song=self.musicQueue[id][self.queueIndex[id]][0]
#             message=self.now_playing_embed(ctx,song)
#             #to send message in non-async function
#             coroutine=ctx.send(embed=message)
#             fut=run_coroutine_threadsafe(coroutine,self.bot.loop)
#             try:
#                 fut.result()
#             except:
#                 pass
            
#             self.vc[id].play(discord.FFmpegPCMAudio(
#                 song['source'],**self.FFMPEG_OPTIONS), after=lambda e:self.play_next(ctx))
#         else:
#             self.queueIndex[id]+=1
#             self.is_playing=False    
#     async def play_music(self,ctx):
#         id=int(ctx.guild.id)
#         #to check if there are more songs to play in the music queue
#         if(self.queueIndex[id]<len(self.musicQueue[id])):
#             self.is_playing=True
#             self.is_paused=False
            
#             #second parameter will return the channel
#             await self.join_VC(ctx,self.musicQueue[id][self.queueIndex[id]][1])
#             song=self.musicQueue[id][self.queueIndex[id]][0]
#             message=self.now_playing_embed(ctx,song)
#             await ctx.send(embed=message)
#             self.vc[id].play(discord.FFmpegPCMAudio(
#                 song['source'],**self.FFMPEG_OPTIONS), after=lambda e:self.play_next(ctx))
        
#         else:
#             await ctx.send("There are no songs in the queue to be played.")    
#             self.queueIndex[id]+=1
#             self.is_playing=False
             
#     @ commands.command(
#         name="join",
#         aliases=["j"],
#         help=""
#     )
    
#     async def join(self,ctx):
#         print("join command given")
#         if ctx.author.voice:
#             userChannel=ctx.author.voice.channel
#             await self.join_vc(ctx,userChannel)
#             await ctx.send(f'Bot has joined {userChannel}')
#         else:
#             await ctx.send("You need to be connected to a voice channel")    
    
#     @ commands.command(
#         name="leave",
#         aliases=["l"],
#         help=""
#     )
#     async def leave(self,ctx):
#         id=int(ctx.guild.id)
#         self.is_playing[id]=self.is_paused[id]=False
#         self.musicQueue[id]=[]
#         self.queueIndex[id]=0
#         if self.vc[id]!=None:
#             await ctx.send("Bot has left the chat")
#             await self.vc[id].disconnect()
