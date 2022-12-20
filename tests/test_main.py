
from main import *
from bson.objectid import ObjectId


class TestClass:
    def test_add(self):
        token_address = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
        chain = "bsc"
        chat_id = -1001612967544
        assert add_token(token_address, chain, chat_id)

    def test_change_ads(self):
        url = "https://t.me/leninMala"
        chat_id = -1001612967544
        assert change_ads(url, chat_id)

    def test_remove_ads(self):
        chat_id = -1001612967544
        assert remove_ads(chat_id)

    def test_change_min_buy(self):
        min_buy = 0.02
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_min_buy(min_buy, group_id, token_id)

    def test_change_emoji(self):
        emoji = '🔵'
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_emoji(group_id, token_id, emoji)

    def test_delete_token(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert delete_token(group_id, token_id)

    def test_change_telegram(self):
        url = "https://t.me/soji_shim"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_telegram(url, group_id, token_id)

    def test_remove_telegram(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_telegram(group_id, token_id)

    def test_change_presale(self):
        url = "https://www.pinksale.finance/launchpad/0x13f625ad1bb28c57beb4c0c5ace302f695cc83dd?chain=BSC"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_presale(url, group_id, token_id)

    def test_remove_presale(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_presale(group_id, token_id)

    def test_change_chart(self):
        url = "https://poocoin.app/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_chart(url, group_id, token_id)

    def test_remove_chart(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_chart(group_id, token_id)

    def test_change_discord(self):
        url = "https://discord.gg/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_discord(url, group_id, token_id)

    def test_remove_discord(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_discord(group_id, token_id)

    def test_change_twitter(self):
        url = "https://twitter.com/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_twitter(url, group_id, token_id)

    def test_remove_twitter(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_twitter(group_id, token_id)

    def test_change_website(self):
        url = "https://www.matakala.io/"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_website(url, group_id, token_id)

    def test_remove_website(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_website(group_id, token_id)

    def test_change_image(self):
        url = "https://res.cloudinary.com/dx5hwvab6/image/upload/v1666265495/Banner_shil_ofls2u.png"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_image(url, group_id, token_id)

    def test_remove_image(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_image(group_id, token_id)

    def test_change_content(self):
        text = "INI CONTENT"
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert change_content(text, group_id, token_id)

    def test_remove_content(self):
        group_id = ObjectId('6347be27293b2388b9db1f93')
        token_id = ObjectId('6350ef9f5b2c7cea3e6ea61a')
        assert remove_content(group_id, token_id)

    def test_resume_all(self):
        chat_id = -1001612967544
        assert resume_all(chat_id)

    def test_pause_all(self):
        chat_id = -1001612967544
        assert pause_all(chat_id)

    def test_delete_all(self):
        chat_id = -1001612967544
        assert delete_all(chat_id)
