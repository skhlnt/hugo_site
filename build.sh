#!/bin/bash

# install fonttools, brotli
pip3 install fonttools brotli --user
export PATH="/vercel/.local/bin/:$PATH"

# Build the project.
hugo -D # if using a theme, replace with `hugo -t <YOURTHEME>`

cd public

# install ripgrep
# yum install wget
# mkdir ripgrep
# wget -qO- https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep-13.0.0-x86_64-unknown-linux-musl.tar.gz | \
#    tar xvzf - --strip-components 1 -C ./ripgrep
export PATH="../ripgrep/:$PATH"

origin='LXGWWenKaiLite-Regular.ttf' # 原始字体名称
optimized='LXGW.woff2' # 压缩后的字体名称，注意需要和 font-face 中定义的字体名一致
pyftsubset "font/$origin" --text=$(rg -e '[\w\d]' -oN --no-filename|sort|uniq|tr -d '\n') --no-hinting
fonttools ttLib.woff2 compress -o "font/$optimized" "font/${origin/\./\.subset\.}"

rm "font/${origin/\./\.subset\.}"