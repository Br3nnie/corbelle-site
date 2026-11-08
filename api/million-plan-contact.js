import { botCheck } from "./_altcha.js";
const LOOPS_CONTACT_UPDATE_URL = "https://app.loops.so/api/v1/contacts/update";

function json(res, statusCode, body) {
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(body));
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return json(res, 405, { success: false, message: "Method not allowed" });
  }

  if (!process.env.LOOPS_API_KEY) {
    return json(res, 500, { success: false, message: "Email capture is not configured" });
  }

  const body = req.body || {};
  const bot = botCheck(body);
  if (bot === "spam") return json(res, 200, { success: true });
  if (bot) return json(res, 400, { success: false, message: bot });
  const email = String(body.email || "").trim().toLowerCase();
  if (!isValidEmail(email)) {
    return json(res, 400, { success: false, message: "Please enter a valid email address." });
  }

  const loopsBody = {
    email,
    firstName: String(body.firstName || "").trim() || undefined,
    source: "Million-Pound Operating Plan",
    userGroup: "Million-Pound Operating Plan",
  };

  if (process.env.LOOPS_MAILING_LIST_ID) {
    loopsBody.mailingLists = { [process.env.LOOPS_MAILING_LIST_ID]: true };
  }
  Object.keys(loopsBody).forEach((key) => {
    if (loopsBody[key] === undefined) delete loopsBody[key];
  });

  try {
    const response = await fetch(LOOPS_CONTACT_UPDATE_URL, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${process.env.LOOPS_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loopsBody),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.success === false) {
      return json(res, response.status || 502, {
        success: false,
        message: data.message || "Email capture is temporarily unavailable.",
      });
    }
    return json(res, 200, { success: true, id: data.id });
  } catch {
    return json(res, 502, { success: false, message: "Email capture is temporarily unavailable." });
  }
}
