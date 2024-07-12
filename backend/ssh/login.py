from typing import Dict, Tuple

import logging


async def parse(data: Dict[str, str]) -> Tuple[str, int, str, str]:
    password = data.get('password')
    if password is None:
        logging.error('Corruption detected in login data in A-SSH')
        return ('Invalid', 0, '', '')
    user_loc_unsplit = data.get('user_and_location')
    if user_loc_unsplit is None:
        logging.error('Corruption detected in login data in A-SSH')
        return ('Invalid', 0, '', '')
    user_loc_split = user_loc_unsplit.split('@', 1)
    if len(user_loc_split) == 1:
        user = user_loc_split[0]
        host = 'localhost'
        port = 22
    else:
        user, loc = user_loc_split
        if len(loc.split(':', 1)) > 1:
            host, port_ = loc.split(':', 1)
            port = int(port_)
        else:
            host, port = loc, 22

    return (host, port, user, password)
