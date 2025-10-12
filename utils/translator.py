from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    'tr': 'Turkish', 'en': 'English', 'es': 'Spanish', 'fr': 'French',
    'de': 'German', 'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian',
    'ja': 'Japanese', 'ko': 'Korean', 'zh-CN': 'Chinese', 'ar': 'Arabic',
    'hi': 'Hindi', 'bn': 'Bengali', 'ur': 'Urdu', 'fa': 'Persian'
    # 43 dil daha eklenecek...
}

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Metni çevir"""
    try:
        if source_lang == target_lang:
            return text
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except:
        return text  # Hata olursa orijinal metni döndür
