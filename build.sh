#!/bin/bash

# Build the project.
hugo -D # if using a theme, replace with `hugo -t <YOURTHEME>`

# Go To Public folder
cd public

origin='LXGWWenKaiLite-Regular.ttf' # 原始字体名称
optimized='LXGW.woff2' # 压缩后的字体名称，注意需要和 font-face 中定义的字体名一致

pyftsubset "font/$origin" --text=$(rg -e '[\w\d]' -oN --no-filename|sort|uniq|tr -d '\n') --no-hinting
fonttools ttLib.woff2 compress -o "font/$optimized" "font/${origin/\./\.subset\.}"
rm "font/${origin/\./\.subset\.}"