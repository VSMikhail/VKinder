from VK import Vk
from Tinder import match
from Tokens import vk_user_token, vk_chat_bot_token
from Database import Database, conn
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
inst_db = Database(conn())
inst_vk = Vk(vk_user_token)
bot_session = vk_api.VkApi(token=vk_chat_bot_token)
longpoll = VkLongPoll(bot_session)


def current_match(user_id: int):
    """Функция находит подходящего партнера для пользователя ВК. """
    partner_sex = 1
    if inst_vk.get_user_info(user_id)['sex'] == 1:
        partner_sex = 2
    match_from_db = inst_db.select_match(user_id)
    user_city = inst_vk.get_user_info(user_id)['city_id']
    potential_partners = inst_vk.search_potential_partners(partner_sex, user_city)
    user_birthdate = inst_vk.get_user_info(user_id)['birthdate']
    current_match = match(user_birthdate, potential_partners, match_from_db)
    inst_db.add_match(user_id, current_match)
    return current_match


def send_message(vk_session, user_id, message, attachment=None):
    """Функция отправляет сообщение пользователю ВК."""
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': get_random_id(),
                                        'attachment': attachment
                                        }
                      )


if __name__ == '__main__':
    inst_db.delete_table()
    inst_db.create_table()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            in_mes = event.text
            if in_mes.lower() == 'привет':
                send_message(bot_session, event.user_id, 'Введите 1, чтобы подобрать пару.')
            elif in_mes.lower() == '1':
                profile_availability = 0
                while profile_availability != 1:
                    new_match = current_match(event.user_id)
                    if new_match:
                        new_match_name = inst_vk.get_user_info(new_match)['user_name']
                        photos = inst_vk.get_three_photos(new_match)
                        if photos:
                            send_message(bot_session, event.user_id, f'{new_match_name}: https://vk.com/id{str(new_match)}')
                            send_message(bot_session, event.user_id, 'Три популярные фотографии профиля:', photos)
                            send_message(bot_session, event.user_id, 'Введите 1, чтобы подобрать другую пару')
                            profile_availability = 1
                    else:
                        send_message(bot_session, event.user_id, 'Недоступна информация о дате вашего рождения.')

