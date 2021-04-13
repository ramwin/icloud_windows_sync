import git
import pathlib
import datetime
import re
from model import File


git_obj = git.cmd.Git()


def main():
    print("use git lfs to calculate the sha and save it to index.db")
    cnt = 0
    result = git_obj.execute('git lfs ls-files -l')
    for line in result.split("\n"):
        sha, path_str = re.split(r" [*-] ", line)
        path = pathlib.Path(path_str).absolute()
        if path.stat().st_size <= 1000:
            continue
        file_obj, created = File.get_or_create(
            path=str(path),
            defaults={
                "st_size": path.stat().st_size,
                "st_ctime": datetime.datetime.fromtimestamp(path.stat().st_ctime),
            }
        )
        if not file_obj.sha256sum:
            file_obj.sha256sum = sha
            file_obj.save()
        if file_obj.is_del:
            file_obj.is_del = False
            file_obj.save()
        assert file_obj.sha256sum == sha
        assert file_obj.st_size == path.stat().st_size
        cnt += 1
        if cnt % 100 == 0:
            print(f"   {cnt} handled")
    print(f"finished {len(File.filter(sha256sum=None))} file still have no sha256sum")


if __name__ == "__main__":
    main()
