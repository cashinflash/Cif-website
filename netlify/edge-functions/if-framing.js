// Relax framing restrictions for the /if card-submission page ONLY, so it
// loads inside email / in-app browsers (e.g. Gmail's webview).
//
// The site's global headers (netlify.toml `for = "/*"`) send:
//     X-Frame-Options: SAMEORIGIN
//     Content-Security-Policy: ... frame-ancestors 'self' ...
// Both restrict framing to our own origin, so when an email's in-app
// browser embeds the page in a frame, Chrome refuses it with
// ERR_BLOCKED_BY_RESPONSE ("refused to connect").
//
// Per-path [[headers]] rules can't fix this: Netlify APPENDS a second
// value for nested paths instead of replacing, so the restrictive value
// still wins. This edge function runs after the static headers are
// applied (via context.next()) and reliably removes the framing
// restrictions from the final response for this route only — every other
// security header is left untouched.
//
// Path matching is declared in netlify.toml under [[edge_functions]].

export default async (request, context) => {
  const response = await context.next();

  // Remove the legacy framing header entirely.
  response.headers.delete("X-Frame-Options");

  // Strip only the `frame-ancestors` directive from the CSP, leaving the
  // rest of the policy (script-src, connect-src, etc.) intact.
  const csp = response.headers.get("Content-Security-Policy");
  if (csp) {
    const relaxed = csp.replace(/\s*frame-ancestors[^;]*;?/gi, "").trim();
    if (relaxed) {
      response.headers.set("Content-Security-Policy", relaxed);
    } else {
      response.headers.delete("Content-Security-Policy");
    }
  }

  return response;
};
