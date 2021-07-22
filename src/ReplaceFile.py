import datetime
import glob
import os
import sys
import stat
import chardet
import Setting
import logging
import logging.handlers

# ログの初期設定
def setup_logger(log_folder = '{0}.log'.format(datetime.date.today())):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    fh = logging.handlers.RotatingFileHandler(log_folder, backupCount=7, mode='a', encoding='utf-8')

    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger


def replace_file():
    setting = Setting.Setting(logger)
    glob_path = setting.get_grep_dir() + '\\**\\*.*'
    replace_words = setting.get_replace_words()
    for filename in glob.glob(glob_path, recursive=True):
        # ファイル名終端で除外拡張子判定 小文字で比較
        if filename.lower().endswith(setting.get_exclude_extension()):
            continue

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
            logger.debug("file changed:" + filename)
            return True
    except:
        logger.debug(sys.exc_info())


def read_line(filename, charset):
    try:
        with open(filename, encoding=charset) as f:
            return f.read()
    except:
        logger.debug(sys.exc_info())


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


# 文字コード取得
def get_charset(filename):
    with open(filename, 'rb') as f:
        charset = chardet.detect(f.read())
        return charset['encoding']


# 読み取り専用解除
def unlock_readonly(filename):
    if not os.access(filename, os.W_OK):
        os.chmod(filename, stat.S_IWRITE)


if __name__ == '__main__':
    logger = setup_logger()
    replace_file()
