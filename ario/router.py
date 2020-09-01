from dataclasses import dataclass


@dataclass
class Endpoint:
    method: str
    route: str


    def __call__(self):
        print(f"{self.route} called with {self.method}")


    def __eq__(self, other):
        if (self.method == other.method 
                and self.route == other.route):
            return True
        else:
            return False


class RouterController:
    __instance = None


    @staticmethod
    def get_instance():
        if __instance is None:
            RouterController()
        return RouterController.__instance


    def __init__(self):
        if __instance is None:
            self.routes = []
            RouterController.__instance = self
        else:
            raise Exception("Controller already instantiated")


    def __call__(self):
        pass
    

    def route(cls):
        def wrapper():
            router = cls()
            self.routes.append(router)


