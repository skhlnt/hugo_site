---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
slug: {{ substr (md5 (printf "%s%s" .Date (replace .TranslationBaseName "-" " " | title))) 4 8 }}
author: "miralem"

summary: ""
description: ""
tags: 
  - 

weight: false
math: true
comments: true
ShowToc: true
TocOpen: true
---
