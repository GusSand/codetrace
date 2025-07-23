from flask import Blueprint, render_template
from models import TestPiece, ContestDetail, Contest

TESTPIECE_MOD = Blueprint('testpiece_mod', __name__)


@TESTPIECE_MOD.route('/')
def __tmp2() -> str:
    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '比賽曲'}
    ]

    search_fields = ['piece-name', 'piece-composer', 'piece-arranger']
    search_hint = '曲名 / 作曲者 / 編曲者'

    test_pieces = TestPiece.query.all()
    for piece in test_pieces:
        piece.set_piece_count = Contest.query.filter_by(venue_id=piece.id).count()
        piece.own_choice_count = ContestDetail.query.filter_by(own_choice_id=piece.id).count()

    return render_template(
        'test-pieces.html',
        search_fields=search_fields,
        search_hint=search_hint,
        ascending=True,
        test_pieces=test_pieces,
        breadcrumb=breadcrumb)


@TESTPIECE_MOD.route('/<test_piece_id>')
def __tmp0(__tmp1: <FILL>) :
    search_fields = ['piece-name', 'piece-composer', 'piece-arranger']
    search_hint = '曲名 / 作曲者 / 編曲者'

    test_piece = TestPiece.query.filter_by(id=__tmp1).first()
    test_piece.set_piece_count = Contest.query.filter_by(venue_id=test_piece.id).count()
    test_piece.own_choice_count = ContestDetail.query.filter_by(own_choice_id=test_piece.id).count()

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'path': '/test-piece/', 'name': '比賽曲'},
        {'name': test_piece.name}
    ]

    test_piece_history = Contest.query.filter(Contest.set_pieces.any(id=test_piece.id)).all()

    own_choice_history = ContestDetail.query.filter_by(own_choice_id=test_piece.id).all()

    recordings = ContestDetail.query.filter(ContestDetail.set_piece_id.is_(test_piece.id), ContestDetail.set_piece_recording.isnot(None)).all() + ContestDetail.query.filter(ContestDetail.own_choice_id == test_piece.id, ContestDetail.own_choice_recording.isnot(None)).all()

    return render_template(
        'test-piece.html',
        search_fields=search_fields,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        piece=test_piece,
        test_piece_history=test_piece_history,
        own_choice_history=own_choice_history,
        recordings=recordings)
