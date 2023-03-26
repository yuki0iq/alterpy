import utils.common
import utils.log
import iuliia
import lemminflect
import spacy


log = utils.log.get("lang-en")

spacy_model_name = "en_core_web_md"
log.info("Probing spaCy-en...")
try:
    nlp = spacy.load(spacy_model_name)
except OSError:
    log.info("Model not found, downloading...")
    import spacy.cli.download
    spacy.cli.download(spacy_model_name)
    nlp = spacy.load(spacy_model_name)
log.info("spaCy-en OK!")


def inflect(s, form):
    return lemminflect.getInflection(s, form)[0]


def inflector(form):
    return lambda s: inflect(s, form)


def agree_with_number(s, num, _):
    if type(num) != int or abs(num) > 1:
        return s + "s"
    return s


def tr(s):
    return iuliia.translate(s, iuliia.WIKIPEDIA)


def to_role(line: str) -> tuple[str, bool]:
    doc = nlp(line)
    # for e in doc if e.pos_=="VERB" and e.dep_ in "ROOT advcl conj" -> inflect(past)
    res = []
    has_dobj = False
    for tok in doc:
        # print(tok, tok.pos_, tok.dep_)
        if tok.dep_ == "dobj":
            has_dobj = True
        s = str(tok)
        if tok.pos_ != "PUNCT":
            res.append(' ')
        if tok.pos_ == "VERB" and tok.dep_ in "ROOT advcl conj".split():
            res.append(inflect(s, 'VBD'))
        else:
            res.append(s)
    return ''.join(res).lstrip(), not has_dobj
