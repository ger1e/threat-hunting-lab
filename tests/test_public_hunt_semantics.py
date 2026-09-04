from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read_hunt(name: str) -> str:
    return (ROOT / "hunts" / name).read_text(encoding="utf-8")


class PublicHuntSemanticTests(unittest.TestCase):
    def test_device_code_follow_on_is_successful_and_endpoint_correlated(self) -> None:
        text = read_hunt("device-code-follow-on.kql")
        self.assertIn("SigninLogs", text)
        self.assertNotIn("AADSignInEventsBeta", text)
        self.assertIn('AuthenticationProtocol =~ "deviceCode"', text)
        self.assertRegex(text, r'ResultType\)\s*==\s*"0"')
        self.assertIn("DeviceProcessEvents", text)
        self.assertIn("FollowOnWindow", text)
        self.assertIn("join kind=inner", text)
        self.assertNotIn("| where Attempts > 0", text)

    def test_rare_outbound_hunt_only_claims_repeated_public_connections(self) -> None:
        text = read_hunt("rare-outbound-beaconing.kql")
        title = next(line for line in text.splitlines() if line.startswith("// Title:"))
        description = next(line for line in text.splitlines() if line.startswith("// Description:"))
        self.assertNotIn("periodic", title.casefold())
        self.assertNotIn("beacon", title.casefold())
        self.assertNotIn("periodic", description.casefold())
        self.assertIn("ipv4_is_private(RemoteIP) == false", text)

    def test_powershell_header_does_not_claim_unimplemented_no_profile_logic(self) -> None:
        text = read_hunt("suspicious-powershell-encoded-command.kql")
        behavior = next(line for line in text.splitlines() if line.startswith("// Suspicious Behavior:"))
        if "no-profile" in behavior.casefold():
            self.assertRegex(text.casefold(), r"-(?:nop|noprofile)\b")


if __name__ == "__main__":
    unittest.main()
