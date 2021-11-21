from dataclasses import dataclass, asdict
from types import SimpleNamespace
from pype import functionize, pgetattr, pfilter, peq, psort


class ForbiddenError(Exception):
    pass


@dataclass
class User:
    username: str = ''
    hidden: bool = False

    @staticmethod
    def find_by_key(key):
        return users.get(key)

    @staticmethod
    def all():
        return users.values()

    def can(self, action, target):
        if action == 'read' and target == 'User':
            return True
        return False

    def __lt__(self, rhs):
        return self.username < rhs.username


users = {
    'admin': User('admin'),
    'jim': User('jim'),
    'secret': User('jim', hidden=True),
}

@functionize
def authenticate(request):
    key = request.params.key
    user = User.find_by_key(key)
    if user is None:
        raise ForbiddenError()
    request.user = user
    request.authenticated = True
    return request


@functionize
def authorize(action, target):
    @functionize
    def inner(request):
        if request.user.can(action, target):
            return request
        else:
            raise ForbiddenError()
    return inner


@functionize
def serialize(model):
    if isinstance(model, list):
        return [asdict(m) for m in model]
    return asdict(model)


@functionize
def respond(obj):
    return HttpResponse(data=obj)


@dataclass
class HttpResponse:
    status: int = 200
    data: str = ''


def server_action(function):
    def inner(self, request):
        try:
            response = function(self, request)
            return HttpResponse(data=response)
        except ForbiddenError as error:
            return HttpResponse(status=403, data=error)
    return inner

@functionize
def paginate(request):
    @functionize
    def inner(array):
        return array
    return inner


class UserController:
    @server_action
    def show(self, request):
        return request \
            | authenticate \
            | authorize('read', 'User') \
            | pgetattr('user') \
            | serialize

    @server_action
    def index(self, request):
        request = request | authenticate | authorize('read', 'User')
        return User.all()\
            | pfilter * (pgetattr('hidden') | peq(False)) \
            | psort \
            | paginate(request)\
            | serialize


if __name__ == '__main__':
    request = SimpleNamespace(
        params=SimpleNamespace(
            key='admin'
        )
    )
    print(UserController().show(request))
    print(UserController().index(request))
