from src.core.crypto import decrypt_cookies, encrypt_cookies


class TestCrypto:
    def test_encrypt_decrypt_roundtrip(self):
        original = "# Netscape HTTP Cookie File\n\n.tiktok.com\tTRUE\t/\tTRUE\t1785600000\tsessionid\tabc123"
        encrypted = encrypt_cookies(original)
        assert encrypted != original
        decrypted = decrypt_cookies(encrypted)
        assert decrypted == original

    def test_encrypt_produces_different_output_each_time(self):
        data = "test data"
        e1 = encrypt_cookies(data)
        e2 = encrypt_cookies(data)
        assert e1 != e2

    def test_empty_string(self):
        encrypted = encrypt_cookies("")
        decrypted = decrypt_cookies(encrypted)
        assert decrypted == ""

    def test_unicode_content(self):
        original = "cookies with unicode: \u2603 \U0001f600"
        encrypted = encrypt_cookies(original)
        decrypted = decrypt_cookies(encrypted)
        assert decrypted == original
