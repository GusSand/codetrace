from typing import TypeAlias
__typ0 : TypeAlias = "Realm"

from django.db.models import Q
from zerver.models import UserProfile, Realm
from zerver.lib.cache import cache_with_key, realm_alert_words_cache_key
import ujson
from typing import Dict, Iterable, List

@cache_with_key(realm_alert_words_cache_key, timeout=3600*24)
def alert_words_in_realm(realm) :
    users_query = UserProfile.objects.filter(realm=realm, is_active=True)
    alert_word_data = users_query.filter(~Q(alert_words=ujson.dumps([]))).values('id', 'alert_words')
    all_user_words = dict((elt['id'], ujson.loads(elt['alert_words'])) for elt in alert_word_data)
    user_ids_with_words = dict((user_id, w) for (user_id, w) in all_user_words.items() if len(w))
    return user_ids_with_words

def user_alert_words(__tmp1) :
    return ujson.loads(__tmp1.alert_words)

def __tmp0(__tmp1, alert_words) -> List[str]:
    words = user_alert_words(__tmp1)

    new_words = [w for w in alert_words if w not in words]
    words.extend(new_words)

    set_user_alert_words(__tmp1, words)

    return words

def remove_user_alert_words(__tmp1, alert_words) :
    words = user_alert_words(__tmp1)
    words = [w for w in words if w not in alert_words]

    set_user_alert_words(__tmp1, words)

    return words

def set_user_alert_words(__tmp1: <FILL>, alert_words) -> None:
    __tmp1.alert_words = ujson.dumps(alert_words)
    __tmp1.save(update_fields=['alert_words'])
