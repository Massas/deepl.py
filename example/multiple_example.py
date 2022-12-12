import os

import deepl

text = ['I have a pen.', 'I don\'t hava a pen.']

translator = deepl.Translator(deepl.RequestsAdapter(os.getenv("DEEPL_API_KEY")))


def main():
    print(translator.translate_multi(text, target_lang=deepl.TargetLang.Japanese))
    print(translator.translate_multi(text, target_lang=deepl.TargetLang.Italian))


if __name__ == '__main__':
    main()
