import asyncio
import os

import deepl

text = 'I have a pen.'

translator = deepl.Translator(deepl.AiohttpAdapter(os.getenv("DEEPL_API_KEY")))


async def main():
    print(await translator.translate(text, target_lang=deepl.TargetLang.Japanese))
    print(await translator.translate(text, target_lang=deepl.TargetLang.Italian))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
