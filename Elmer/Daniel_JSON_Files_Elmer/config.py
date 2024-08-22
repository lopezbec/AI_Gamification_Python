import os
import sys


class Config:
    _user_name = ""

    @classmethod
    def set_user_name(cls, name):
        cls._user_name = name

    @classmethod
    def get_user_name(cls):
        return cls._user_name
