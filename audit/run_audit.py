import sys
import os

# Add the current directory to sys.path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_tests import run_api_tests
from auth_tests import run_auth_tests
from security_scan import run_security_scan
from service_checks import run_service_checks
from advanced_security import run_advanced_security


def main():
    print("="*60)
    print("🛡️  HUNTEROS SYSTEM AUDIT ENGINE")
    print("="*60)
    print("Target Environment: http://localhost:8000")

    try:
        run_service_checks()
        run_api_tests()
        run_auth_tests()
        run_security_scan()
        run_advanced_security()

        
        print("\n" + "="*60)
        print("✅ AUDIT COMPLETE - SYSTEM STABLE")
        print("="*60)
    except KeyboardInterrupt:
        print("\n⚠️ Audit Interrupted by User")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ AUDIT FAILED CRITICALLY: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
