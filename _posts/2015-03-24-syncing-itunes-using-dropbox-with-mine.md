---
layout: post
title: Syncing iTunes using Dropbox with Mine
tags:
- mine
- dropbox
- itunes
- python
---

Many applications provide their own synchronization methods to enable usage on multiple computers, but what about those that don't? It turns out that lots of programs are perfectly happy to have their files stored inside Dropbox rather than their typical location.

## Storing iTunes in Dropbox

Many guides exist showing you how to do this with iTunes:

* [digiwonk.wonderhowto.com/how-to/sync-your-itunes-library-with-several-computers-using-dropbox](http://digiwonk.wonderhowto.com/how-to/sync-your-itunes-library-with-several-computers-using-dropbox-0155955)
* [lifehacker.com/5715126/how-to-sync-itunes-across-all-your-computers-with-dropbox](http://lifehacker.com/5715126/how-to-sync-itunes-across-all-your-computers-with-dropbox)
* [cloudproductivity.net/automatically-backup-itunes-dropbox](http://www.cloudproductivity.net/automatically-backup-itunes-dropbox)

Unfortunately, the shared caveat in all these guides is that only one instance of iTunes is to be running at any given time. That's where `mine` comes in.

## Installing and Configuring Mine

`mine` is a daemon and command-line [Python program](https://github.com/jacebrowning/mine) that starts and stops remote applications using a configuration file in Dropbox. After setting up iTunes and Dropbox using one of the above guides, install `mine`:

```
$ pip3 install --upgrade mine
```

If you don't have `pip3`, install `python3` with your system's package manager (on OSX with [Homebrew](http://brew.sh/): `$ brew install python3`).

Additional configuration instructions are found in the project's [README](https://github.com/jacebrowning/mine#setup).

## Using Mine to Manage Remote Applications

Once installed and configured, let it run in the background on each computer:

```
$ mine --daemon
```

Applications can be killed remotely and started on the current computer:

```
$ mine switch
```

To kill all local applications and start them on another computer:

```
$ mine switch <name>
```

where `<name>` is part of the name of another computer with `mine` running.

To leave `mine` running in the background:

-----

Find a problem? Please submit an [issue](https://github.com/jacebrowning/mine/issues) or contribute!



