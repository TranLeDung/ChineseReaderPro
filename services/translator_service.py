from deep_translator import (
    GoogleTranslator
)

from services.translation_cache_service import (
    load_cache,
    save_cache
)


def translate_to_vi(text):

    cache = load_cache()

    if text in cache:

        return cache[text]

    try:

        result = GoogleTranslator(
            source="zh-CN",
            target="vi"
        ).translate(text)

        cache[text] = result

        save_cache(cache)

        return result

    except Exception:

        return "⚠ Không thể kết nối dịch vụ dịch"