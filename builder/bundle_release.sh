wine pyinstaller win.spec --clean -y
pyinstaller posix.spec --clean -y

cd dist

7z a ImagesManip-$0-posix.zip posix
7z a ImagesManip-$0-win.zip win
