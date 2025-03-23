from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📲 РЕГИСТРАЦИЯ", url="https://1wcneg.com/v3/2158/1win-mines?p=8amb"),
         InlineKeyboardButton(text="📑 ИНСТРУКЦИЯ", callback_data="btn2")],  # Две кнопки в одном ряду
        [InlineKeyboardButton(text="🚀 ВЫДАТЬ СИГНАЛ ", callback_data="links", width=2)]  # Одна кнопка на всю ширину
    ]
)



#
# instruction_menu = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="📲 РЕГИСТРАЦИЯ", url="https://1wcneg.com/v3/2158/1win-mines?p=8amb")],
#         [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")],
#     ]
# )
#
# currency_pairs = [
#     ("🇺🇸/🇯🇵 USD/JPY OTC", "usd_jpy"),
#     ("🇬🇧/🇺🇸 GBP/USD OTC", "gbp_usd"),
#     ("🇪🇺/🇺🇸 EUR/USD OTC", "eur_usd"),
#     ("🇦🇺/🇨🇭 AUD/CHF OTC", "aud_chf"),
#     ("🇦🇺/🇨🇦 AUD/CAD OTC", "aud_cad"),
#     ("🇬🇧/🇨🇦 GBP/CAD OTC", "gbp_cad"),
#     ("🇪🇺/🇦🇺 EUR/AUD OTC", "eur_aud"),
#     ("🇪🇺/🇨🇭 EUR/CHF OTC", "eur_chf"),
#     ("🇳🇿/🇺🇸 NZD/USD OTC", "nzd_usd"),
#     ("🇬🇧/🇨🇭 GBP/CHF OTC", "gbp_chf"),
#     ("🇬🇧/🇯🇵 GBP/JPY OTC", "gbp_jpy"),
#     ("🇺🇸/🇨🇦 USD/CAD OTC", "usd_cad"),
# ]
#
# buttons = [
#     InlineKeyboardButton(text=pair[0], callback_data="traps") for pair in currency_pairs # пока что callback_data оставляем одинаковой для всех вариантов
# ]
#
# traps_menu = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)])
#
# signal_menu = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="🔄 Новый сигнал", callback_data="btn_new_signal")],
#         [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
#     ]
# )
#
# unregistered_menu = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="📲 РЕГИСТРАЦИЯ", url="https://1wcneg.com/v3/2158/1win-mines?p=8amb")],
#         [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
#     ]
# )
#
# time_menu = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="1 минута", callback_data="time_60"),
#             InlineKeyboardButton(text="2 минуты", callback_data="time_120"),
#         ],
#         [
#             InlineKeyboardButton(text="3 минуты", callback_data="time_180"),
#             InlineKeyboardButton(text="4 минуты", callback_data="time_240"),
#         ],
#         [InlineKeyboardButton(text="5 минут", callback_data="time_300"),]
#     ]
# )