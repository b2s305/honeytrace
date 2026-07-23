import paramiko

from database.attacker_repo import save_attacker
from database.session_repo import create_session
from database.credential_repo import save_credential


class HoneyTraceSSHServer(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):

        print("\n===================================")
        print("🚨 SSH Login Attempt")
        print("===================================")
        print(f"IP Address : {self.client_ip}")
        print(f"Username   : {username}")
        print(f"Password   : {password}")

        try:
            attacker_id = save_attacker(self.client_ip)

            session_id = create_session(attacker_id)

            save_credential(session_id, username, password)

            print("✅ Login attempt saved to MySQL")

        except Exception as e:
            print("❌ Database Error:", e)

        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED