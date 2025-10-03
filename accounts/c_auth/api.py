# people/api.py
import json
from typing import Any
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from django.http.response import HttpResponse
from ninja_jwt.tokens import RefreshToken, Token
from ninja_jwt.authentication import JWTAuth

from ninja_extra import api_controller, http_post, http_get, http_put

# from .models import Branch
from .schemas import TokenObtainPairIn, TokenObtainPairOut, TokenRefreshIn, UserDetailsOut

User = get_user_model()


@api_controller("/auth", tags=["Auth & Users"])
class AuthController:
    @http_post("/token/pair",
        response={200: None, 401: str},
        auth=None,
        url_name="login",
    )
    def obtain_token(self, request, payload: TokenObtainPairIn):
        """
        Authenticates user, sets HttpOnly cookie for refresh token,
        and returns access token.
        """
        user = authenticate(email=payload.email, password=payload.password)

        if user is None:
            return 401, "Invalid credentials"

        refresh: Token = RefreshToken.for_user(user)
        access: str = str(refresh.access_token)

        response_data = {
            "access": access,
        }
        
        response:HttpResponse = HttpResponse(
            content_type="application/json",
            content=json.dumps(response_data)
        )
        response.set_cookie(
            key=settings.NINJA_JWT.get("JWT_AUTH_COOKIE"),
            value=str(refresh),
            httponly=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_HTTP_ONLY"),
            secure=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_SECURE", True),
            samesite=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_SAMESITE"),
            max_age=settings.NINJA_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds(),
            path=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_PATH"),
        )
        return response

    # Refresh token endpoint
    @http_post(
        "/token/refresh",
        response={200: None, 401: str},
        auth=None,
        url_name="token_refresh",
    )
    def refresh_token(self, request):
        """
        Takes a refresh token from an HttpOnly cookie and returns a
        new access token. Also rotates the refresh token.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return 401, "No refresh token provided"
            
        try:
            refresh = RefreshToken(refresh_token)
            # Blacklist the old refresh token
            if (
                settings.NINJA_JWT["ROTATE_REFRESH_TOKENS"] 
                and settings.NINJA_JWT["BLACKLIST_AFTER_ROTATION"]
            ):
                refresh.blacklist()

            # Generate new tokens
            new_refresh = RefreshToken.for_user(refresh.access_token.get("user_id"))
            new_access = str(new_refresh.access_token)

            response:HttpResponse = HttpResponse(
                content_type="application/json",
                content={"access": access}
            )
            response.set_cookie(
                key=settings.NINJA_JWT.get("JWT_AUTH_COOKIE"),
                value=str(new_refresh),
                httponly=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_HTTP_ONLY"),
                secure=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_SECURE", True),
                samesite=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_SAMESITE"),
                max_age=settings.NINJA_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds(),
                path=settings.NINJA_JWT.get("JWT_AUTH_COOKIE_PATH"),
            )
            return response

        except Exception as e:
            return 401, str(e)

    # Logout endpoint
    @http_post("/token/blacklist", auth=None, url_name="logout")
    def logout(self, request):
        """
        Logs out a user by blacklisting their refresh token and clearing
        the HttpOnly cookie.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return 200, {"message": "No refresh token provided"}

        refresh = RefreshToken(payload.refresh)
        refresh.blacklist()

        return 200, {"message": "Token Blacklisted"}

    @http_get("/me", auth=JWTAuth(), response={
            200: UserDetailsOut, 
            401: str
        }
    )
    def get_user_details(self, request):
        """
        Returns the details of the authenticated user.
        """
        user = request.auth
        return 200, user
