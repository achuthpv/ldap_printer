#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEST="/usr/local/ldap_printer"

sudo apt-get update
sudo apt-get install python-dev python-pip libcups2-dev cups libcups2 firefox

sudo rm -rf ${DEST}

echo "Copying project to ${DEST}"
sudo cp -rf ${DIR} ${DEST}

echo "Generating wrapper file..."
sudo python ${DEST}/generate_wrapper.py

echo "Compiling wrapper file..."
sudo g++ ${DEST}/generated_wrapper.cpp -o ${DEST}/ldap_print

echo "Deleting wrapper file..."
sudo rm -rf ${DEST}/generated_wrapper.cpp

echo "Setting appropriate permissions..."
sudo chown root:root -R ${DEST}
sudo find ${DEST} -type d -exec chmod 755 {} \;
sudo find ${DEST} -type f -exec chmod 600 {} \;
sudo chmod 755 ${DEST}
sudo chmod 4711 ${DEST}/ldap_print

#installing required dependecies
sudo pip install -r ${DEST}/requirements.txt

#to prevent the update of cups files
echo "libcups2-dev hold" | sudo dpkg --set-selections
echo "libcups2 hold" | sudo dpkg --set-selections
echo "cups hold" | sudo dpkg --set-selections


echo "Adding command to PATH"
sudo touch /etc/profile.d/ldap_printer.sh # Adding to PATH
echo "export PATH=${DEST}:\${PATH}" | sudo tee /etc/profile.d/ldap_printer.sh > /dev/null
source /etc/profile

echo "Installtion Completed"
