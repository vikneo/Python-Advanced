import os
import re


BASE_DIR = os.path.dirname(__file__)

PATH_TO_DB = os.path.join(BASE_DIR, 'library.db')
PATH_TO_FORLDER_FILE = os.path.join(BASE_DIR, 'files')
PATH_TO_CSV = os.path.join(BASE_DIR, "students.csv")

ALLOWED_EXTENSIONS = ['csv']

ALPHABET = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'j',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ь': '',
    'ы': 'y',
    'ъ': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    }


def cleaned_text(data: str) -> str:
    """
    Очистка текста от знаков препинания.

    :param data: Для форматирования от знаков препинания.
    :rtype : str.
    :return : str.
    """
    own_text = ''.join(re.findall(r'[ \w*0-9]', data))
    return own_text


def slugify(text: str) -> str:
    """
    Преобразование символов кириллицы в символы латиницы из отформатированного текста.

    :param text: Отформатированный текст.
    :return: str.
    """
    _res = []
    own_text = cleaned_text(data=text)
    _text = own_text.replace(' ', '-').lower()

    for _char in _text:
        _res.append(ALPHABET[_char] if _char in ALPHABET.keys() else _char)

    return ''.join(_res)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
