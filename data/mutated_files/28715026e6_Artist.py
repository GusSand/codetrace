from typing import TypeAlias
__typ2 : TypeAlias = "int"
__typ0 : TypeAlias = "str"
__typ3 : TypeAlias = "Venue"

import datetime

from utils.songkick_api.sk_venue import Venue
from utils.songkick_api.sk_artist import Artist


class __typ1(object):

    def __tmp1(

            __tmp0,
            sk_id,
            date,
            artist:    <FILL>,
            artist_id,
            venue,
            venue_id,
            city,
            state):

            __tmp0.sk_id = sk_id
            __tmp0.date = date
            __tmp0.artist = artist
            __tmp0.artist_id = artist_id
            __tmp0.venue = venue
            __tmp0.venue_id = venue_id
            __tmp0.city = city
            __tmp0.state = state

    def __str__(__tmp0):

        return "      \n" \
           "ID: {}    \n" \
           "Date: {}  \n" \
           "Artist: {}\n" \
           "Venue: {} \n".format(

            __typ0(__tmp0.sk_id),
            __tmp0.date,
            __tmp0.artist.displayName,
            __tmp0.venue.displayName)

    def __dict__(__tmp0):

        return {
            'sk_id':     __tmp0.sk_id,
            'date':      __tmp0.date,
            'artist':    __tmp0.artist,
            'artist_id': __tmp0.artist_id,
            'venue':     __tmp0.venue,
            'venue_id':  __tmp0.venue_id,
            'city':      __tmp0.city,
            'state':     __tmp0.state}
