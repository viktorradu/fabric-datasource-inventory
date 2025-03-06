import os
from azure.identity import DefaultAzureCredential
from azure.identity import AzureAuthorityHosts

class Auth:
    def __init__(self):
        self.token_cache = {}
        self.tenant_id = None
        self.client_id = None
        self.client_secret = None

    def set_sp_credentials(self, tenant_id: str, client_id: str, client_secret: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self, scope: str):
        if scope not in self.token_cache:
            if self.tenant_id is not None:
                os.environ['AZURE_TENANT_ID'] = self.tenant_id
                os.environ['AZURE_CLIENT_ID'] = self.client_id
                os.environ['AZURE_CLIENT_SECRET'] = self.client_secret
                credentials = DefaultAzureCredential(
                    authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD,
                    exclude_interactive_browser_credential = True,
                    exclude_managed_identity_credential = True,
                    exclude_environment_credential = False,
                    exclude_workload_identity_credential = True,
                    exclude_developer_cli_credential = True,
                    exclude_shared_token_cache_credential = True,
                    exclude_cli_credential = True,
                    exclude_powershell_credential = True
                )
            else:
                credentials = DefaultAzureCredential(
                    authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD,
                    exclude_interactive_browser_credential = False,
                    exclude_managed_identity_credential = True,
                    exclude_environment_credential = True,
                    exclude_workload_identity_credential = True,
                    exclude_developer_cli_credential = True,
                    exclude_shared_token_cache_credential = True,
                    exclude_cli_credential = True,
                    exclude_powershell_credential = True
                )
            token = credentials.get_token(scope).token
            self.token_cache[scope] = token
        return self.token_cache[scope]