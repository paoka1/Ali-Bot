from pydantic import BaseSettings


class Config(BaseSettings):

    key = ''

    inform_group = {}

    class Config:
        extra = "ignore"
