#!/bin/bash
#
# Automatically removes files of emage python bindings. Show and asks the files
# to remove before actually doing the real operation.

echo "Files to be removed:"
cat ./install.log
read -r -p "Do you want to remove such files? " -n 1
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
        echo "Removing files..."
        cat ./install.log | xargs rm -rf
else
        echo "Interrupted!"
fi