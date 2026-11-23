"""OIDC/JWT verification and fail-closed principal extraction."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import jwt

from ..settings import Settings
from .errors import AuthenticationError, AuthorizationError


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    tenant_id: str
    scopes: frozenset[str]
    issuer: str
    token_id: str | None = None


def _signing_key(token: str, settings: Settings):
    if settings.oidc_jwks_url:
        if not settings.oidc_jwks_url.startswith("https://") and settings.environment not in {"development", "test", "ci"}:
            raise AuthenticationError("oidc_jwks_must_use_https")
        try:
            return jwt.PyJWKClient(settings.oidc_jwks_url, cache_keys=True).get_signing_key_from_jwt(token).key
        except Exception as exc:
            raise AuthenticationError("oidc_jwks_unavailable_or_key_unknown") from exc
    if settings.oidc_public_key_file:
        try:
            return Path(settings.oidc_public_key_file).read_text(encoding="utf-8")
        except OSError as exc:
            raise AuthenticationError("oidc_verification_key_unavailable") from exc
    raise AuthenticationError("oidc_verification_not_configured")


def authenticate_token(token: str, settings: Settings) -> Principal:
    if not token or len(token) > 16384:
        raise AuthenticationError()
    if not settings.oidc_issuer or not settings.oidc_audience:
        raise AuthenticationError("oidc_issuer_or_audience_not_configured")
    algorithms = [value.strip() for value in settings.oidc_algorithms.split(",") if value.strip()]
    if not algorithms or any(value.lower().startswith("hs") for value in algorithms):
        raise AuthenticationError("unsafe_oidc_algorithm_configuration")
    key = _signing_key(token, settings)
    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=algorithms,
            issuer=settings.oidc_issuer,
            audience=settings.oidc_audience,
            options={"require": ["exp", "iat", "iss", "sub", "aud"]},
            leeway=15,
        )
    except jwt.PyJWTError as exc:
        raise AuthenticationError("token_signature_or_claim_validation_failed") from exc
    subject = claims.get("sub")
    tenant_id = claims.get("tenant_id")
    if not isinstance(subject, str) or not subject or not isinstance(tenant_id, str) or not tenant_id:
        raise AuthenticationError("required_principal_claims_missing")
    raw_scopes = claims.get("scope", claims.get("scp", []))
    if isinstance(raw_scopes, str):
        scopes = frozenset(item for item in raw_scopes.split() if item)
    elif isinstance(raw_scopes, list) and all(isinstance(item, str) for item in raw_scopes):
        scopes = frozenset(raw_scopes)
    else:
        raise AuthenticationError("invalid_scope_claim")
    return Principal(
        subject=subject,
        tenant_id=tenant_id,
        scopes=scopes,
        issuer=str(claims["iss"]),
        token_id=claims.get("jti") if isinstance(claims.get("jti"), str) else None,
    )


def require_scope(principal: Principal, scope: str) -> None:
    if scope not in principal.scopes:
        raise AuthorizationError("required_scope_missing")
