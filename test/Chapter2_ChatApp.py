import unittest
import unittest.mock


class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        user1 = ChatClient("Goldi Goldenhair")
        user2 = ChatClient("Rumpeltiltskin")

        user1.send_message("Hello World")
        messages = user2.fetch_messages()

        assert messages == ["Goldi Goldenhair: Hello World"]


class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("User 1")

        assert client.nickname == "User 1"

    def test_send_message(self):
        client = ChatClient("User 1")
        client.connection = unittest.mock.Mock()

        sent_message = client.send_message("Hello World")

        assert sent_message == "User 1: Hello World"

    def test_client_connection(self):
        client = ChatClient("User 1")

        connection_spy = unittest.mock.MagicMock()
        with unittest.mock.patch.object(client, "_get_connection",
                                        return_value=connection_spy):
            client.send_message("Test test")

            connection_spy.broadcast.assert_called_with("User 1 : Test test")


class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        with unittest.mock.patch.object(Connection, "connect"):
            conn = Connection(("localhost", 9090))

        with unittest.mock.patch.object(conn, "get_messages", return_value=[]):
            conn.broadcast("test message")

            assert conn.get_messages()[-1] == "test message"


class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname
        self.connection = None

    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message

    @property
    def connection(self):
        if self.connection is None:
            self.connection = self._get_connection()
        return self.connection

    @connection.setter
    def connection(self, value):
        if self.connection is not None:
            self.connection.close()
        self.connection = value

    def _get_connection(self):
        return Connection(("localhost", 9090))


from multiprocessing.managers import SyncManager


class Connection(SyncManager):
    def __init__(self, address):
        self.register("get_messages")
        super().__init__(address=address)
        self.connect()

    def broadcast(self, message):
        messages = self.get_messages()
        messages.append(message)


if __name__ == '__main__':
    unittest.main()