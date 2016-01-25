---
layout: post
title: Replacing Git Submodules with GDM
tags:
- git
- submodules
- gdm
- version-control
- python
---

Lots of languages offer dependency managers ([`pip`](https://pip.pypa.io/en/stable/), [`gem`](https://rubygems.org/), [`npm`](https://www.npmjs.com/), etc.), but in many situations, that's not enough. Sometimes you need to:

* use a language without a dependency manager
* include code from multiple languages
* explicitly control the installation location

## Git Submodules

When using [Git](https://git-scm.com/) for version control, the obvious choice is to use [submodules](http://git-scm.com/docs/git-submodule) to include the source from another repository. However, in practice, submodules can often be a pain to use, as they:

* require extra information to meaningfully identify the submodule's SHA
* cause confusing merge conflicts (one SHA vs. another)
* show confusing status changes when switching branches

And while submodules can be used to track a branch (rather than a SHA), this will:

* show confusing status changes if the branch head moves
* require a new commit by whomever updates submodules first

## An Alternative

GDM ([Git Dependency Manager](https://github.com/jacebrowning/gdm)) avoids these issues and adds the ability to:

* track a specific tag in a source dependency's repository
* checkout by `rev-parse` dates (e.g. `'develop@{2015-06-18 10:30:59}'`)

### Installation

To install GDM, first install Python 3 and it's dependency manager, `pip`:

* Windows: [python.org/downloads](https://www.python.org/downloads)
* Mac: `$ brew install python3`
* Ubuntu: `$ sudo apt-get install python3-pip`

Then, install `gdm` using `pip3`:

```bash
$ pip3 install --upgrade gdm
```

Version and help information are available on the command-line

```bash
$ gdm --version
$ gdm --help
```

### Mimicking Submodules

While GDM, provides [additional capabilities](https://github.com/jacebrowning/gdm#basic-usage), it can also directly replace the behavior of submodules. To mimic a working tree containing a submodule:

```bash
<root>/vendor/my_dependency  # submodule at: a5fe3d...
```

create a `.gdm.yml` file in the root of your working tree:

```yaml
location: .gdm
sources:
- repo: <URL of my_dependency's repository>
  dir: my_dependency
  rev: a5fe3d
  link: vendor/my_depenendy
```

and run:

```bash
$ gdm install
```

To display the specific versions of source dependencies:

```bash
$ gdm list
```

-----

See a typo? Help me [edit](https://github.com/jacebrowning/info/edit/master/{{page.path}}) this post.

Find a problem with `gdm`? Please submit an [issue](https://github.com/jacebrowning/gdm/issues) or contribute!
