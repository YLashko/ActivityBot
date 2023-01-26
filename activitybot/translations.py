from .config import RECORD_TIME_RANGE

ru = {
    "start": lambda: 'Привет! Запись активности - /activity, доступна с {} до {}, сменить язык / switch language - /lang'
    .format(RECORD_TIME_RANGE[0].strftime("%H:%M:%S"), RECORD_TIME_RANGE[1].strftime("%H:%M:%S")),
    "База данных очищена": lambda: 'База данных очищена',
    "Выберите пользователя. Отмена - /cancel": lambda: "Выберите пользователя. Отмена - /cancel",
    "Язык изменён": lambda: "Язык изменён",
    "Отменить запись активности - /cancel": lambda: "Отменить запись активности - /cancel",
    "Абсолютная оценка количества проделанной работы": lambda: 'Абсолютная оценка количества проделанной работы',
    "Относительная оценка количества проделанной работы": lambda: 'Относительная оценка количества проделанной работы',
    "Абсолютная оценка настроения": lambda: 'Абсолютная оценка настроения',
    "Относительная оценка настроения": lambda: 'Относительная оценка настроения',
    'В данное время нельзя сделать запись': lambda: 'В данное время нельзя сделать запись',
    "Запись отменена": lambda: "Запись отменена",
    "Удаление отменено": lambda: "Удаление отменено",
    "Пользователь удален, если такой существовал": lambda f: f"Пользователь @{f} удален, если такой существовал",
    "Что-то пошло не так.": lambda f: f"Что-то пошло не так. {f}",
    "Ваши оценки записаны!": lambda: "Ваши оценки записаны!",
    "Как прошел твой день? /activity": lambda: "Как прошел твой день? /activity",
    "Нельзя записать активность дважды в день": lambda: "Нельзя записать активность дважды в день"
}

en = {
    "start": lambda: 'Hello! To record activity, send - /activity ({} - {}), сменить язык / switch language - /lang'
    .format(RECORD_TIME_RANGE[0].strftime("%H:%M:%S"), RECORD_TIME_RANGE[1].strftime("%H:%M:%S")),
    "База данных очищена": lambda: 'Database cleared',
    "Выберите пользователя. Отмена - /cancel": lambda: "Choose a user. Cancel - /cancel",
    "Язык изменён": lambda: "The language has been changed",
    "Отменить запись активности - /cancel": lambda: "Cancel activity record - /cancel",
    "Абсолютная оценка количества проделанной работы": lambda: 'Absolute estimate of the amount of work done',
    "Относительная оценка количества проделанной работы": lambda: 'Relative assessment of the amount of work done',
    "Абсолютная оценка настроения": lambda: 'Absolute mood assesment',
    "Относительная оценка настроения": lambda: 'Relative mood assessment',
    'В данное время нельзя сделать запись': lambda: "You can't record activity at this time",
    "Запись отменена": lambda: "The record has been canceled",
    "Удаление отменено": lambda: "The deletion has been cancelled.",
    "Пользователь удален, если такой существовал": lambda f: f"User @{f} deleted, if there was one",
    "Что-то пошло не так.": lambda f: f"Something went wrong. {f}",
    "Ваши оценки записаны!": lambda: "Your assessments have been recorded!",
    "Как прошел твой день? /activity": lambda: "How was your day? /activity",
    "Нельзя записать активность дважды в день": lambda: "You can't record activity twice a day"
}

class Translations:

    def __init__(self) -> None:
        self.languages = {
            "en": en,
            "ru": ru
        }
        self.language_codes = list(self.languages.keys())
        self.users_languages = {}

    def __getitem__(self, key: str) -> dict:
        if key not in list(self.languages.keys()):
            raise KeyError(f"There is no translations for language '{key}'")
        return self.languages[key]

    def t_id(self, user_id: int | str, message_name: str, *args, **kwargs):
        str_uid = str(user_id)
        if str_uid not in list(self.users_languages.keys()):
            raise ValueError(f"There is no language specification for {str_uid}")
        try:
            return self[self.users_languages[str_uid]][message_name](*args, **kwargs)
        except Exception:
            try:
                return self["en"][message_name](*args, **kwargs)
            except Exception:
                return message_name
    
    def set_lang(self, user_id: str, language: str) -> None:
        if language not in list(self.language_codes):
            raise ValueError(f"Can not set language to {language}: this language is not on the available languages list")
        self.users_languages[user_id] = language
    
    def toggle_language(self, user_id: str | int) -> str:
        str_uid = str(user_id)
        if str_uid not in list(self.users_languages.keys()):
            raise ValueError(f"There is no language specification for {str_uid}")
        index_ = self.language_codes.index(self.users_languages[str_uid])
        index_ = (index_ + 1) % len(self.language_codes)
        self.users_languages[str_uid] = self.language_codes[index_]
        return self.users_languages[str_uid]
    
    def set_users_languages(self, language_dict): 
        self.users_languages = language_dict
