import unittest2 as unittest
from nose.plugins.attrib import attr
from mock import MagicMock, patch
from jnpr.junos.transport.tty_telnet import Telnet


@attr('unit')
class TestTTYTelnet(unittest.TestCase):

    @patch('jnpr.junos.transport.tty_telnet.telnetlib.Telnet')
    def setUp(self, mpock_telnet):
        self.tel_conn = Telnet(host='1.1.1.1', user='test',
                               password='password123', port=23,
                               timeout=30)

    def test_open(self):
        self.tel_conn._tty_open()
        self.tel_conn._tn.open.assert_called()

    def test_open_exception(self):
        self.tel_conn._tn.open.side_effect = Exception
        Telnet.RETRY_OPEN = 1
        Telnet.RETRY_BACKOFF = 0.1
        self.assertRaises(RuntimeError, self.tel_conn._tty_open)
        # reset
        Telnet.RETRY_OPEN = 3
        Telnet.RETRY_BACKOFF = 2

    def test_close(self):
        self.tel_conn._tty_close()
        self.tel_conn._tn.close.assert_called()

    def test_read(self):
        self.tel_conn.read()
        self.tel_conn._tn.read_until.assert_called()

    def test_read_prompt_RuntimeError(self):
        self.tel_conn.expect = MagicMock()
        self.tel_conn.expect =(None, None, 'port already in use')
        self.assertRaises(RuntimeError, self.tel_conn._login_state_machine)



