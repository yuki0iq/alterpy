import aiohttp


async def correct(session: aiohttp.ClientSession, text: str) -> str:
    if not text:
        return ''

    text = text.replace('\r\n', '\n').replace('\r', '\n')

    url = 'https://speller.yandex.net/services/spellservice.json/checkText'
    async with session.post(url, data={'text': text}) as resp:
        data = await resp.json()
    
    data.sort(key=lambda x: (x['row'], x['col']), reverse=True)
    
    newlines = [0]
    for i in range(len(text)-1):
        if text[i] == '\n':
            newlines.append(i+1)

    pos = lambda r, c: newlines[r] + c
    for el in data:
        p = pos(el['row'], el['col'])
        l = el['len']
        s = el['s'][0]
        text = text[:p] + s + text[p+l:]

    return text

