import aiohttp, asyncio, yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

token = config.get("token")
password = config.get("password")
new_username = config.get("new_username")

headers = {"Authorization": token, "Content-Type": "application/json"}
payload = {"username": new_username, "password": password}

async def _8w(session):
    async with session.patch("https://discord.com/api/v9/users/@me", headers=headers, json=payload) as r:
        status = r.status
        try:
            data = await r.json()
        except:
            data = await r.text()
        if status == 200:
            print(f"[+] Username changed successfully: {data.get('username', 'N/A')}")
        elif status == 429:
            retry_after = data.get("retry_after", 1)
            print(f"[-] Rate Limited. Retry after {retry_after}s")
            await asyncio.sleep(retry_after)
        else:
            print(f"[-] {status} {str(data)[:100]}")

async def _8w_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [_8w(session) for _ in range(20)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

async def _8w_once():
    async with aiohttp.ClientSession() as session:
        await _8w(session)

asyncio.run(_8w_once())

# Note: if you want Turbo Mode (20 req/s) change _8w_once() to _8w_loop()
