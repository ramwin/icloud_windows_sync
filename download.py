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
from log import logger



def main(count=100000):
    for cloud_file in CLOUD_PATH.iterdir():
        logger.info(f"INFO: handling {cloud_file}")
        count -= 1
        if count % 10 == 0:
            logger.info(f"remaining: {count}, time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if count < 0:
            return
        st_ctime = datetime.datetime.fromtimestamp(cloud_file.stat().st_ctime)
        st_size = cloud_file.stat().st_size
        file_obj, created = model.File.get_or_create(st_ctime=st_ctime, st_size=st_size)
        if created is False:
            logger.info(f"File {cloud_file} handled before")
            if file_obj.path or file_obj.is_del:
                logger.info(f"local file {file_obj.path} exist")
                logger.info("delete remote file")
                os.unlink(cloud_file)
            else:
                logger.info(f"this file should be rehandle")
                file_obj.delete_instance()
            continue
        directory = BACK_PATH.joinpath(str(st_ctime.year)).joinpath(str(st_ctime.month))
        if not directory.exists():
            os.makedirs(directory)
        local_file = directory.joinpath(cloud_file.name)
        if (not local_file.exists()) or local_file.stat().st_size == 0:
            shutil.copy2(cloud_file, local_file)
        else:
            logger.info(f"luck, file exist")
        if local_file.stat().st_size == cloud_file.stat().st_size:
            if model.File.filter(path=str(local_file.absolute())).exists():
                file_obj_new = model.File.get(path=str(local_file.absolute()))
                file_obj_new.st_ctime = file_obj.st_ctime
                file_obj_new.save()
                file_obj.delete_instance()
            else:
                file_obj.st_size = local_file.stat().st_size
                file_obj.path = local_file.absolute()
                file_obj.save()
            os.unlink(cloud_file)
            logger.info(f"file copied to {local_file}")
        else:
            logger.error((
                f"file is differenc\n"
                f"    local_file vs cloud_file\n"
                f"    path {local_file} vs {cloud_file}\n"
                f"    size {local_file.stat().st_size} vs {cloud_file.stat().st_size}\n"
            ))
            continue
    model.db.close()


if __name__ == "__main__":
    main()
