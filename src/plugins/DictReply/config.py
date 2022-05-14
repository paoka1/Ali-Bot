from pydantic import BaseSettings


class Config(BaseSettings):

    reply_dic = {}

    class Config:
        extra = "ignore"
