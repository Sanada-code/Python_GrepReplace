import glob
import os
import sys
import stat
import chardet
import Setting
import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler('./logger.log', mode='a', encoding='utf-8')
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def replace_file():
    setting = Setting.Setting(logger)
    glob_path = setting.get_grep_dir() + '\\**\\*.*'
    replace_words = setting.get_replace_words()

    for filename in glob.glob(glob_path, recursive=True):
        # ファイル名終端で除外拡張子判定 小文字で比較
        if filename.lower().endswith(setting.get_exclude_extension()):
            continue

        print("filename:", filename)
        unlock_readonly(filename)
        charset = get_charset(filename)
        if charset is None:
            continue

        for replaceFrom, replaceTo in replace_words.items():
            do_replace(filename, replaceFrom, replaceTo, charset)


def write_line(filename, lines, charset):
    try:
        with open(filename, 'w', encoding=charset) as f:
            f.write(lines)
    except:
        logger.exception(sys.exc_info())


def read_line(filename, charset):
    try:
        with open(filename, encoding=charset) as f:
            return f.read()
    except:
        logger.exception(sys.exc_info())


def do_replace(filename, replace_word_from, replace_word_to, charset):
    line_src = read_line(filename, charset)
    # null除外
    if line_src is None:
        return
    # 文字列を置換
    line_replaced = line_src.replace(replace_word_from, replace_word_to)

    # 置換後文字列が同じなら何もしない
    if line_src == line_replaced:
        return
    write_line(filename, line_replaced, charset)
    print('CHANGED:', filename)


# 文字コード取得
def get_charset(filename):
    with open(filename, 'rb') as f:
        charset = chardet.detect(f.read())
        print(charset)
        return charset['encoding']


# 読み取り専用解除
def unlock_readonly(filename):
    if not os.access(filename, os.W_OK):
        os.chmod(filename, stat.S_IWRITE)


if __name__ == '__main__':
    replace_file()
