class Config:
    _user_name = ""
    _user_score = 0

    @classmethod
    def set_user_name(cls, name):
        cls._user_name = name

    @classmethod
    def get_user_name(cls):
        return cls._user_name

    @classmethod
    def set_user_score(cls, score):
        cls._user_score = score

    @classmethod
    def get_user_score(cls):
        return cls._user_score
    