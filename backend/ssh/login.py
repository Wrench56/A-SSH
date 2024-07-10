from typing import Dict, Tuple

import logging


async def parse(data: Dict[str, str]) -> Tuple[str, int, str, str]:
    password = data.get('password')
    if password is None:
        logging.error('Corruption detected in login data in A-SSH')
        return ('Invalid', 0, '', '')
    user_loc = data.get('user_and_location')
    if user_loc is None:
        logging.error('Corruption detected in login data in A-SSH')
        return ('Invalid', 0, '', '')
    user, loc = user_loc.split('@', 1)
    if len(loc.split(':', 1)) > 1:
        host, port_ = loc.split(':', 1)
        port = int(port_)
    else:
        host, port = loc, 22
    return (host, port, user, password)
