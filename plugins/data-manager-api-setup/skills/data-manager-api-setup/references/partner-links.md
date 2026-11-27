# Partner Links

A partner link connects an advertiser account to a data partner account. The
data partner then manages audiences or events in the advertiser's account using
credentials for its **own** data partner account. For the full guide, see
[Partner links](https://developers.google.com/data-manager/api/devguides/accounts/partner-links.md.txt).

## Data partner workflow

Advertisers can also manage partner links in the Google Ads, Display & Video
360, or Google Ad Manager UI. Use `PartnerLinkService` when that isn't available
or when offering linking inside the partner's own application.

1.  **Get short-lived advertiser credentials** for a Google Account that's a
    user in the advertiser account, requesting only this scope:

    `https://www.googleapis.com/auth/datamanager.partnerlink`

    Build an OAuth flow in the partner's app. Use a **Web server** or **Web
    browser** OAuth client (not Desktop), following
    [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
    or
    [OAuth 2.0 for Client-side Web Applications](https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow).
2.  **Create the partner link** with the advertiser credentials. See
    [Create or delete a partner link](https://developers.google.com/data-manager/api/devguides/accounts/partner-links/create-partner-link.md.txt)
    for the request fields and samples.
3.  **Discard the advertiser credentials.** They're no longer needed.
4.  **For all later requests**, use credentials for a Google Account or service
    account with access to the **data partner account**.

## OAuth app verification

The `datamanager.partnerlink` scope is sensitive, so the partner's app must
complete OAuth app verification before advertisers authorize it. Otherwise,
advertisers see the unverified app screen.

For details on the verification process, see
[OAuth app verification](https://developers.google.com/data-manager/api/devguides/concepts/oauth-verification.md.txt).
