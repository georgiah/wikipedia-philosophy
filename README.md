# Getting to philosophy

## Introduction

> Clicking on the first link in the main text of a Wikipedia article, and then repeating the process for subsequent articles, would usually lead to the Philosophy article.

As described in [Wikipedia: Getting to Philosophy](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy), most (97% as of February 2016) Wikipedia articles lead back to the article for Philosophy by clicking the first link the main text. The first link in the main text is classified by:

- Ignore external links, links to the current page, or red links
- The first remaining link that is non-parenthesized and non-italicized

This repository is an amateur attempt to play the _Philosophy Game_. Written in `Python`, it generates a random Wikipedia article, then follows the first links until it reaches Philosophy, enters an infinite loop, or reaches an article without any valid links. You can see a demonstration of the program below:

![demonstration](assets/philosophy.gif)

It operates by fetching the content of the article's URL and parsing the returned data. As part of the parsing process, it strips any parenthesized content that is not containing in an `<a>` tag, then checking each remaining link that is not contained within a number of specific classes which signify that the link is outside the main text. It also ignores image files, and strips URLs of section tags.

The code stores visited articles and their corresponding first links in a dictionary, speeding up the game once an article is reached that it has seen before. The more often the game is played, the more knowledgable and faster it becomes.

The tradeoff involved is that if a Wikipedia article is updated, it won't be checked again to validate and update the first link. See the **TODO** section for further details.

A list of articles that do **not** lead back to Philosophy can be found [here](https://georgiah.github.io/wikipedia-philosophy)

## Installation

The `Python` code in this repository was developed using `Python 2.7.10`, which comes preinstalled on `Mac OS X 10.8^`. You can check if you have `Python` installed on your computer by running the command:

```
python --version
```

If you don't have `Python`, it can be downloaded [here](https://www.python.org/downloads/).

This project also makes use of an external library, `BeautifulSoup`. Information for installing `BeautifulSoup` can be found [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).

After cloning the repository, navigate to its folder, and start the program by running:

```
python philowiki.py
```

The first time this is run, it will create another file called `wikidict.p`. This is where the dictionary of visited articles is saved.

## TODO

- [ ] more comprehensive testing that link selected is from the main body of the article
- [ ] maintain a list of articles that do _not_ lead back to Philosophy, which is automatically published a website
- [ ] allow an option command line input to specify the initial article
- [ ] upload program to a server to continuously run and improve the dictionary
- [ ] periodically check the validity of articles and their first links stored in the dictionary

## License
MIT
