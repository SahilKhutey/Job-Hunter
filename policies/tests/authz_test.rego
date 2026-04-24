package hunteros.authz_test

import data.hunteros.authz

test_allow_user_on_dashboard {
    authz.allow with input as {
        "token": {"scope": "user"},
        "path": "/api/v1/dashboard"
    }
}

test_deny_user_on_export {
    not authz.allow with input as {
        "token": {"scope": "user"},
        "path": "/api/v1/analytics/export"
    }
}

test_allow_stepup_on_export {
    authz.allow with input as {
        "token": {"scope": "step-up"},
        "path": "/api/v1/analytics/export"
    }
}

test_allow_admin_everywhere {
    authz.allow with input as {
        "token": {"role": "admin"},
        "path": "/api/v1/user/delete"
    }
}
