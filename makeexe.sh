echo "*** Create Executable ***"
pyinstaller -y -w dodagoogle.py

echo "Copying resources to dist folder"
cp app.ico ./dist/main
cp ./gui/*.qrc ./dist/main
echo "[*] Done"