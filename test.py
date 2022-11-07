
from main import *


class TestClass:
    def test_add(self):
        token_address = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
        chain = "bsc"
        chat_id = -1001612967544

        assert add_token(token_address, chain, chat_id)

    def test_token_check(self):
        assert buy_check() == None
