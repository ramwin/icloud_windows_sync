import os
import pathlib
from model import File
import datetime
import update_sha
import logging
import re


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
        return super().__call__(path0, path1)

    def get_weight(self, path):
        return -len(path.stem)


rules = [
    IcloudFirstRule(),
    MatchYearMonthRule(),
    ShortNameRule(),
]

def keep_and_delete(path0, path1, rules):
    """
    return         keeppath: path0,       deletepath: path1
    """
    for rule in rules:
        if rule(path0, path1):
            return rule(path0, path1)
    raise Exception("I don't know which to delete")


def main():
    for item in File.raw("select sha256sum, count(id) total from file where sha256sum is not null and is_del = False group by sha256sum having total > 2"):
        sha256sum = item.sha256sum
        files = [file_obj for file_obj in File.filter(sha256sum=sha256sum, is_del=False)]
        while len(files) >= 2:
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
