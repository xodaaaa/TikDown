
from src.api.routes.cookies import _validate_json_content, _validate_netscape_content, json_cookies_to_netscape


class TestCookieValidation:
    def test_validate_netscape_valid(self):
        content = """# Netscape HTTP Cookie File
.tiktok.com\tTRUE\t/\tTRUE\t1785600000\tsessionid\tabc123
.tiktok.com\tTRUE\t/\tTRUE\t1785600000\ttt_csrf_token\txyz789
"""
        valid, msg = _validate_netscape_content(content)
        assert valid
        assert msg == ""

    def test_validate_netscape_missing_header(self):
        content = ".tiktok.com\tTRUE\t/\tTRUE\t1785600000\tsessionid\tabc123"
        valid, msg = _validate_netscape_content(content)
        assert not valid
        assert "Missing Netscape header" in msg

    def test_validate_netscape_missing_sessionid(self):
        content = "# Netscape HTTP Cookie File\n.tiktok.com\tTRUE\t/\tTRUE\t1785600000\tother\tval"
        valid, msg = _validate_netscape_content(content)
        assert not valid
        assert "sessionid" in msg.lower()

    def test_validate_json_valid(self):
        content = (
            '[{"domain":".tiktok.com","name":"sessionid","value":"abc"},'
            '{"domain":".tiktok.com","name":"tt_csrf_token","value":"xyz"}]'
        )
        valid, msg, cookies_list = _validate_json_content(content)
        assert valid
        assert len(cookies_list) == 2

    def test_validate_json_missing_sessionid(self):
        content = '[{"domain":"example.com","name":"other","value":"val"}]'
        valid, msg, cookies_list = _validate_json_content(content)
        assert not valid
        assert "sessionid" in msg.lower()

    def test_validate_json_invalid_json(self):
        content = "not json"
        valid, msg, cookies_list = _validate_json_content(content)
        assert not valid
        assert "Invalid JSON" in msg

    def test_json_to_netscape_conversion(self):
        cookies = [
            {
                "domain": ".tiktok.com",
                "name": "sessionid",
                "value": "abc123",
                "path": "/",
                "secure": True,
                "expirationDate": 1785600000,
            },
            {
                "domain": ".tiktok.com",
                "name": "tt_csrf_token",
                "value": "xyz789",
                "path": "/",
                "secure": False,
            },
        ]
        result = json_cookies_to_netscape(cookies)
        assert result.startswith("# Netscape HTTP Cookie File")
        assert "sessionid" in result
        assert "abc123" in result
        assert "tt_csrf_token" in result
        assert "xyz789" in result
