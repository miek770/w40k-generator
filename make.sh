#!/usr/bin/bash

# Get project title and version from main.py
TITLE=$(grep -n "__title__ = " main.py | tr '"' '\n' | sed '2q;d' | tr ' ' '_')
VERSION=$(grep -n "__version__ = " main.py | tr '"' '\n' | sed '2q;d' | tr ' ' '_')

# Remove previous distribution
rm -rf main.dist
rm -rf "$TITLE-$VERSION"
rm -rf "$TITLE-win32-$PROCESSOR_ARCHITECTURE-$VERSION.zip"

# Compile using Nuitka
python -m nuitka --standalone --plugin-enable=numpy --mingw64 --assume-yes-for-downloads --remove-output --windows-disable-console main.py

# Rename and compress release
sleep 5
cp -r codices main.dist
cp -r configs main.dist
mv main.dist/main.exe "main.dist/$TITLE-$VERSION.exe"
sleep 1
mv main.dist "$TITLE-$VERSION"
sleep 1
zip -r "$TITLE-win32-$PROCESSOR_ARCHITECTURE-$VERSION.zip" "$TITLE-$VERSION"
