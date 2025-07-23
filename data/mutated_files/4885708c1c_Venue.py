from typing import TypeAlias
__typ1 : TypeAlias = "Artist"
__typ2 : TypeAlias = "int"
__typ0 : TypeAlias = "str"

import datetime

from utils.songkick_api.sk_venue import Venue
from utils.songkick_api.sk_artist import Artist


class __typ3(object):

    def __init__(

            __tmp1,
            sk_id:     __typ2,
            date,
            artist:    __typ1,
            artist_id,
            venue:     <FILL>,
            venue_id,
            city,
            state):

            __tmp1.sk_id = sk_id
            __tmp1.date = date
            __tmp1.artist = artist
            __tmp1.artist_id = artist_id
            __tmp1.venue = venue
            __tmp1.venue_id = venue_id
            __tmp1.city = city
            __tmp1.state = state

    def __str__(__tmp1):

        return "      \n" \
           "ID: {}    \n" \
           "Date: {}  \n" \
           "Artist: {}\n" \
           "Venue: {} \n".format(

            __typ0(__tmp1.sk_id),
            __tmp1.date,
            __tmp1.artist.displayName,
            __tmp1.venue.displayName)

    def __tmp0(__tmp1):

        return {
            'sk_id':     __tmp1.sk_id,
            'date':      __tmp1.date,
            'artist':    __tmp1.artist,
            'artist_id': __tmp1.artist_id,
            'venue':     __tmp1.venue,
            'venue_id':  __tmp1.venue_id,
            'city':      __tmp1.city,
            'state':     __tmp1.state}
