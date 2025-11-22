from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from loguru import logger


class DebuggingSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to debug OAuth failures."""
    
    def pre_social_login(self, request, sociallogin):
        """Log detailed information about social login attempts."""
        logger.info(f"=== SOCIAL LOGIN ATTEMPT ===")
        logger.info(f"Provider: {sociallogin.account.provider}")
        logger.info(f"UID: {sociallogin.account.uid}")
        logger.info(f"Email: {sociallogin.email_addresses}")
        logger.info(f"User: {sociallogin.user}")
        logger.info(f"Extra data keys: {list(sociallogin.account.extra_data.keys())}")
        super().pre_social_login(request, sociallogin)
    
    def save_user(self, request, sociallogin, form=None):
        """Log user creation attempts."""
        try:
            logger.info(f"=== ATTEMPTING TO SAVE USER ===")
            logger.info(f"Email: {sociallogin.email_addresses}")
            logger.info(f"Username: {sociallogin.user.username if hasattr(sociallogin.user, 'username') else 'N/A'}")
            user = super().save_user(request, sociallogin, form)
            logger.info(f"✓ User saved successfully: {user}")
            return user
        except Exception as e:
            logger.error(f"✗ FAILED TO SAVE USER: {type(e).__name__}: {e}")
            logger.exception("Full traceback:")
            raise
