import utils.log
import fugashi


log = utils.log.get('mecab')

log.info("Probing MeCab...")
try:
    tagger = fugashi.Tagger()
except RuntimeError:
    log.warning("Dictionary not found, downloading...")
    import unidic.download
    unidic.download.download_version()
    log.info("Dictionary downloaded")
    tagger = fugashi.Tagger()
log.info("MeCab OK!")


def reading(s):
    rea = []
    for word in tagger(s):
        if '空白' == word.feature.pos1:
            continue
        if '名' in word.feature.pos3:
            rea.append("##")
        if '補助記号' == word.feature.pos1:
            rea.append("#space#")
        rea.append((word.feature.pron if word.feature.pron != "*" else word.feature.lemma) or word.surface)
        if '補助記号' == word.feature.pos1:
            if '点' not in word.feature.pos2:
                rea.append("#space#")
        # print(word.feature)
    return (' '.join(rea)).replace("## ", "##").replace(" #space# ", "").replace("#space# ", "").replace(" #space#", "")


