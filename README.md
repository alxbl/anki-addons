Anki Addons
===========

A collection of addons for Anki that I found solved some practical problems
that I stumbled across while studying.


Installing
==========

Installing the addons is as easy as cloning the repository over your Anki
addon folder.

It gets a tiny bit more involved if you have existing addons. Assuming that
the environment variable `ANKI_ADDON_PATH` is defined, the snippets below
give a generic overview of how to install these addons.

```
	git clone git@github.com:alxbl/anki-addons.git $ANKI_ADDON_PATH/addons
```

If this fails with a message `fatal: destination path 'addons' already exists 
and is not an empty directory.`, then it is possible to merge the previous
addons along with the ones contained in this repository as follows:

```
	git clone git@github.com:alxbl/anki-addons.git $ANKI_ADDON_PATH/addons/anki-addons \
	&& mv $ANKI_ADDON_PATH/addons/anki-addons/{*,.git} $ANKI_ADDON_PATH/addons/ \
	&& rm -rf $ANKI_ADDON_PATH/addons/anki-addons
```

Addons
======

alc.py
------

`alc` adds a UI window that allows to search for words using `alc.co.jp` as a dictionary.
It will directly convert the selected example sentences into flash cards in the specified
deck.