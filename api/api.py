from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}