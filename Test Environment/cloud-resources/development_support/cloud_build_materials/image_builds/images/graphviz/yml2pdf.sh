#!/bin/bash -e
YML2GV=/usr/local/bin/yml2gv.py
YMLFILE=$1
GVFILE=$1.gv
PDFFILE=$2

$YML2GV --input="$YMLFILE" --output="$GVFILE"
dot -Tpdf "$GVFILE" -o "$PDFFILE"
unlink "$GVFILE"
