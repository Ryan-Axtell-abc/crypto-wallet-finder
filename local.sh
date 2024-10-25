#!/usr/bin/bash
echo "Uninstalling"
sudo rm -rf /usr/lib/python3.10/site-packages/cryptosniffer
sudo rm -rf /usr/share/cryptosniffer/
sudo rm /usr/bin/cryptosniffer 
echo "Rebuilding"
rm -rf _build/
meson --prefix /usr _build && cd _build
meson compile
echo "Installing"
sudo meson install
cd ..
sudo chown jaro:jaro /usr/bin/cryptosniffer
chmod +x /usr/bin/cryptosniffer
sudo -u jaro
/usr/bin/cryptosniffer