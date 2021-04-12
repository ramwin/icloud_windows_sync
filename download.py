#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2021-04-10 09:56:11

import hashlib
import peewee
import json
import pathlib
import os
import shutil
import datetime
from settings import CLOUD_PATH, BACK_PATH
import subprocess
import model



def main(count=1000):
    model.db.connect()
    for cloud_file in CLOUD_PATH.iterdir():
        try:
            print(f"INFO: handling {cloud_file}")
            count -= 1
            if count % 10 == 0:
                print(f"    remaining: {count}, time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            if count < 0:
                return
            st_ctime = datetime.datetime.fromtimestamp(cloud_file.stat().st_ctime)
            directory = BACK_PATH.joinpath(str(st_ctime.year)).joinpath(str(st_ctime.month))
            if not directory.exists():
                os.makedirs(directory)
            local_file = directory.joinpath(cloud_file.name)
            if not local_file.exists():
                shutil.copy2(cloud_file, local_file)
            else:
                print(f"    luck, file exist")
            if local_file.stat().st_size == cloud_file.stat().st_size:
                file_obj, created = model.File.get_or_create(path=str(local_file.absolute()))
                file_obj.st_size = local_file.stat().st_size
                file_obj.st_ctime = datetime.datetime.fromtimestamp(cloud_file.stat().st_ctime)
                file_obj.save()
                os.unlink(cloud_file)
                print(f"    SUCCESS: file copied to {local_file}")
            else:
                print(f"ERROR: file is different: {local_file}")
        except Exception as e:
            print(f"CRITICAL: {cloud_file}")
            print(e)
    model.db.close()


if __name__ == "__main__":
    main()