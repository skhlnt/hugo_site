## Dependencies
+ [hugo](https://gohugo.io/): One of the most popular open-source static site generators.
  ```shell
  scoop install hugo # Windows
  ```
+ [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod): A clean Hugo theme.

## Build
```shell
# Clone this repository and initialize all contained submodules
git clone git@github.com:Kenshin2438/kenshin2438.top.git --recursive
# Launch a web server for your Hugo site (default hostname = localhost:1313)
cd kenshin2438.top && hugo server -D
```

## Usage
Create a new post. (*Pay attention to formatting the filename*)
```shell
hugo new 'posts/{year}/{date} - {filename}.md'
```
