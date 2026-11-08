// Shared ALTCHA (proof-of-work "I'm not a robot") helpers.
// Files starting with "_" in /api are not deployed as routes.
import crypto from "node:crypto";

// Signing key: ALTCHA_HMAC_KEY if set in Vercel, otherwise derived from the existing
// LOOPS_API_KEY so no new secret is needed. Nothing secret lives in this file.
function signingKey() {
  if (process.env.ALTCHA_HMAC_KEY) return process.env.ALTCHA_HMAC_KEY;
  if (process.env.LOOPS_API_KEY) {
    return crypto.createHash("sha256").update("corbelle-altcha:" + process.env.LOOPS_API_KEY).digest("hex");
  }
  return null;
}

const MAX_NUMBER = 60000;
const TTL_SECONDS = 20 * 60;
const used = new Map(); // best-effort replay protection per warm instance

const sha256 = (s) => crypto.createHash("sha256").update(s).digest("hex");
const hmac = (key, s) => crypto.createHmac("sha256", key).update(s).digest("hex");

export function createChallenge() {
  const key = signingKey();
  if (!key) return null;
  const expires = Math.floor(Date.now() / 1000) + TTL_SECONDS;
  const salt = crypto.randomBytes(12).toString("hex") + "?expires=" + expires;
  const number = crypto.randomInt(0, MAX_NUMBER);
  const challenge = sha256(salt + number);
  return { algorithm: "SHA-256", challenge, maxnumber: MAX_NUMBER, salt, signature: hmac(key, challenge) };
}

export function verifySolution(payload) {
  try {
    const key = signingKey();
    if (!key || !payload || typeof payload !== "string") return false;
    const p = JSON.parse(Buffer.from(payload, "base64").toString("utf8"));
    if (p.algorithm !== "SHA-256") return false;
    const expires = Number(new URLSearchParams(String(p.salt).split("?")[1] || "").get("expires"));
    if (!expires || expires < Date.now() / 1000) return false;
    if (sha256(String(p.salt) + String(p.number)) !== p.challenge) return false;
    const expected = Buffer.from(hmac(key, p.challenge));
    const given = Buffer.from(String(p.signature));
    if (expected.length !== given.length || !crypto.timingSafeEqual(expected, given)) return false;
    if (used.has(p.challenge)) return false;
    used.set(p.challenge, expires);
    if (used.size > 5000) for (const [k, v] of used) if (v < Date.now() / 1000) used.delete(k);
    return true;
  } catch {
    return false;
  }
}

// Returns "spam" (silently ignore), an error message, or null if the request looks human.
export function botCheck(body) {
  if (body && String(body.website || "").trim()) return "spam"; // hidden honeypot field was filled
  if (!verifySolution(body && body.altcha)) return "Please tick the \"I'm not a robot\" check and try again.";
  return null;
}
