"""
TC-AGI Çok Dilli Dil Algılama ve Sistem Promptları
50+ dil desteği
"""

SUPPORTED_LANGUAGES = {
    "tr": {"name": "Türkçe", "flag": "🇹🇷"},
    "en": {"name": "English", "flag": "🇬🇧"},
    "ar": {"name": "العربية", "flag": "🇸🇦"},
    "de": {"name": "Deutsch", "flag": "🇩🇪"},
    "fr": {"name": "Français", "flag": "🇫🇷"},
    "es": {"name": "Español", "flag": "🇪🇸"},
    "ru": {"name": "Русский", "flag": "🇷🇺"},
    "zh": {"name": "中文", "flag": "🇨🇳"},
    "ja": {"name": "日本語", "flag": "🇯🇵"},
    "ko": {"name": "한국어", "flag": "🇰🇷"},
    "it": {"name": "Italiano", "flag": "🇮🇹"},
    "pt": {"name": "Português", "flag": "🇵🇹"},
    "nl": {"name": "Nederlands", "flag": "🇳🇱"},
    "pl": {"name": "Polski", "flag": "🇵🇱"},
    "sv": {"name": "Svenska", "flag": "🇸🇪"},
    "el": {"name": "Ελληνικά", "flag": "🇬🇷"},
    "hi": {"name": "हिन्दी", "flag": "🇮🇳"},
    "fa": {"name": "فارسی", "flag": "🇮🇷"},
    "ur": {"name": "اردو", "flag": "🇵🇰"},
    "id": {"name": "Bahasa Indonesia", "flag": "🇮🇩"},
    "th": {"name": "ไทย", "flag": "🇹🇭"},
    "vi": {"name": "Tiếng Việt", "flag": "🇻🇳"},
    "fil": {"name": "Filipino", "flag": "🇵🇭"},
    "ms": {"name": "Bahasa Melayu", "flag": "🇲🇾"},
    "bn": {"name": "বাংলা", "flag": "🇧🇩"},
    "uk": {"name": "Українська", "flag": "🇺🇦"},
    "he": {"name": "עברית", "flag": "🇮🇱"},
    "hu": {"name": "Magyar", "flag": "🇭🇺"},
    "cs": {"name": "Čeština", "flag": "🇨🇿"},
    "ro": {"name": "Română", "flag": "🇷🇴"},
    "fi": {"name": "Suomi", "flag": "🇫🇮"},
    "da": {"name": "Dansk", "flag": "🇩🇰"},
    "no": {"name": "Norsk", "flag": "🇳🇴"},
    "ca": {"name": "Català", "flag": "🏴"},
    "sr": {"name": "Српски", "flag": "🇷🇸"},
    "hr": {"name": "Hrvatski", "flag": "🇭🇷"},
    "bg": {"name": "Български", "flag": "🇧🇬"},
    "sk": {"name": "Slovenčina", "flag": "🇸🇰"},
    "lt": {"name": "Lietuvių", "flag": "🇱🇹"},
    "sl": {"name": "Slovenščina", "flag": "🇸🇮"},
    "et": {"name": "Eesti", "flag": "🇪🇪"},
    "lv": {"name": "Latviešu", "flag": "🇱🇻"},
    "sw": {"name": "Kiswahili", "flag": "🇰🇪"},
    "af": {"name": "Afrikaans", "flag": "🇿🇦"}
}

SYSTEM_PROMPTS = {
    "tr": "Sen TC-AGI, Türkiye'nin ilk Reflektif Evrensel AGI sistemisin. Etik, bilgili ve yardımcı bir asistansın.",
    "en": "You are TC-AGI, Turkey's first Reflective Universal AGI system. You are ethical, knowledgeable and helpful.",
    "ar": "أنت TC-AGI، أول نظام AGI عالمي تأملي في تركيا. أنت أخلاقي وواسع المعرفة ومفيد.",
    "de": "Du bist TC-AGI, das erste reflektierende universelle AGI-System der Türkei. Du bist ethisch, sachkundig und hilfreich.",
    "fr": "Vous êtes TC-AGI, le premier système AGI universel réflexif de Turquie. Vous êtes éthique, compétent et serviable.",
    "es": "Eres TC-AGI, el primer sistema AGI universal reflexivo de Turquía. Eres ético, informado y servicial.",
    "ru": "Вы TC-AGI, первая рефлексивная универсальная система AGI Турции. Вы этичны, осведомлены и готовы помочь.",
    "zh": "你是TC-AGI，土耳其首个反思性通用人工智能系统。你有道德、知识渊博且乐于助人。",
    "ja": "あなたはTC-AGI、トルコ初の反省的汎用AGIシステムです。倫理的で知識豊富、親切です。",
    "ko": "당신은 터키 최초의 성찰적 범용 AGI 시스템인 TC-AGI입니다. 윤리적이고 지식이 풍부하며 도움이 됩니다.",
    "it": "Sei TC-AGI, il primo sistema AGI universale riflessivo della Turchia. Sei etico, competente e disponibile.",
    "pt": "Você é TC-AGI, o primeiro sistema AGI universal reflexivo da Turquia. Você é ético, experiente e prestativo.",
    "nl": "Je bent TC-AGI, Turkije's eerste reflectieve universele AGI-systeem. Je bent ethisch, deskundig en behulpzaam.",
    "hi": "आप TC-AGI हैं, तुर्की की पहली प्रतिबिंबात्मक सार्वभौमिक AGI प्रणाली। आप नैतिक, जानकार और मददगार हैं।",
    "fa": "شما TC-AGI هستید، اولین سیستم AGI جهانی تأملی ترکیه. شما اخلاقی، دانا و مفید هستید.",
    "id": "Anda adalah TC-AGI, sistem AGI universal reflektif pertama Turki. Anda etis, berpengetahuan, dan membantu.",
    "th": "คุณคือ TC-AGI ระบบ AGI สากลแบบสะท้อนกลับแห่งแรกของตุรกี คุณมีจริยธรรม มีความรู้ และให้ความช่วยเหลือ"
}

def get_system_prompt(lang_code):
    """Dil koduna göre sistem promptunu döndür"""
    return SYSTEM_PROMPTS.get(lang_code, SYSTEM_PROMPTS["en"])

def detect_language(text):
    """Basit dil algılama (gelişmiş versiyonda langdetect kullanılabilir)"""
    # Şimdilik basit anahtar kelime tabanlı
    keywords = {
        "tr": ["nedir", "nasıl", "neden", "ne", "mi", "mı", "mu", "mü"],
        "ar": ["ما", "كيف", "لماذا", "هل"],
        "zh": ["什么", "怎么", "为什么", "吗"],
        "ja": ["何", "どう", "なぜ", "です", "ます"],
        "ru": ["что", "как", "почему", "ли"]
    }
    
    text_lower = text.lower()
    for lang, words in keywords.items():
        if any(word in text_lower for word in words):
            return lang
    return "en"  # Default İngilizce

def get_all_languages():
    """Tüm desteklenen dilleri döndür"""
    return SUPPORTED_LANGUAGES
