from logging import Logger

from utils.songkick_api.sk_artist import Artist
from utils.songkick_api.sk_event import Event
from utils.songkick_api.sk_venue import Venue
log = Logger


def build_venue(__tmp2: dict, __tmp1: dict) :

    '''
    :param dict venue_data: JSON response node from API @ resultsPage.results.event.venue
    :param dict location_data: JSON response node @ resultsPage.results.event.location
    :return: If the dict holds the targeted k/v pairs (and v types are correct for Venue instantiation), a Venue object is returned, otherwise the return is a boolean 'False'
    '''

    try:
        new_venue = Venue(
            __tmp2['id'],
            __tmp2['displayName'],
            __tmp1['city'].split(',')[0],
            __tmp2['metroArea']['state']['displayName'])
        return new_venue

    except KeyError:
        log('KeyError from constructor.build_venue')
        return False

    except SyntaxError:
        log('SyntaxError from constructor.build_venue')
        return False


def __tmp4(__tmp3: <FILL>) -> Artist or False:
    '''
    :param dict artist_data: Derived from JSON response node
    :return:
    '''

    try:
        new_artist = Artist(
            __tmp3['id'],
            __tmp3['displayName'])
        return new_artist

    except KeyError:
        log('KeyError from constructor.build_artist')
        return False


def __tmp0(__tmp5: dict) -> Event or False:

    try:
        new_event = Event(
            __tmp5['id'],
            __tmp5['start']['datetime'],
            __tmp5['performance'][0]['artist']['displayName'],
            __tmp5['performance'][0]['artist']['id'],
            __tmp5['venue']['displayName'],
            __tmp5['venue']['id'],
            __tmp5['location']['city'].split(',')[0],
            __tmp5['venue']['metroArea']['state']['displayName'])

        return new_event

    except KeyError:
        log('KeyError from build_event()')
        return False

    except IndexError:
        log('IndexError from build_event()')
        return False

