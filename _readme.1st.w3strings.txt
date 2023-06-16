Introduction
-------------

This package contains a commandline w3strings decoder / encoder for adding new
strings as standalone w3string files to mods.

The input files have to be saved as "UTF8 without BOM". It should work with all
UTF-8 characters. Do NOT use excel to edit the csv files as it changes the format
on saving the file. Instead use wordpad or notepad++.

Important:

To prevent multiple mods from using the same string ids the usable ids are
restricted for every file (1000 ids per file allowed). Upon encoding you have to
provide an id-space, follow the example to see how it works. I suggest you use
your nexusmod mod id for this.

These tools are distributed in the hope that they will be useful - but WITHOUT
ANY WARRANTY.

Features

- decodes w3strings to csv file
- creates a standalone w3strings file from a csv file with localized strings (new
  ids and string keys) for your mod
- generates a ws script file to test the strings are accessible in the game

The encoder is compiled for 64bit windows. Start with --help to see all options.


More details can be found here: http://forums.cdprojektred.com/threads/62747-Utility-Strings-encoder-for-adding-new-strings-(new-ids-and-keys)-as-standalone-w3strings-file
