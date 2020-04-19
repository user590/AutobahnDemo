from autobahn.twisted.component import Component, run
from autobahn.wamp.types import RegisterOptions
import autobahn.wamp.message as message
from twisted.internet.defer import inlineCallbacks, returnValue

component = Component(
    transports=[
        {
            "type": "websocket",
            "serializers": ["json"],
            "url": "ws://localhost:8080/ws",
            "endpoint": {
                "type": "tcp",
                "host": "localhost",
                "port": 8080,
            },
            "options": {
                "open_handshake_timeout": 100,
            }
        },
    ],
    realm="realm1"
)


@component.on_join
@inlineCallbacks
def join(session, details):
    print("joined {}: {}".format(session, details))
    msg = message.Publish(topic="public", payload="123".encode())
    session._transport.send(msg)
    yield

@component.register(
    "remote_add",
    options=RegisterOptions(details_arg='details'),
)
@inlineCallbacks
def foo(*args, **kw):
    print("remote_add called: {}, {}".format(args, kw))
    res = sum(args)
    print("returning %s" % res)
    returnValue(res)
    yield


if __name__ == "__main__":
    run([component])