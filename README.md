# icloud_windows_sync

back up icloud file to local directory on windows system

# How did it works
since we can only get the stat info from icloud directory before download. I use the create time and size info as unique index for each file.  
* if there is data stored in the index.db, then it will recognize it as handled and delete the cloud file directly.
* otherwise it will copy the file to the backup directory and create a row in index.db
* finally, use the git lfs to find the duplicate file and only keep one 
    1. set all the sha column
    2. set the row in index.db as deleted(is_del=True)
    3. delete the local file


# Usage

1. init backup repository

```
git init backup
cd backup
```


2. install git lfs

```
git lfs install
git lfs track "*.jpg" "*.png" "*.exe" "*.JPG" "*.iso" "*.AAE" "*.mp4" "*.JPG" "*.PNG" "*.MOV"
git clone git@github.com:ramwin/icloud_windows_sync.git
pip3 install -r icloud_windows_sync/requirements.txt
```


3. init database


```
$ python
from icloud_windows_sync.model import File, db
db.create_tables([File])
```

4. download file


```
python3 icloud_windows_sync/downlowd.py
```


3. delete duplicate file


```
python icloud_windows_sync/update_sha.py
python icloud_windows_sync/delete_duplicate_file.py
# you can add your customer rule to determine which file to delete
```
