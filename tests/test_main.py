
from app import *
from bson.objectid import ObjectId


class TestClass:
    def test_add(self):
        token_address = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
        chain = "bsc"
        chat_id = -1001612967544
        data = {token_address, chain, chat_id}
        assert add_token(data)

    def test_change_ads(self):
        url = "https://t.me/leninMala"
        chat_id = -1001612967544
        data = {url, chat_id}
        assert change_ads(data)

    def test_remove_ads(self):
        chat_id = -1001612967544
        data = {chat_id}
        assert remove_ads(data)

    def test_change_min_buy(self):
        min_buy = 0.02
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {min_buy, group_id, token_id}
        assert change_min_buy(data)

    def test_change_emoji(self):
        emoji = '🔵'
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {emoji, group_id, token_id}
        assert change_emoji(data)

    def test_delete_token(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert delete_token(data)

    def test_change_telegram(self):
        url = "https://t.me/soji_shim"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_telegram(data)

    def test_remove_telegram(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_telegram(data)

    def test_change_presale(self):
        url = "https://www.pinksale.finance/launchpad/0x13f625ad1bb28c57beb4c0c5ace302f695cc83dd?chain=BSC"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_presale(data)

    def test_remove_presale(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_presale(data)

    def test_change_chart(self):
        url = "https://poocoin.app/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_chart(data)

    def test_remove_chart(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_chart(data)

    def test_change_discord(self):
        url = "https://discord.gg/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_discord(data)

    def test_remove_discord(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_discord(data)

    def test_change_twitter(self):
        url = "https://twitter.com/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_twitter(data)

    def test_remove_twitter(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_twitter(data)

    def test_change_website(self):
        url = "https://www.matakala.io/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_website(data)

    def test_remove_website(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_website(data)

    def test_change_image(self):
        url = "https://res.cloudinary.com/dx5hwvab6/image/upload/v1666265495/Banner_shil_ofls2u.png"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {url, group_id, token_id}
        assert change_image(data)

    def test_remove_image(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_image(data)

    def test_change_content(self):
        text = "INI CONTENT"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {text, group_id, token_id}
        assert change_content(data)

    def test_remove_content(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        data = {group_id, token_id}
        assert remove_content(data)

    def test_resume_all(self):
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        chat_id = -1001612967544
        is_paused = False
        data = {chat_id, is_paused}
        assert update_token(token_id, data)

    def test_delete_all(self):
        chat_id = -1001612967544
        data = {chat_id}
        assert delete_all(data)
