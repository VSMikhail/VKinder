import datetime


def match(user_birthdate: datetime.datetime, search_response: dict, match_from_db: list) -> int:
    """Функция возвращает ID пользователя, подходящего по городу полу и возрасту."""
    potential_partners = {}
    for user in search_response['response']['items']:
        try:
            birthdate_str = user['bdate']
        except KeyError:
            birthdate_str = ''
        if len(birthdate_str) > 5:
            birthdate = datetime.datetime.strptime(birthdate_str, '%d.%m.%Y')
            potential_partners[str(user['id'])] = abs(user_birthdate - birthdate)
    for key in match_from_db:
        potential_partners.pop(str(key))
    for key, value in potential_partners.items():
        if value == min(potential_partners.values()):
            match = key
    return int(match)
