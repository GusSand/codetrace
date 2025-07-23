from typing import TypeAlias
__typ0 : TypeAlias = "int"

import datetime

from utils.songkick_api.sk_venue import Venue
from utils.songkick_api.sk_artist import Artist


class Event(object):

    def __init__(

            self,
            sk_id:     __typ0,
            date:      datetime.date,
            artist,
            artist_id,
            venue:     Venue,
            venue_id,
            city,
            state:     <FILL>):

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

            str(self.sk_id),
            self.date,
            self.artist.displayName,
            self.venue.displayName)

    def __tmp0(self):

        return {
            'sk_id':     self.sk_id,
            'date':      self.date,
            'artist':    self.artist,
            'artist_id': self.artist_id,
            'venue':     self.venue,
            'venue_id':  self.venue_id,
            'city':      self.city,
            'state':     self.state}
