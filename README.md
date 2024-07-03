## Dependencies
+ [hugo](https://gohugo.io/): One of the most popular open-source static site generators.
  ```shell
  scoop install hugo-extended # Windows
  ```
+ [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod): A clean Hugo theme.

## Build
```shell
# Clone this repository and initialize all contained submodules
git clone git@github.com:Kenshin2438/kenshin2438.top.git blog --recursive
# Launch a web server for your Hugo site (default hostname = localhost:1313)
cd blog && hugo server -D

# [optional] git submodule update --remote --merge
```

## Usage
Create a new post. (*Pay attention to formate the filename*)
```shell
hugo new 'posts/{year}/{date} - {filename}.md'
```
