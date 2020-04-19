from autobahn import wamp
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks


class AppSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("Connected!")
        yield self.register(self)

    @wamp.register("remote_add")
    def remote_add(self, x, y):
        print("return %s" % (x + y))
        return x + y

    @wamp.register("send_public")
    def send_public(self, msg):
        self.publish("public", msg)
        return "OK"


if __name__ == '__main__':
    runner = ApplicationRunner(
        url="ws://127.0.0.1:8080/ws",
        realm="realm1")

    runner.run(AppSession)
