# http://web.archive.org/web/20130617172843/https://ru.wikipedia.org/wiki/Участник:Tassadar/киричзи
import re
import utils.mecab
import utils.common
import utils.str

normalize = {
    'ゎ': 'わ', 'ゕ': 'か', 'ゖ': 'け',
    'ゐ': 'うぃ', 'ゑ': 'うぇ',
    'ヷ': 'ゔぃ', 'ヸ': 'ゔぃ', 'ヹ': 'ゔぇ', 'ヺ': 'ゔぉ',
    '！': '!', '？': '?', '。': '.', '、': ',', '：': ':', '；': ';',
}

consonants = set('кгсщзтчднхбпмрв')
vowels = set('аиуэоеяюё')

hiragana = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわをんゔゐゑ"
katakana = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヲンヴヰヱ"
K_to_H = {k: h for k, h in zip(katakana, hiragana)}

kana_to_ru = {
    'あ': 'а',  'い': 'и',   'う': 'у',   'え': 'э',  'お': 'о',
    'ぁ': 'ъа', 'ぃ': 'ъи',  'ぅ': 'ъу',  'ぇ': 'ъэ', 'ぉ': 'ъо',
    'か': 'ка', 'き': 'ки',  'く': 'ку',  'け': 'ке', 'こ': 'ко',
    'が': 'га', 'ぎ': 'ги',  'ぐ': 'гу',  'げ': 'ге', 'ご': 'го',
    'さ': 'са', 'し': 'щи',  'す': 'су',  'せ': 'сэ', 'そ': 'со',
    'ざ': 'за', 'じ': 'чзи', 'ず': 'зу',  'ぜ': 'зе', 'ぞ': 'зо',
    'た': 'та', 'ち': 'чи',  'つ': 'цу',  'て': 'тэ', 'と': 'то',
    'だ': 'да', 'ぢ': 'дзи', 'づ': 'дзу', 'で': 'дэ', 'ど': 'до',
    'な': 'на', 'に': 'ни',  'ぬ': 'ну',  'ね': 'нэ', 'の': 'но',
    'は': 'ха', 'ひ': 'хи',  'ふ': 'фу',  'へ': 'хе', 'ほ': 'хо',
    'ば': 'ба', 'び': 'би',  'ぶ': 'бу',  'べ': 'бе', 'ぼ': 'бо',
    'ぱ': 'па', 'ぴ': 'пи',  'ぷ': 'пу',  'ぺ': 'пе', 'ぽ': 'по',
    'ま': 'ма', 'み': 'ми',  'む': 'му',  'め': 'ме', 'も': 'мо',
    'ら': 'ра', 'り': 'ри',  'る': 'ру',  'れ': 'рэ', 'ろ': 'ро',
    'や': 'я',  'ゆ': 'ю',  'よ': 'ё',
    'ゃ': 'ъя', 'ゅ': 'ъю', 'ょ': 'ъё',
    'わ': 'ва', 'を': 'о',  'ん': 'н', 'ゔ': 'ву',
}

zero_special_n = {
    re.compile(r'\bざ'): 'дза',
    re.compile(r'\bず'): 'дзу',
    re.compile(r'\bぜ'): 'дзе',
    re.compile(r'\bぞ'): 'дзо',
}

first_special_n = {'んや': 'нъя', 'んゆ': 'нъю', 'んよ': 'нъё',}

second_special_n = {'нз': 'ндз', 'нп': 'мп', 'нб': 'мб',}

double_vowels = {
    'аи': 'ай', 'уи': 'уй', 'эи': 'ээ', 'ои': 'ой', 'еи': 'ээ',
    #'иа': 'йа', 'иу': 'йу', 'иэ': 'йэ', #'ио': 'йо',
    'оу': 'оо', 'ёу': 'ёо',
}

three_vowels = {'айи': 'аии'}

fix_vowels = {
    'щя': 'ща', 'щю': 'щу', 'щё': 'що',
    'чя': 'ча', 'чю': 'чу', 'чё': 'чо',
}


def re_sub(s, rule):
    for f, t in rule.items():
        s = re.sub(f, t, s)
    return s


def replace(s, rule):
    for f, t in rule.items():
        s = s.replace(f, t)
    return s


def fast_replace(s, rule):
    res = []
    for c in s:
        res.append(rule[c] if c in rule else c)
    return ''.join(res)


def fix_long_vowels(s):
    """
    Replace long vowel marks
    a- -> aa, i- -> ii, u- -> uu, e- -> ee, o- -> ou, ya- -> yaa, yu- -> yuu, yo- -> you
    """
    next = {'а': 'あ', 'и': 'い', 'у': 'う', 'э': 'え', 'о': 'お', 'е': 'え', 'я': 'あ', 'ю': 'う', 'ё': 'う', '-': 'ー'}
    s = list(s)
    last = '-'
    for i, c in enumerate(s):
        if c == 'ー':
            s[i] = next[last]
        if c in kana_to_ru:
            tmp = kana_to_ru[c][-1]
            last = tmp if tmp in vowels else '-'
    return ''.join(s)


def fix_double_consonants(s):
    """
    Replace double cons. marks
    qki -> kki
    """
    s = list(s)[::-1]
    last = '-'
    for i, c in enumerate(s):
        if c == 'っ':
            s[i] = last
        if c in consonants:
            last = c
    return ''.join(s[::-1])


def fix_combined(s):
    """
    Replace combination marks
    bi#ya -> bya
    a#a -> a

    #! Ci#ya -> Cya  DEL
    #! u#ya -> wya  SKIP
    #! vu#ya -> vya  DEL
    #! i#e -> йе EXCEPTIONAL
    #! se, te, de, tsu, fu, shi, ji #ya -> sya, tya, ...  DEL
    #! ?V#V -> SKIP
    """
    combined_need_replace = {'ву', 'сэ', 'тэ', 'дэ', 'цу', 'фу'}
    s = list(s)
    n = len(s)
    for i in range(1, n):
        if s[i] == 'ъ' and s[i - 1] in vowels:
            s[i] = ''
            if i != 1 and (s[i - 1] == 'и' or (s[i - 2] + s[i - 1]) in combined_need_replace):
                s[i - 1] = ''
            elif s[i - 1] == 'у':
                s[i - 1] = 'в'
            elif i + 1 < n and s[i - 1] == 'и' and s[i + 1] == 'э':
                s[i - 1], s[i + 1] = 'й', 'е'
    return ''.join(s)


def capitalize(s):
    """
    Fix capitalization with name hints from mecab
    ##yuki -> Yuki
    """

    s = list(s)
    n = len(s)
    for i in range(2, n):
        if s[i - 2] == s[i - 1] == '#':
            s[i] = s[i].upper()
            s[i - 2] = s[i - 1] = ''
    return ''.join(s)


def to(s):
    s = fast_replace(s, K_to_H)
    s = fast_replace(s, normalize)
    s = fix_long_vowels(s)
    s = re_sub(s, zero_special_n)
    s = replace(s, first_special_n)
    s = fast_replace(s, kana_to_ru)
    s = replace(s, second_special_n)
    s = fix_combined(s)
    s = replace(s, double_vowels)
    s = replace(s, three_vowels)
    s = replace(s, fix_vowels)
    s = fix_double_consonants(s)
    s = capitalize(s)
    return s


def parse(s):
    res = []
    for line in utils.common.split_by_func(s, utils.str.is_kanji):
        if utils.str.is_kanji(line):
            line = to(utils.mecab.reading(line))
        res.append(line)
    return ''.join(res)


if __name__ == '__main__':
    assert(to('しろい') == 'щирой')
    assert(to('でんしゃ') == 'дэнща')
    assert(to('ばしょ') == 'бащо')
    assert(to('ちいさい') == 'чиисай')
    assert(to('ともだち') == 'томодачи')
    assert(to('ちょしょ') == 'чощо')
    assert(to('キリじ') == 'киричзи')
    assert(to('じぶん') == 'чзибун')
    assert(to('だいじょうぶ') == 'дайчзёобу')
    assert(to('かぜ') == 'казе')
    assert(to('かぞく') == 'казоку')
    assert(to('ずっと') == 'зутто')  # word begin!
    assert(to('まんぞく') == 'мандзоку')
    assert(to('とおい') == 'тоой')
    assert(to('さようなら') == 'саёонара')
    assert(to('ゆうき') == 'юуки')
    assert(to('ほうこう') == 'хоокоо')
    assert(to('いい') == 'ии')
    assert(to('いっぱい') == 'иппай')
    assert(to('かわいい') == 'каваии')
    assert(to('こんや') == 'конъя')
    assert(to('うんめい') == 'унмээ')
    assert(to('せんぱい') == 'сэмпай')
    assert(to('ふつう') == 'фуцуу')
    assert(to('つづく') == 'цудзуку')
    assert(to('エッチ') == 'эччи')
    assert(to('いっしょ') == 'ищщо')
    assert(to('まぁね') == 'маанэ')
    assert(to('エヴァンゲリオン') == 'эвангерион')
    assert(to('ティケット') == 'тикетто')
    assert(to('ねぇ おきて') == 'нээ окитэ')
    assert(to('くうそう メソロギヰ') == 'куусоо месорогиви')
    assert(to('イェ') == 'йе')
    print('passed')
