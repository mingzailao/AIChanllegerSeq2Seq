from __future__ import print_function
import jieba
import nltk


def _preprocess_sgm(line, is_sgm):
    """Preprocessing to strip tags in SGM files."""
    if not is_sgm:
        return line
    # In SGM files, remove <srcset ...>, <p>, <doc ...> lines.
    if line.startswith("<srcset") or line.startswith("</srcset"):
        return ""
    if line.startswith("<refset") or line.startswith("</refset"):
        return ""
    if line.startswith("<doc") or line.startswith("</doc"):
        return ""
    if line.startswith("<p>") or line.startswith("</p>"):
        return ""
    # Strip <seg> tags.
    line = line.strip()
    if line.startswith("<seg") and line.endswith("</seg>"):
        i = line.index(">")
        return line[i+1:-6]  # Strip first <seg ...> and last </seg>.


def tokenize(line, is_sgm=False, is_zh=False, lower_case=True, delim=' '):
    # strip sgm tags if any
    _line = _preprocess_sgm(line, is_sgm)
    # replace non-breaking whitespace
    _line = _line.replace("\xa0", " ").strip()
    # tokenize
    _tok = jieba.cut(_line.rstrip('\r\n')) if is_zh else nltk.word_tokenize(
        _line)
    _tokenized = delim.join(_tok)
    # lowercase. ignore if chinese.
    _tokenized = _tokenized.lower() if lower_case and not is_zh else _tokenized
    return _tokenized


def tokenized(filepath):
    tokenized = ''
    flag_sgm = filepath.endswith('.sgm')
    flag_zh  = filepath.endswith('.zh') or filepath.endswith('.zh.sgm')
    flag_lowwer = not flag_zh
    with open(filepath,'rb') as f:
        for index,line in enumerate(f):
            line=line.decode('utf-8')
            _tokenized = tokenize(line, flag_sgm, flag_zh, flag_lowwer, ' ')
            tokenized+="%s\n" % _tokenized
    return tokenized

def write_ob(filename,ob):
    with open(filename,'r') as f:
        f.write(ob)
    