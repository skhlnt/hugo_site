---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
slug: {{ substr (md5 (printf "%s%s" .Date (replace .TranslationBaseName "-" " " | title))) 4 8 }}
author: "Kenshin2438"

summary: ""
description: ""
keywords: 
  - 
categories: 
  - 
tags: 
  - 

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

