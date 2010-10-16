Echo Nest album identifier
==========================

A tool to identify an album based on the Echo Nest fingerprint system.

What it does
------------

 1. Uses the Echo Nest music fingerprint API to guess what artist and track name this file is
 2. Matches track listings to releases on musicbrainz
 3. Identifies releases on musicbrainz that have the same number of tracks as we have files

To set up
----------

 * install ffmpeg
 * compile http://github.com/alastair/enmfp-boost-python and put in here
 * put your echonest api key in echonestconf.py
 * make sure you have an up-to-date version of python-musicbrainz2 (0.7.2).  http://packages.ubuntu.com/python-musicbrainz2 or ftp://ftp.musicbrainz.org/pub/musicbrainz/python-musicbrainz2/

To run
------
    ./identify <directory>


Demo
----
Here's an example of the identifier running on an unknown album.

    alastair@cage:~/Projects/echonest-albumidentify$ ./identify album/
    decoding album/11.mp3 ...
    decoding album/2.mp3 ...
    decoding album/9.mp3 ...
    decoding album/song.mp3 ...
    decoding album/what.mp3 ...
    decoding album/12.mp3 ...
    decoding album/6.mp3 ...
    decoding album/unknown.mp3 ...
    decoding album/five.mp3 ...
    decoding album/8.mp3 ...
    decoding album/ten.mp3 ...
    decoding album/1.mp3 ...
    Could be release: Challengers, by The New Pornographers (http://musicbrainz.org/release/fca8fd71-dd88-4a52-9bd0-deac6470ce85.html)
    1.mp3 --> 1 - The New Pornographers - My Rights Versus Yours.mp3
    2.mp3 --> 2 - The New Pornographers - All the Old Showstoppers.mp3
    song.mp3 --> 3 - The New Pornographers - Challengers.mp3
    unknown.mp3 --> 4 - The New Pornographers - Myriad Harbour.mp3
    five.mp3 --> 5 - The New Pornographers - All the Things That Go to Make Heaven and Earth.mp3
    6.mp3 --> 6 - The New Pornographers - Failsafe.mp3
    what.mp3 --> 7 - The New Pornographers - Unguided.mp3
    8.mp3 --> 8 - The New Pornographers - Entering White Cecilia.mp3
    9.mp3 --> 9 - The New Pornographers - Go Places.mp3
    ten.mp3 --> 10 - The New Pornographers - Mutiny, I Promise You.mp3
    11.mp3 --> 11 - The New Pornographers - Adventures in Solitude.mp3
    12.mp3 --> 12 - The New Pornographers - The Spirit of Giving.mp3

