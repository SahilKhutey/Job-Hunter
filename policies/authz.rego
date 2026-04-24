package hunteros.authz

import future.keywords.if
import future.keywords.in

default allow = false

# Allow if valid JWT and user has basic access
allow if {
    input.token.scope == "user"
    not is_sensitive_path
}

# Require 'step-up' scope for sensitive operations
allow if {
    input.token.scope == "step-up"
    is_sensitive_path
}

# Admin has full access
allow if {
    input.token.role == "admin"
}

# Helper: Identify sensitive paths
is_sensitive_path if {
    input.path in ["/api/v1/user/delete", "/api/v1/analytics/export", "/api/v1/auth/mfa/enable"]
}
