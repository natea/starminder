# Setting up GitHub Authentication

To enable "Login with GitHub" locally, you need to register a GitHub App and configure your environment variables.

## 1. Register a New GitHub App

1. Go to [GitHub Developer Settings > GitHub Apps > New GitHub App](https://github.com/settings/apps/new).
2. **GitHub App Name**: `Starminder (Local)` (or similar)
3. **Homepage URL**: `http://127.0.0.1:8000`
4. **Callback URL**: `http://127.0.0.1:8000/accounts/github/login/callback/`
   > **Important**: This URL must match exactly what `allauth` expects.
5. **Webhook URL**: You can uncheck "Active" for now, or use a dummy URL like `http://127.0.0.1:8000/webhook`.
6. **Permissions**:
   - You typically don't need special permissions just for login, but if you need to read starred repos, you might need to request `Metadata` (Read-only) and `Contents` (Read-only) or similar, depending on your app's logic.
   - For simple login, defaults are usually fine.
7. **User Authorization**:
   - [x] **Request user authorization (OAuth) during installation** (This is CRITICAL for login to work).
8. Click **Create GitHub App**.

## 2. Get Credentials

1. On the app's settings page, find **Client ID** near the top. Copy this.
2. Scroll down to **Client secrets** and click **Generate a new client secret**. Copy this value immediately (you won't see it again).

## 3. Configure Environment

1. Open your `.env` file.
2. Add or update the following lines:

```bash
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_SECRET=your_client_secret_here
```

## 4. Apply Configuration

Run the setup command to update the database with your new credentials:

```bash
just setup_social_app
```

Now restart your server (`just devserve`) and try logging in!
