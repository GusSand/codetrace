from typing import Optional, Dict, Any
from pyoembed import oEmbed, PyOembedException


def get_oembed_data(__tmp0: <FILL>,
                    maxwidth: Optional[int]=640,
                    maxheight: Optional[int]=480) -> Optional[Dict[str, Any]]:
    try:
        data = oEmbed(__tmp0, maxwidth=maxwidth, maxheight=maxheight)
    except PyOembedException:
        return None

    data['image'] = data.get('thumbnail_url')
    return data
