from dataclasses import dataclass


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
    

    def route():
        def wrapper(cls):
            router = cls()
            self.routes.append(router)


