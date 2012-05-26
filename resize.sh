#!/bin/sh

set +x

SIZE=400x400

rm -rf static/
mkdir static/
cp like.png static/
ls -1 pictures | xargs -n1 -I{} convert -resize $SIZE pictures/{} static/{}
