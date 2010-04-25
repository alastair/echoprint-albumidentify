Echo Nest album identifier
==========================

A tool to identify an album based on the Echo Nest fingerprint system.

What it does
------------

 1. Uses the Echo Nest music fingerprint API to guess what artist and release a file belongs to
 2. Counts the number of files that match a particular (artist, release) pair
 3. Get musicbrainz data for this artist (thanks, project rosetta stone)
 4. Search musicbrainz for likely release candidates and print them out

To set up
----------

 * install ffmpeg
 * compile http://github.com/alastair/enmfp-boost-python and dump in here
 * put your echonest api key in echonestconf.py
 * make sure you have an up-to-date version of python-musicbrainz2 (0.7.2).  http://packages.ubuntu.com/python-musicbrainz2 or ftp://ftp.musicbrainz.org/pub/musicbrainz/python-musicbrainz2/

To run
------
    ./identify <directory>

the python bindings for the EN code generator can sometimes be a bit temperamental.  If you get scary malloc errors, try and
run it again.  It worked for me!

Demo
----
Here's an example of the identifier running on a test album, then looking up matches in musicbrainz.

    git alastair@dvorak:~/Projects/echonest-albumidentify$ ./identify test/
    decoding test/01 - Pink Floyd - Speak to Me - Breathe.mp3 ...
    num samples 441206
    num codes 72
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/08 - Pink Floyd - Brain Damage.mp3 ...
    num samples 441206
    num codes 132
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/07 - Pink Floyd - Any Colour You Like.mp3 ...
    num samples 441206
    num codes 118
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/02 - Pink Floyd - On the Run.mp3 ...
    num samples 441206
    num codes 170
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/04 - Pink Floyd - The Great Gig in the Sky.mp3 ...
    num samples 441206
    num codes 56
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/06 - Pink Floyd - Us and Them.mp3 ...
    num samples 441206
    num codes 100
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/09 - Pink Floyd - Eclipse.mp3 ...
    num samples 441206
    num codes 114
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/05 - Pink Floyd - Money.mp3 ...
    num samples 441206
    num codes 136
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    decoding test/03 - Pink Floyd - Time.mp3 ...
    num samples 441206
    num codes 160
    opening url http://beta.developer.echonest.com/api/alpha_identify_song?api_key=<mykey>&match_type=enmfp&format=json
    {
        "ARYW4BX1187B98DDE8": {
            "name": "Gomez", 
            "releases": {
                "Machismo [EP]": 1
            }
        }, 
        "ARD4C1I1187FB4B0C3": {
            "name": "Pink Floyd", 
            "releases": {
                "Dark Side Of The Moon": 10, 
                "The Dark Side Of The Moon": 7
            }
        }
    }
    Considering artist ARYW4BX1187B98DDE8 (Gomez)
        Machismo [EP]
        probability: 11%
    Considering artist ARD4C1I1187FB4B0C3 (Pink Floyd)
        Dark Side Of The Moon
        probability: 111%
          I think it could be this one.  Here are some musicbrainz releases
          * http://musicbrainz.org/release-group/9786eb08-ad65-33ed-b0bd-42d711615360.html
          * http://musicbrainz.org/release-group/3ec8adf5-ced6-3ae0-ba7e-a8b5d96a9f50.html
          * http://musicbrainz.org/release-group/16bfdd8b-0b00-317d-bee6-357c308f7085.html
          * http://musicbrainz.org/release-group/6cadcf33-98b6-3da1-b274-e3655bfb4361.html
        The Dark Side Of The Moon
        probability: 77%
          I think it could be this one.  Here are some musicbrainz releases
          * http://musicbrainz.org/release-group/9786eb08-ad65-33ed-b0bd-42d711615360.html
          * http://musicbrainz.org/release-group/3ec8adf5-ced6-3ae0-ba7e-a8b5d96a9f50.html
          * http://musicbrainz.org/release-group/16bfdd8b-0b00-317d-bee6-357c308f7085.html
          * http://musicbrainz.org/release-group/6cadcf33-98b6-3da1-b274-e3655bfb4361.html
    
