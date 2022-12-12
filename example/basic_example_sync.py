import os

import deepl

text = 'I have a pen.'

translator = deepl.Translator(deepl.AiohttpAdapter(os.getenv("DEEPL_API_KEY")))


def main():
    print(translator.translate(text, target_lang=deepl.TargetLang.Japanese))
    print(translator.translate(text, target_lang=deepl.TargetLang.Italian))


if __name__ == '__main__':
    main()
