import aiohttp


async def correct(session: aiohttp.ClientSession, text: str) -> str:
    if not text:
        return ''

    text = text.replace('\r\n', '\n').replace('\r', '\n')

    url = 'https://speller.yandex.net/services/spellservice.json/checkText'
    async with session.post(url, data={'text': text}) as resp:
        data = await resp.json()
    
    data.sort(key=lambda x: x['pos'], reverse=True)
    
    for el in data:
        p = el['pos']
        if p and text[p-1] == '@':
            continue
        l = el['len']
        s = el['s'][0]
        text = text[:p] + s + text[p+l:]

    return text

