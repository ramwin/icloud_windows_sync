# icloud_windows_sync

back up icloud file to local directory on windows system

# Usage

1. init backup repository


    git init backup


2. install git lfs

    
    git lfs install
    git lfs track "*.jpg" "*.png" "*.exe" "*.JPG" "*.iso" "*.AAE" "*.mp4" "*.JPG" "*.PNG" "*.MOV"
    git clone git@github.com:ramwin/icloud_windows_sync.git
    python3 icloud_windows_sync/downlowd.py


3. delete duplicate file


    git lfs ls-files -l > tmp.csv
    python icloud_windows_sync/delete_duplicate_file.py
