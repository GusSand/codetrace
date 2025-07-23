from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "Artist"
__typ0 : TypeAlias = "Venue"

import datetime

from utils.songkick_api.sk_venue import Venue
from utils.songkick_api.sk_artist import Artist


class __typ3(object):

    def __init__(

            self,
            sk_id:     <FILL>,
            date,
            artist,
            artist_id,
            venue,
            venue_id,
            city,
            state):

            self.sk_id = sk_id
            self.date = date
            self.artist = artist
            self.artist_id = artist_id
            self.venue = venue
            self.venue_id = venue_id
            self.city = city
            self.state = state

    def __str__(self):

        return "      \n" \
           "ID: {}    \n" \
           "Date: {}  \n" \
           "Artist: {}\n" \
           "Venue: {} \n".format(

            __typ2(self.sk_id),
            self.date,
            self.artist.displayName,
            self.venue.displayName)

    def __dict__(self):

        return {
            'sk_id':     self.sk_id,
            'date':      self.date,
            'artist':    self.artist,
            'artist_id': self.artist_id,
            'venue':     self.venue,
            'venue_id':  self.venue_id,
            'city':      self.city,
            'state':     self.state}
