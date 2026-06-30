"""Power BI Authentication for DataTrace.

Provides authentication flows for Power BI REST API using MSAL.
"""

import logging
from typing import Optional

from msal import ConfidentialClientApplication, PublicClientApplication

from datatrace.config.settings import get_settings
from datatrace.lib.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class PowerBIAuth:
    """Base Power BI authentication handler."""

    def __init__(self):
        """Initialize Power BI auth handler."""
        self.settings = get_settings().powerbi

    def get_access_token(self) -> str:
        """Get access token for Power BI API.

        Returns:
            Access token string
        """
        raise NotImplementedError("Subclasses must implement get_access_token")

    def get_token_for_scope(self, scopes: Optional[list[str]] = None) -> str:
        """Get token for specific scopes.

        Args:
            scopes: List of scopes to request

        Returns:
            Access token string
        """
        if scopes is None:
            scopes = [self.settings.scope]
        return self.get_access_token()


class ServicePrincipalAuth(PowerBIAuth):
    """Service Principal authentication for Power BI.

    Uses MSAL ConfidentialClientApplication for automated, headless authentication.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """Initialize Service Principal auth.

        Args:
            client_id: Azure AD application client ID
            tenant_id: Azure AD tenant ID
            client_secret: Service principal client secret
        """
        super().__init__()
        self.client_id = client_id or self.settings.client_id
        self.tenant_id = tenant_id or self.settings.tenant_id
        self.client_secret = client_secret or self.settings.client_secret

        if not self.client_id:
            raise AuthenticationError(
                "Service Principal authentication requires client_id",
                provider="powerbi_service_principal",
            )
        if not self.tenant_id:
            raise AuthenticationError(
                "Service Principal authentication requires tenant_id",
                provider="powerbi_service_principal",
            )
        if not self.client_secret:
            logger.warning(
                "No client_secret provided. Service principal auth will fail without it."
            )

        self.authority = self.settings.authority.format(tenant_id=self.tenant_id)
        self.app: Optional[ConfidentialClientApplication] = None

    def _get_app(self) -> ConfidentialClientApplication:
        """Get or create MSAL ConfidentialClientApplication."""
        if self.app is None:
            self.app = ConfidentialClientApplication(
                self.client_id,
                client_credential=self.client_secret,
                authority=self.authority,
            )
        return self.app

    def get_access_token(self) -> str:
        """Get access token using service principal.

        Returns:
            Access token string
        """
        try:
            app = self._get_app()
            result = app.acquire_token_for_client(scopes=[self.settings.scope])

            if "access_token" not in result:
                error = result.get("error_description", result.get("error", "Unknown error"))
                logger.error(f"Failed to acquire token: {error}")
                raise AuthenticationError(
                    f"Service principal authentication failed: {error}",
                    provider="powerbi_service_principal",
                )

            logger.debug("Successfully acquired Power BI access token via service principal")
            return result["access_token"]

        except Exception as e:
            logger.error(f"Service principal auth error: {e}")
            raise AuthenticationError(
                f"Service principal authentication error: {e}",
                provider="powerbi_service_principal",
            )


class UserAuth(PowerBIAuth):
    """User authentication for Power BI.

    Uses MSAL PublicClientApplication for interactive user authentication.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        username: Optional[str] = None,
    ):
        """Initialize User auth.

        Args:
            client_id: Azure AD application client ID
            tenant_id: Azure AD tenant ID
            username: Optional username for username/password flow
        """
        super().__init__()
        self.client_id = client_id or self.settings.client_id
        self.tenant_id = tenant_id or self.settings.tenant_id
        self.username = username

        if not self.client_id:
            raise AuthenticationError(
                "User authentication requires client_id",
                provider="powerbi_user",
            )

        self.authority = self.settings.authority.format(tenant_id=self.tenant_id)
        self.app: Optional[PublicClientApplication] = None

    def _get_app(self) -> PublicClientApplication:
        """Get or create MSAL PublicClientApplication."""
        if self.app is None:
            self.app = PublicClientApplication(
                self.client_id,
                authority=self.authority,
            )
        return self.app

    def get_access_token(self) -> str:
        """Get access token using interactive user authentication.

        Returns:
            Access token string
        """
        try:
            app = self._get_app()
            result = app.acquire_token_interactive(scopes=[self.settings.scope])

            if "access_token" not in result:
                error = result.get("error_description", result.get("error", "Unknown error"))
                logger.error(f"Failed to acquire token: {error}")
                raise AuthenticationError(
                    f"User authentication failed: {error}",
                    provider="powerbi_user",
                )

            logger.debug("Successfully acquired Power BI access token via user authentication")
            return result["access_token"]

        except Exception as e:
            logger.error(f"User auth error: {e}")
            raise AuthenticationError(
                f"User authentication error: {e}",
                provider="powerbi_user",
            )
