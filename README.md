banking-scripts
===============

Scripts to help me track my personal finances, mostly CSV mangling.

For some time I've been doing this with [a bit of emacs-lisp]
(https://github.com/hillwithsmallfields/JCGS-emacs/blob/master/special-setups/finances/financial-emacs.el)
and manual work in gnumeric.  As I switch to another [finance tracking
app] (http://financisto.com/) as part of my increasing adoption of
Android, I think it's time to script it some more.

Aims
----

The scripts in here should eventually pick up files dumped by
Financisto via Dropbox, and files saved from my bank's online banking
facility, merge them both into the format I've been using for a few
years, and reconcile my spending records and my bank statements.

Design
------

I'll use Python, as I know it has reasonable CSV support.
