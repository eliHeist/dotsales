from ninja_extra import NinjaExtraAPI

from accounts.users.api import AuthController

global_api = NinjaExtraAPI(version='3.0.0')

global_api.register_controllers(AuthController)

@global_api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}