import os
import pathlib
from model import File
from PIL import Image
import datetime
import update_sha
import logging
import re
from decimal import Decimal
from log import logger


class BaseRule:

    def __init__(self):
        pass

    def __call__(self, file0, file1):
        """
        return [keep_path, delete_path]
        """
        path0_weight = self.get_weight(pathlib.Path(file0.path))
        path1_weight = self.get_weight(pathlib.Path(file1.path))
        if path0_weight == path1_weight:
            return None
        elif path0_weight > path1_weight:
            return file0, file1
        else:
            return file1, file0

    def get_weight(self, path):
        raise NotImplementedError("please change this function")


class IcloudFirstRule(BaseRule):

    def get_weight(self, path):
        if "icloud" in str(path):
            return 1
        return 0


class MatchYearMonthRule(BaseRule):

    def get_weight(self, path):
        year_month_pattern = r".*/(?P<year>\d{4})/(?P<month>\d{1,2})"
        if re.match(year_month_pattern, str(path).replace("\\", "/")):
            return 1
        return 0


class ShortNameRule(BaseRule):

    def __call__(self, file0, file1):
        if pathlib.Path(file0.path).absolute().parent != \
                pathlib.Path(file1.path).absolute().parent:
            return None
        return super().__call__(file0, file1)

    def get_weight(self, path):
        return -len(path.stem)


class ImgtimeRule(BaseRule):

    def get_weight(self, path):
        if path.suffix.lower() not in [".png", ".jpg"]:
            return 0
        exif = Image.open(path).getexif()
        if 306 in exif:
            create_datetime = datetime.datetime.strptime(exif[306][0:19], "%Y:%m:%d %H:%M:%S")
            if f"\\{create_datetime.year}\\{create_datetime.month}\\" in str(path).replace("/", "\\"):
                return 1
            else:
                return 0


class TimeOlderRule(BaseRule):

    def get_weight(self, path):
        year_month_pattern = r".*/(?P<year>\d{4})/(?P<month>\d{1,2})"
        match = re.match(year_month_pattern, str(path).replace("\\", "/"))
        if match:
            return - int(match.groupdict()["year"]) * 12 - int(match.groupdict()["month"])


class KeepOriginNameRule(BaseRule):

    def __call__(self, file0, file1):
        if pathlib.Path(file0.path).absolute().parent != \
                pathlib.Path(file1.path).absolute().parent:
            return None
        return super().__call__(file0, file1)

    def get_weight(self, path):
        logger.info(path)
        match = re.match(r".*\((?P<alias>[1-3])\)\.\S*", path.name)
        if match is None:
            result = Decimal("inf")
        else:
            result = -Decimal(match.groupdict()["alias"])
        logging.info(result)
        return result


rules = [
    IcloudFirstRule(),
    MatchYearMonthRule(),
    ShortNameRule(),
    ImgtimeRule(),
    TimeOlderRule(),
    KeepOriginNameRule(),
]

def keep_and_delete(path0, path1, rules):
    """
    return         keeppath: path0,       deletepath: path1
    """
    for rule in rules:
        # print(f"use {type(rule)}")
        if rule(path0, path1):
            return rule(path0, path1)
    raise Exception(f"I don't know which to delete: \n    {path0.path}\n    {path1.path}")


def main():
    for item in File.raw("select sha256sum, count(id) total from file where sha256sum is not null and is_del = False group by sha256sum having total >= 2"):
        sha256sum = item.sha256sum
        files = [file_obj for file_obj in File.filter(sha256sum=sha256sum, is_del=False)]
        while len(files) >= 2:
            print(f"{files[0]} VS {files[1]}")
            keep_file, delete_file = keep_and_delete(
                files[0],
                files[1],
                rules)
            print(f"    delete: {delete_file.path}")
            print(f"      keep: {keep_file.path}")
            delete_file.is_del = True
            delete_file.save()
            os.unlink(delete_file.path)
            files.remove(delete_file)


if __name__ == "__main__":
    main()
