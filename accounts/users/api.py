# people/api.py
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from django.http import HttpResponse
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.exceptions import TokenError

from ninja_extra import api_controller, http_post, http_get, http_put

# from .models import Branch
from .schemas import TokenObtainPairIn, TokenObtainPairOut, TokenRefreshIn

User = get_user_model()


@api_controller("/auth", tags=["Auth & Users"])
class AuthController:
    @http_post("/token/pair",
        response={200: TokenObtainPairOut, 401: str},
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

        refresh = RefreshToken.for_user(user)
        # Return the access token in the response body
        return 200, {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    # Refresh token endpoint
    @http_post(
        "/token/refresh",
        response={200: TokenObtainPairOut, 401: str},
        auth=None,
        url_name="token_refresh",
    )
    def refresh_token(self, request, payload: TokenRefreshIn):
        """
        Takes a refresh token from an HttpOnly cookie and returns a
        new access token. Also rotates the refresh token.
        """
        try:
            refresh = RefreshToken(payload.refresh)
            # Blacklist the old refresh token
            if settings.NINJA_JWT["ROTATE_REFRESH_TOKENS"] and settings.NINJA_JWT["BLACKLIST_AFTER_ROTATION"]:
                refresh.blacklist()

            # Generate new tokens
            new_refresh = RefreshToken.for_user(refresh.access_token.get("user_id"))
            new_access = str(new_refresh.access_token)

            return 200, {
                "access": new_access,
                "refresh": str(new_refresh),
            }

        except Exception as e:
            return 401, str(e)

    # Logout endpoint
    @http_post("/token/blacklist", auth=None, url_name="logout")
    def logout(self, request, payload: TokenRefreshIn):
        """
        Logs out a user by blacklisting their refresh token and clearing
        the HttpOnly cookie.
        """

        refresh = RefreshToken(payload.refresh)
        refresh.blacklist()

        return 200, {"message": "Token Blacklisted"}
    
