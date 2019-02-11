import pytest
from conftest import *
from labco.notifications import Email
import getpass


@pytest.fixture
def email(monkeypatch):
    """Default init"""
    def input_patch(_):
        return 'foobar'
    with monkeypatch.context() as m:
        m.setattr(getpass, 'getpass', input_patch)
        return Email(FROM_ADDR, TO_ADDRS)


def test_default_email(email):
        assert email.from_addr == FROM_ADDR
        assert isinstance(email.from_addr, str)
        assert email.to_addrs == TO_ADDRS
        assert isinstance(email.to_addrs, list)
