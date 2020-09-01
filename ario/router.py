from dataclasses import dataclass
from typing import List


@dataclass
class Endpoint:
    method: List[str]
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
        if RouterController.__instance is None:
            RouterController()
        return RouterController.__instance


    def __init__(self):
        if RouterController.__instance is None:
            self.routes = []
            RouterController.__instance = self
        else:
            raise Exception("Controller already instantiated")


    def __call__(self):
        pass
    

    def route(self, method, route):
        print(method)
        def wrapper(cls):
            print(cls)
            router = cls(method, route)
            self.routes.append(router)

        return wrapper


