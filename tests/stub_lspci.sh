#! /bin/bash

# Last argument is the PCI address: `lspci -vmm -s 0000:3b:00.1`
bus="${@: -1}"
cat "$(dirname $0)/fixtures/lspci_${bus//[:.]/_}"
