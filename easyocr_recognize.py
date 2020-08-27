import numpy as np
import easyocr_tools
import sys
import time


import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


LANG_AFRIKAANS_NAME          = 'Afrikaans'
LANG_ARABIC_NAME             = 'Arabic'
LANG_AZERBAIJANI_NAME        = 'Azerbaijani'
LANG_BELARUSIAN_NAME         = 'Belarusian'
LANG_BULGARIAN_NAME          = 'Bulgarian'
LANG_BOSNIAN_NAME            = 'Bosnian'
LANG_SIMPLIFIEDCHINESE_NAME  = 'Simplified Chinese'
LANG_TRADITIONALCHINESE_NAME = 'Traditional Chinese'
LANG_CZECH_NAME              = 'Czech'
LANG_WELSH_NAME              = 'Welsh'
LANG_DANISH_NAME             = 'Danish'
LANG_GERMAN_NAME             = 'German'
LANG_ENGLISH_NAME            = 'English'
LANG_SPANISH_NAME            = 'Spanish'
LANG_ESTONIAN_NAME           = 'Estonian'
LANG_PERSIAN_NAME            = 'Persian (Farsi)'
LANG_FRENCH_NAME             = 'French'
LANG_IRISH_NAME              = 'Irish'
LANG_HINDI_NAME              = 'Hindi'
LANG_CROATIAN_NAME           = 'Croatian'
LANG_HUNGARIAN_NAME          = 'Hungarian'
LANG_INDONESIAN_NAME         = 'Indonesian'
LANG_ICELANDIC_NAME          = 'Icelandic'
LANG_ITALIAN_NAME            = 'Italian'
LANG_JAPANESE_NAME           = 'Japanese'
LANG_KOREAN_NAME             = 'Korean'
LANG_KURDISH_NAME            = 'Kurdish'
LANG_LATIN_NAME              = 'Latin'
LANG_LITHUANIAN_NAME         = 'Lithuanian'
LANG_LATVIAN_NAME            = 'Latvian'
LANG_MAORI_NAME              = 'Maori'
LANG_MONGOLIAN_NAME          = 'Mongolian'
LANG_MARATHI_NAME            = 'Marathi'
LANG_MALAY_NAME              = 'Malay'
LANG_MALTESE_NAME            = 'Maltese'
LANG_NEPALI_NAME             = 'Nepali'
LANG_DUTCH_NAME              = 'Dutch'
LANG_NORWEGIAN_NAME          = 'Norwegian'
LANG_OCCITAN_NAME            = 'Occitan'
LANG_POLISH_NAME             = 'Polish'
LANG_PORTUGUESE_NAME         = 'Portuguese'
LANG_ROMANIAN_NAME           = 'Romanian'
LANG_SERBIANCYRILLIC_NAME    = 'Serbian (cyrillic)'
LANG_SERBIANLATIN_NAME       = 'Serbian (latin)'
LANG_SLOVAK_NAME             = 'Slovak (need revisit)'
LANG_SLOVENIAN_NAME          = 'Slovenian'
LANG_ALBANIAN_NAME           = 'Albanian'
LANG_SWEDISH_NAME            = 'Swedish'
LANG_SWAHILI_NAME            = 'Swahili'
LANG_TAMIL_NAME              = 'Tamil'
LANG_THAI_NAME               = 'Thai'
LANG_TAGALOG_NAME            = 'Tagalog'
LANG_TURKISH_NAME            = 'Turkish'
LANG_UYGHUR_NAME             = 'Uyghur'
LANG_UKRANIAN_NAME           = 'Ukranian'
LANG_URDU_NAME               = 'Urdu'
LANG_UZBEK_NAME              = 'Uzbek'
LANG_VIETNAMESE_NAME         = 'Vietnamese (need revisit)'
LANG_NAME_TO_FLAG = {
    LANG_AFRIKAANS_NAME         : 'af',
    LANG_ARABIC_NAME            : 'ar',
    LANG_AZERBAIJANI_NAME       : 'az',
    LANG_BELARUSIAN_NAME        : 'be',
    LANG_BULGARIAN_NAME         : 'bg',
    LANG_BOSNIAN_NAME           : 'bs',
    LANG_SIMPLIFIEDCHINESE_NAME : 'ch_sim',
    LANG_TRADITIONALCHINESE_NAME: 'ch_tra',
    LANG_CZECH_NAME             : 'cs',
    LANG_WELSH_NAME             : 'cy',
    LANG_GERMAN_NAME            : 'de',
    LANG_ENGLISH_NAME           : 'en',
    LANG_SPANISH_NAME           : 'es',
    LANG_ESTONIAN_NAME          : 'et',
    LANG_PERSIAN_NAME           : 'fa',
    LANG_FRENCH_NAME            : 'fr',
    LANG_IRISH_NAME             : 'ga',
    LANG_HINDI_NAME             : 'hi',
    LANG_CROATIAN_NAME          : 'hr',
    LANG_HUNGARIAN_NAME         : 'hu',
    LANG_INDONESIAN_NAME        : 'id',
    LANG_ICELANDIC_NAME         : 'is',
    LANG_ITALIAN_NAME           : 'it',
    LANG_JAPANESE_NAME          : 'ja',
    LANG_KOREAN_NAME            : 'ko',
    LANG_KURDISH_NAME           : 'ku',
    LANG_LATIN_NAME             : 'la',
    LANG_LITHUANIAN_NAME        : 'lt',
    LANG_LATVIAN_NAME           : 'lv',
    LANG_MAORI_NAME             : 'mi',
    LANG_MONGOLIAN_NAME         : 'mn',
    LANG_MARATHI_NAME           : 'mr',
    LANG_MALAY_NAME             : 'ms',
    LANG_MALTESE_NAME           : 'mt',
    LANG_NEPALI_NAME            : 'ne',
    LANG_DUTCH_NAME             : 'nl',
    LANG_NORWEGIAN_NAME         : 'no',
    LANG_OCCITAN_NAME           : 'oc',
    LANG_POLISH_NAME            : 'pl',
    LANG_PORTUGUESE_NAME        : 'pt',
    LANG_ROMANIAN_NAME          : 'ro',
    LANG_SERBIANCYRILLIC_NAME   : 'rs_cyrillic',
    LANG_SERBIANLATIN_NAME      : 'rs_latin',
    LANG_SLOVAK_NAME            : 'sk',
    LANG_SLOVENIAN_NAME         : 'sl',
    LANG_ALBANIAN_NAME          : 'sq',
    LANG_SWEDISH_NAME           : 'sv',
    LANG_SWAHILI_NAME           : 'sw',
    LANG_TAMIL_NAME             : 'ta',
    LANG_THAI_NAME              : 'th',
    LANG_TAGALOG_NAME           : 'tl',
    LANG_TURKISH_NAME           : 'tr',
    LANG_UYGHUR_NAME            : 'ug',
    LANG_UKRANIAN_NAME          : 'uk',
    LANG_URDU_NAME              : 'ur',
    LANG_UZBEK_NAME             : 'uz',
    LANG_VIETNAMESE_NAME        : 'vi'
}
LANG_FLAG_TO_NAME = {v: k for k, v in LANG_NAME_TO_FLAG.items()}


select_langs = [LANG_NAME_TO_FLAG[LANG_ENGLISH_NAME]]

reader = None

def print_out(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def on_set(k, v):
    if k == 'select_langs':
        global select_langs
        select_langs = [ LANG_NAME_TO_FLAG[x] for x in v.split(',') ]

def on_get(k):
    if k == 'select_langs':
        return ','.join([ LANG_FLAG_TO_NAME[x] for x in select_langs ])


def on_init():
    global reader
    reader = easyocr_tools.init_recognizer(select_langs)
    return True


def on_run(image):
    result = easyocr_tools.recognize(reader, image)
    draw_image = easyocr_tools.draw_text(image, result)
    text = ','.join([ x[1] for x in result ])
    locations = [ x[0] for x in result ]
    return {'draw_image': draw_image, 'text_list': text, 'text_locations': np.array(locations)}

