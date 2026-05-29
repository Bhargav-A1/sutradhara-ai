# 🇮🇳 DigiLocker OAuth 2.0 Integration Specification

This file serves as the strict API route contract for the Sutradhara AI platform to interact with Digital India's authentication layers.

## 🧭 OAuth 2.0 Authorization Flow Route

### Step A: Trigger User Consent Redirect
The frontend button redirects the user to this gateway to authorize Sutradhara AI to read their KYC data tokens.

* **HTTP Method:** `GET`
* **Sandbox Sandbox Target:** `https://sandbox.api-setu.in/oauth2/1/authorize`
* **URL Format Construct:**
    ```text
    [https://sandbox.api-setu.in/oauth2/1/authorize?response_type=code&client_id=SUTRA_AI_DEV_ID&redirect_uri=http://localhost:8080/callback&state=sutra_secure_session_xyz](https://sandbox.api-setu.in/oauth2/1/authorize?response_type=code&client_id=SUTRA_AI_DEV_ID&redirect_uri=http://localhost:8080/callback&state=sutra_secure_session_xyz)
    ```

### Expected Callback Redirection Capture
Once the user enters their OTP and clicks "Approve", the browser will route them back to our application server with a temporary exchange string:
```text
HTTP/1.1 302 Found
Location: http://localhost:8080/callback?code=b8a7c293de1a56f&state=sutra_secure_session_xyz