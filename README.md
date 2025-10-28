# BurgerBibArkBot
Custom script for Pywikibot to change non-persistent and obsolete links to the catalogue of the Burgerbibliothek Bern to persistent versions.

## Summary
The program executes the following actions:
* Searches for occurrences of [Burgerbib Templates](https://de.wikipedia.org/wiki/Vorlage:BurgerBib) and adds the persistent version.
* Searches for occurrences of links following the schema burgerbib.scopeoais.ch/detail.aspx or katalog.burgerbib.ch/detail.aspx and replaces them with their persistent versions.
* Searches for occurrences of links following the schema archives-quickaccess.ch/bbb/person/* and replaces thme with their persistent versions.
