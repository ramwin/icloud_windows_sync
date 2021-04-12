import os
import pathlib
import git
from model import *
import datetime
import logging
import re


git_obj = git.cmd.Git()

def keep_and_delete(path0, path1):
    """
    return         keeppath: path0,       deletepath: path1
    """
    str_path_0 = str(path0)
    str_path_1 = str(path1)
    if "icloud" in str_path_0 and "icloud" not in str_path_1:
        return path0, path1
    elif "icloud" in str_path_0 and "icloud" not in str_path_1:
        return path1, path0
    year_month_pattern = r"/\d{4}/\d{1,2}/"
    if re.match(year_month_pattern, str_path_0) and not re.match(year_month_pattern, str_path_1):
        return path0, path1
    elif re.match(year_month_pattern, str_path_1) and not re.match(year_month_pattern, str_path_0):
        return path1, path0
    if str(path0.parent) == str(path1.parent):
        if len(path0.stem) > len(path1.stem):
            return path1, path0
        elif len(path0.stem) < len(path1.stem):
            return path0, path1    

def main(act=False):
    cnt = 0
    result = git_obj.execute('git lfs ls-files -l')
    for line in result.split("\n"):
        # print(f"处理{line}")
        cnt += 1
        if cnt % 100 == 0:
            print(f"当前处理了 {cnt}")
        sha, path_str = re.split(r" [*-] ", line)
        path = pathlib.Path(path_str)
        if path.stat().st_size <= 1000:
            continue
        file_obj, created = File.get_or_create(
            sha256sum=sha,
            defaults={
                "path": path_str,
                "st_size": path.stat().st_size,
                "st_ctime": datetime.datetime.fromtimestamp(path.stat().st_ctime),
            }
        )
        if created or pathlib.Path(file_obj.path) == path:
            continue
        result = keep_and_delete(path, pathlib.Path(file_obj.path))
        if not result:
            print(f"报错 {path}")
            continue
        keeppath, deletepath = keep_and_delete(path, pathlib.Path(file_obj.path) )
        print(f"保留: {keeppath}, \n删除: {deletepath}")
        if act:
            file_obj.path = str(keeppath)
            file_obj.save()
            if deletepath.exists():
                os.unlink(deletepath)


if __name__ == "__main__":
    main(act=True)
