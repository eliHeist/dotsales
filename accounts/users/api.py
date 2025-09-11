# people/api.py
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from ninja.responses import Response

from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from ninja_extra import api_controller, http_post, http_get, http_put
from ninja_extra.permissions import IsAuthenticated

# from .models import Branch
from .schemas import LoginResponseSchema, LoginSchema, UserOutAuthedSchema

User = get_user_model()


@api_controller("/auth", tags=["Auth & Users"])
class AuthController:
    # @http_get("/me", response=UserOutSchema, auth=JWTAuth())
    # def me(self, request):
    #     user = request.user
    #     return user
    
    @http_post("/login", response={200: LoginResponseSchema, 401: dict, 403: dict})
    def login(self, request, data: LoginSchema):
        """
        Login. Returns access token and user profile.
        Refresh token is set in an httpOnly cookie.
        """
        user = authenticate(request, email=data.email, password=data.password)
        if not user:
            return {"detail": "Invalid credentials"}, 401
        if not user.is_active:
            return {"detail": "User inactive"}, 403

        print("Authenticated", user)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_str = str(refresh)

        payload = {"access": access, "user": UserOutAuthedSchema.from_orm(user).dict()}

        # cookie lifetime from settings.NINJA_JWT if present
        max_age = None
        if lif := settings.NINJA_JWT.get("REFRESH_TOKEN_LIFETIME"):
            max_age = int(lif.total_seconds())

        resp = Response(payload)
        resp.set_cookie(
            "refresh_token",
            refresh_str,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            max_age=max_age,
            path="/auth/refresh/",
        )
        return resp
    
    @http_post("/refresh", response={200: dict, 401: dict})
    def refresh(self, request, data: LoginSchema):
        """
        Read refresh token from cookie first.
        Return a new access token and user profile.
        """
        token = request.COOKIES.get("refresh_token")
        if not token:
            return Response({"detail": "No refresh token"}, status=401)

        try:
            refresh = RefreshToken(token)
            access = str(refresh.access_token)
            # token payload usually has 'user_id'
            user_id = refresh.get("user_id") or refresh["user_id"]
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=401)

        return {"access": access, "user": UserOutAuthedSchema.from_orm(user).dict()}


