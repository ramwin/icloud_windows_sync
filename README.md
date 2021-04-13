# icloud_windows_sync

back up icloud file to local directory on windows system

# Usage

1. init backup repository


    git init backup


2. install git lfs

    
    git lfs install
    git lfs track "*.jpg" "*.png" "*.exe" "*.JPG" "*.iso" "*.AAE" "*.mp4" "*.JPG" "*.PNG" "*.MOV"
    git clone git@github.com:ramwin/icloud_windows_sync.git


3. init database


    python
    >>> from icloud_windows_sync.model import File, db
    db.create_tables([File])


4. download file


    python3 icloud_windows_sync/downlowd.py


3. delete duplicate file


    python icloud_windows_sync/delete_duplicate_file.py


4. 
