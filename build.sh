#!/bin/bash

# # install fonttools, brotli
pip3 install fonttools brotli --user
export PATH="/vercel/.local/bin/:$PATH"

# # install ripgrep
yum install yum-utils
yum-config-manager --add-repo=https://copr.fedorainfracloud.org/coprs/carlwgeorge/ripgrep/repo/epel-7/carlwgeorge-ripgrep-epel-7.repo
yum install ripgrep

# Build the project.
hugo -D # if using a theme, replace with `hugo -t <YOURTHEME>`

pyftsubset "public/font/LXGWWenKaiLite-Regular.ttf" --text=$(rg -e '[\w\d\p{P}]' "public/" -oN --no-filename | sort | uniq | tr -d '\n') --no-hinting --timing
fonttools ttLib.woff2 compress -o "public/font/LXGW.woff2" "public/font/LXGWWenKaiLite-Regular.subset.ttf"

rm "public/font/LXGWWenKaiLite-Regular.subset.ttf"