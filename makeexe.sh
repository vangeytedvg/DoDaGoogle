echo "*** Create Executable ***"
pyinstaller -y -w -i app.ico dodagoogle.py \
--hidden-import='email.mime.multipart' \
--hidden-import='email.mime.message' \
--hidden-import='email.mime.text' \
--hidden-import='email.mime.image' \
--hidden-import='email.mime.audio' \
--hidden-import='json' \
--hidden-import='httplib2' \
--hidden-import='uritemplate' \
--hidden-import='discovery' \
--hidden-import='uuid' \
--hidden-import='pkg_resources' \
--hidden-import='wsgiref.simple_server' \
--hidden-import='requests' \
--hidden-import='cachetools'

echo "Copying resources to dist folder"
cp app.ico ./dist/main
cp ./gui/*.qrc ./dist/main
echo "[*] Done"