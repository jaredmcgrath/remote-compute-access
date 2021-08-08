#!/bin/bash

grub_item=0

# Get env vars
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -i|--item)
    grub_item=$2
    shift # Past argument
    shift # Past value
    ;;
    *) # unknown
    POSITIONAL+=("$1") # Save in array
    shift # past argument
    ;;
esac
done

# Retore positional
set -- "${POSITIONAL[@]}"

echo "Will reboot with GRUB item $grub_item"
echo "(this is a 0-based index)"

sudo grub-reboot $grub_item
sudo reboot
