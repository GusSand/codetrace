from logging import Logger

from utils.songkick_api.sk_artist import Artist
from utils.songkick_api.sk_event import Event
from utils.songkick_api.sk_venue import Venue
log = Logger


def __tmp0(venue_data: dict, location_data) -> Venue or False:

    '''
    :param dict venue_data: JSON response node from API @ resultsPage.results.event.venue
    :param dict location_data: JSON response node @ resultsPage.results.event.location
    :return: If the dict holds the targeted k/v pairs (and v types are correct for Venue instantiation), a Venue object is returned, otherwise the return is a boolean 'False'
    '''

    try:
        new_venue = Venue(
            venue_data['id'],
            venue_data['displayName'],
            location_data['city'].split(',')[0],
            venue_data['metroArea']['state']['displayName'])
        return new_venue

    except KeyError:
        log('KeyError from constructor.build_venue')
        return False

    except SyntaxError:
        log('SyntaxError from constructor.build_venue')
        return False


def build_artist(artist_data) -> Artist or False:
    '''
    :param dict artist_data: Derived from JSON response node
    :return:
    '''

    try:
        new_artist = Artist(
            artist_data['id'],
            artist_data['displayName'])
        return new_artist

    except KeyError:
        log('KeyError from constructor.build_artist')
        return False


def build_event(event_data: <FILL>) -> Event or False:

    try:
        new_event = Event(
            event_data['id'],
            event_data['start']['datetime'],
            event_data['performance'][0]['artist']['displayName'],
            event_data['performance'][0]['artist']['id'],
            event_data['venue']['displayName'],
            event_data['venue']['id'],
            event_data['location']['city'].split(',')[0],
            event_data['venue']['metroArea']['state']['displayName'])

        return new_event

    except KeyError:
        log('KeyError from build_event()')
        return False

    except IndexError:
        log('IndexError from build_event()')
        return False

