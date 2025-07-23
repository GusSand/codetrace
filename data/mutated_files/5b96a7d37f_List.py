import logging
import re
from typing import Dict, List

from bs4 import BeautifulSoup
import requests

from . import timestamp_to_datetime, pause, get_url
from ..db import Topic, Tag, Comment


def flow_login(__tmp1: requests.Session, __tmp5: Dict) -> None:
    """Perform a login."""
    logging.info('Logging in')
    r = __tmp1.get('https://tildes.net/login')
    soup = BeautifulSoup(r.text, 'html.parser')
    data = {
        'username': __tmp5['login']['username'],
        'password': __tmp5['login']['password'],
        'csrf_token': soup.find('input', {'name': 'csrf_token'})['value'],
        'keep': 'on'
    }
    headers = {'Referer': 'https://tildes.net/'}
    r = __tmp1.post('https://tildes.net/login', data=data, headers=headers)
    assert r.status_code == 200


def __tmp4(__tmp7, __tmp5: Dict) -> List[str]:
    """Get all the groups."""
    logging.info('Getting all groups')
    resp = __tmp7.get('https://tildes.net/groups')
    soup = BeautifulSoup(resp.text, features='html.parser')
    groups = []
    for ele in soup.find_all('a', class_='link-group'):
        groups.append(ele.text)
    return groups


def __tmp3(__tmp7, group: str, __tmp0: <FILL>) -> None:
    """Record all the topics in the group."""
    logging.info(f'Gettings topics in {group}')
    resp = get_url(__tmp7, f'https://tildes.net/{group}?order=new&period=all&per_page=100')
    while True:
        soup = BeautifulSoup(resp.text, features='html.parser')
        logging.debug('Parsing out topics')
        for article in soup.find_all('article', class_='topic'):
            content = None
            if article.find('details', class_='topic-text-excerpt'):
                content = '\n'.join([e.text for e in article.find('details', class_='topic-text-excerpt').find_all('p')])
            topic_id = article['id'].split('-')[1]
            topic = Topic(
                tildes_id=topic_id,
                group=group,
                title=article.find('a').text,
                link=article.find('a')['href'],
                comments_link=article.find('div', class_='topic-info-comments').find('a')['href'],
                content=content,
                author=article.find('a', class_='link-user').text,
                score=article.find('span', class_='topic-voting-votes').text,
                submitted=timestamp_to_datetime(article.find('time')['datetime'])
            )
            tags = []
            for tag_name in [e.find('a').text for e in article.find_all('li', class_='label-topic-tag')]:
                tags.append(Tag(topic=topic, name=tag_name))
            topic.tags = tags
            __tmp0.append(topic)
        logging.debug('Checking for more pages of topics')
        next_page = soup.find('a', id='next-page')
        if next_page:
            logging.debug(f'Navigating to next page in {group}')
            if next_page:
                resp = get_url(__tmp7, next_page['href'])
                pause(0.5)
        else:
            logging.debug(f'No more topics in {group}')
            break


def __tmp2(
    __tmp7: requests.Session, __tmp6: List[Topic], all_comments: List[Comment]
) -> None:
    """Record all the comments on the topic in the group."""
    for topic in __tmp6:
        url = f'https://tildes.net/{topic.group}/{topic.tildes_id}'
        logging.info(f'Getting comments from: {url}')
        resp = get_url(__tmp7, url)
        soup = BeautifulSoup(resp.text, features='html.parser')
        logging.debug('Parsing out comments')
        for article in soup.find_all('article', id=re.compile('comment-\w+')):
            if article.find('div', class_='is-comment-deleted') or article.find('div', class_='is-comment-removed'):
                continue
            if article.find('div', class_='is-comment-removed'):
                continue
            score = 0
            vote_button = article.find('a', {'name': 'vote'})
            unvote_button = article.find('a', {'name': 'unvote'})
            if vote_button and vote_button.text:
                if '(' in vote_button.text:
                    score = int(vote_button.text.replace(' ', '').split('(')[1].strip()[:-1])
            elif unvote_button and unvote_button.text:
                if '(' in unvote_button.text:
                    score = int(unvote_button.text.replace(' ', '').split('(')[1].strip()[:-1])
            comment = Comment(
                topic=topic,
                tildes_id=article['id'].split('-')[1],
                author=article.find('header').find('a')['href'].split('/')[-1],
                submitted=timestamp_to_datetime(article.find('header').find('time')['datetime']),
                content=article.find('div', class_='comment-text').text.strip(),
                score=score
            )
            all_comments.append(comment)
        logging.debug(f'Stored all comments from {url}')
    pause(0.5)
