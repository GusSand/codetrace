import datetime
from typing import Dict, Union

from flask import Blueprint, render_template
from models import ContestType, Contest, ContestDetail, TestPiece

CONTEST_MOD = Blueprint('contest_mod', __name__)


@CONTEST_MOD.route('/moe/')
def all_contests_moe() :
    from sqlalchemy import func
    from database import get_db_session
    db_session = get_db_session()

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '比賽'},
        {'name': '學生音樂比賽'}
    ]

    contests = db_session.query(ContestType, func.count(Contest.id)).outerjoin(Contest).group_by(ContestType.id).filter((ContestType.parent_id == 1) | (ContestType.id == 1))

    search_fields = ['contest-location']
    search_hint = '比賽名稱'
    return render_template(
        'contest-moe-list.html',
        search_fields=search_fields,
        search_hint=search_hint,
        ascending=True,
        contests=contests,
        breadcrumb=breadcrumb)


@CONTEST_MOD.route('/moe/<contest_type_id>')
def all_contests_moe_location(contest_type_id) :
    contest_info = ContestType.query.filter_by(id=contest_type_id).first()

    contest_info.contests = Contest.query.filter_by(contest_type_id=contest_info.id).group_by(Contest.area_id, Contest.category, Contest.band_type).all()

    for contest in contest_info.contests:
        contest.champion = ContestDetail.query.join(Contest).join(ContestType).filter(ContestType.id == contest_info.id, Contest.area_id == contest.area_id, Contest.band_type == contest.band_type, ContestDetail.position == 1).order_by(Contest.date.desc()).first()

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '比賽'},
        {'path': '/contest/moe/', 'name': '學生音樂比賽'},
        {'name': contest_info.name}
    ]

    meta: Dict[str, Union[bool, str]] = dict()
    meta['has_area'] = True
    meta['has_category'] = True
    meta['contest_id'] = 'moe'

    search_fields = ['contest-group', 'contest-area']
    shortcut_options = ['北區', '東區', '西區', '南區', '高中', '國中', '國小']
    search_hint = '地域 / 組別'
    return render_template(
        'contest-group-list.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        contest=contest_info,
        meta=meta)


@CONTEST_MOD.route('/moe/<contest_type_id>/<area_id>/<band_type>/<category>')
def __tmp0(contest_type_id, area_id, band_type: <FILL>, category) :
    contests = Contest.query.filter_by(contest_type_id=contest_type_id, area_id=area_id, band_type=band_type, category=category).all()

    for contest in contests:
        contest.year = contest.date.strftime('%Y')
        contest.test_pieces = TestPiece.query.filter(TestPiece.contests.any(id=contest.id)).all()

        champion_record = ContestDetail.query.filter_by(contest_id=contest.id, position=1).first()
        contest.champion = champion_record.band.name if champion_record else ''

        contest.url = '/contest/moe/{}/{}/{}/{}/{}'.format(contest_type_id, area_id, band_type, category, contest.year)

    # XXX: at least one band is required
    contest_name = contests[0].get_fullname(prefix=False, area=False, category=False, band_type=False)
    contest_area = contests[0].get_fullname(prefix=False, ctype=False)

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '比賽'},
        {'path': '/contest/moe/', 'name': '學生音樂比賽'},
        {'path': '/contest/moe/{}'.format(contest_type_id), 'name': contest_name},
        {'name': contest_area}
    ]

    search_hint = ''
    return render_template(
        'contest-history.html',
        search_hint=search_hint,
        ascending=False,
        breadcrumb=breadcrumb,
        contests=contests,
        contest_name=contest_name,
        contest_area=contest_area)


@CONTEST_MOD.route('/moe/<contest_type_id>/<area_id>/<band_type>/<category>/<year>')
def __tmp1(contest_type_id, area_id, band_type, category, year) :
    contest = Contest.query.filter(Contest.contest_type_id == contest_type_id, Contest.area_id == area_id, Contest.band_type == band_type, Contest.category == category, Contest.date > datetime.datetime.strptime(year, '%Y'), Contest.date < datetime.datetime.strptime(str(int(year) + 1), '%Y')).first()

    contest.test_pieces = TestPiece.query.filter(TestPiece.contests.any(id=contest.id)).all()

    contest.teams = ContestDetail.query.filter_by(contest_id=contest.id).all()
    contest_name = contest.get_fullname(area=False, category=False, band_type=False)
    contest_area = contest.get_fullname(prefix=False, ctype=False)

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '比賽'},
        {'path': '/contest/moe/', 'name': '學生音樂比賽'},
        {'path': '/contest/moe/%s' % contest_type_id, 'name': contest.get_fullname(prefix=False, area=False, category=False, band_type=False)},
        {'path': '/contest/moe/%s/%s/%s/%s' % (contest_type_id, area_id, band_type, category), 'name': contest_area},
        {'name': year}
    ]

    search_hint = ''
    return render_template(
        'contest-detail.html',
        search_hint=search_hint,
        ascending=True,
        sortme=0,
        contest=contest,
        breadcrumb=breadcrumb,
        contest_name=contest_name,
        contest_area=contest_area)
