Musicbrainz + Echoprint submitter and renamer
=============================================

These tools help you submit echoprint fingerprints to the Musicbrainz NGS system.

For more information on echoprint see http://blog.echonest.com/post/6824753703/announcing-echoprint

To set up
----------

 * Download echoprint-codegen, compile it, and put the resulting binary in this directory
 * put your echonest api key and musicbrainz login in conf.py (rename conf.py.dist)

Submitting Echoprints
---------------------

Musibrainz contains a mapping between its recordings and an echoprint id. For example, look at
http://echoprint.musicbrainz.org/recording/a4d7cb45-2f1e-48d9-b57a-f287ab083bb2/echoprints

If you have renamed your music collection with Picard or another tool that adds the MUSICBRAINZ_TRACKID
tag to files then you can help to populate this mapping.

Use the submit_echoprints.py script on one or more directories:

    $ python submit_echoprints.py ~/Music/some-album

Some caveats:

 * The echoprint database is currently quite small, so you might not get a match for everything. You cannot submit unknown fingerprints to echoprint yet
 * Don't use your regular password when submitting to musicbrainz. As it is a development server, all passwords have been reset to 'mb'

Identifying albums
------------------

To come... Code needs to be converted to musicbrainz NGS
