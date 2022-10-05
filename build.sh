#!/bin/bash

# install fonttools, brotli
pip3 install fonttools brotli --user
export PATH="/vercel/.local/bin/:$PATH"

# Build the project.
hugo -D # if using a theme, replace with `hugo -t <YOURTHEME>`

cd public

# install ripgrep
yum install wget
mkdir ripgrep
wget -qO- https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep-13.0.0-x86_64-unknown-linux-musl.tar.gz | tar xvzf - --strip-components 1 -C ./ripgrep
export PATH="./ripgrep/:$PATH"

pyftsubset "font/LXGWWenKaiLite-Regular.ttf" --text=$(rg -e '[\w\d]' -oN --no-filename|sort|uniq|tr -d '\n') --no-hinting
fonttools ttLib.woff2 compress -o "font/LXGW.woff2" "font/LXGWWenKaiLite-Regular.subset.ttf"

rm "font/LXGWWenKaiLite-Regular.subset.ttf"
rm -rf ripgrep