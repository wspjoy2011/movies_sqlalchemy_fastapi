from fastapi import APIRouter
from apps.accounts.controllers import (
    create_user_controller,
    activate_user_controller,
    create_profile_controller,
    login_controller,
    access_token_refresh_controller
)

router = APIRouter()

router.post("/users", status_code=201)(create_user_controller)
router.get("/users/activate/{token}", status_code=200)(activate_user_controller)
router.post("/users/{user_id}/profile", status_code=201)(create_profile_controller)
router.post("/auth/token/login", status_code=201)(login_controller)
router.post("/auth/token/refresh", status_code=201)(access_token_refresh_controller)
