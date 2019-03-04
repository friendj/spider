import hashlib
import re


# 转换md5路径
def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_number(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num


if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode("utf-8")))
