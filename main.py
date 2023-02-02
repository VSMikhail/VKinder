from vk import Vk
from tinder import match
from tokens import vk_user_token
from database import Database, conn
inst_db = Database(conn())
inst_vk = Vk(vk_user_token)
user_id = 30183124


def current_match(user_id: int):
    """Функция находит подходящего партнера для пользователя ВК.
    """
    partner_sex = 1
    if inst_vk.get_sex(user_id) == 1:
        partner_sex = 2
    match_from_db = inst_db.select_match(user_id)
    user_city = inst_vk.get_city_id(user_id)
    potential_partners = inst_vk.search_potential_partners(partner_sex, user_city)
    user_birthdate = inst_vk.get_birthdate(user_id)
    current_match = match(user_birthdate, potential_partners, match_from_db)
    inst_db.add_match(user_id, current_match)
    print(f'https://vk.com/id{current_match}')


current_match(user_id)
