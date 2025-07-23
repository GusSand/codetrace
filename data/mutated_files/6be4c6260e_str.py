from typing import TypeAlias
__typ3 : TypeAlias = "Artist"
__typ2 : TypeAlias = "int"
__typ0 : TypeAlias = "Venue"

import datetime

from utils.songkick_api.sk_venue import Venue
from utils.songkick_api.sk_artist import Artist


class __typ1(object):

    def __tmp2(

            __tmp1,
            sk_id:     __typ2,
            date,
            artist,
            artist_id: __typ2,
            venue:     __typ0,
            venue_id:  __typ2,
            city:      <FILL>,
            state):

            __tmp1.sk_id = sk_id
            __tmp1.date = date
            __tmp1.artist = artist
            __tmp1.artist_id = artist_id
            __tmp1.venue = venue
            __tmp1.venue_id = venue_id
            __tmp1.city = city
            __tmp1.state = state

    def __tmp3(__tmp1):

        return "      \n" \
           "ID: {}    \n" \
           "Date: {}  \n" \
           "Artist: {}\n" \
           "Venue: {} \n".format(

            str(__tmp1.sk_id),
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
