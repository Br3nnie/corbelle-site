import { createChallenge } from "./_altcha.js";

export default function handler(req, res) {
  const challenge = createChallenge();
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
  res.statusCode = challenge ? 200 : 500;
  res.end(JSON.stringify(challenge || { error: "Robot check is not configured" }));
}
