from pydantic import BaseSettings


class Config(BaseSettings):

    inform_group = {}

    class Config:
        extra = "ignore"
