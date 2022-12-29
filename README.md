## Installing dependencies

To install the dependencies for working with this project just run

```
pip install -e .\[dev]
```

## Keycloak configuration

Since the REST API will use Keycloak as a third-party application
to manage the user account and the AuthN/AuthZ, it will be required
to configure some parameters to take in account to connect with
the Keycloak server

The `.env` file or Environment Variables should be configured with
the following data:

```properties
KC_BASE_URL="http://keycloak.url"
KC_REALM="realm_of_the_project"
KC_REALM_URL = "http://keycloak.url/realms/realm_of_the_project"
KC_TOKEN_ENDPOINT = "http://keycloak.url/realms/realm_of_the_project/protocol/openid-connect/token"

KC_CLIENT_ID=client_id_for_project
KC_CLIENT_SECRET=client_secret_for_project

KC_ADMIN_USERNAME=admin_user_for_project
KC_ADMIN_PASSWORD=admin_password_for_project
```
