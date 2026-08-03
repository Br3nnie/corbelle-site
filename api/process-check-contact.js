const LOOPS_CONTACT_UPDATE_URL = "https://app.loops.so/api/v1/contacts/update";
const LOOPS_TRANSACTIONAL_URL = "https://app.loops.so/api/v1/transactional";

const RESULTS = {
  "The Hidden Drain": {
    summary: "The process is hurting performance, but its boundary, owner and failure pattern are still too blurred for a solution decision.",
    consequence: "Workarounds continue because nobody owns the whole journey. Improvement efforts risk fixing one step while moving cost or delay somewhere else.",
    actions: ["Write the process trigger and final outcome in one sentence.", "Name one accountable owner for the whole flow—not each individual task.", "Follow three real cases end to end and mark every wait, hand-off and correction."],
  },
  "The Cost Blind Spot": {
    summary: "You can see where the process hurts, but the commercial case is still built on frustration rather than an agreed baseline.",
    consequence: "The problem keeps losing to visible projects because its cost is spread across salaries, delays, rework and missed capacity. Any promised return will be easy to challenge.",
    actions: ["Validate the weekly hours with the people doing the work.", "Separate capacity value, cashable cost, delay and revenue impact.", "Agree the one operational measure that must improve for action to count as success."],
  },
  "The Unproven Fix": {
    summary: "The process deserves attention and a possible fix is forming, but the assumptions behind that fix have not yet earned confidence.",
    consequence: "A persuasive demo can outrun process fit, usable data and real user needs. The organisation may automate waste, choose the wrong tool or approve benefits that cannot be measured.",
    actions: ["Turn the pain into one specific use case with a named user and outcome.", "List the three assumptions most likely to destroy value.", "Design the smallest test that produces evidence for a stop, reshape or proceed decision."],
  },
  "The Stalled Change": {
    summary: "The organisation has moved beyond diagnosis, but ownership, evidence, data or delivery decisions are stopping the change from reaching live work.",
    consequence: "Pilot cost and leadership attention accumulate while the old process keeps running. Ambiguity makes ‘still learning’ a permanent status instead of a decision.",
    actions: ["Name one person accountable for the next decision and its date.", "Write explicit stop, fix and proceed thresholds for the current test.", "Resolve the single dependency that blocks a live workflow—not a better demo."],
  },
  "The Double-Running Trap": {
    summary: "The new route exists, but the old process is still winning often enough that much of the cost remains.",
    consequence: "The organisation pays twice: for the solution and for the manual route beside it. Low trust and uneven use can make a sound intervention look like a technology failure.",
    actions: ["Measure adoption by role, workflow step and frequency—not total logins.", "Ask five users and five non-users where the old route still wins.", "Remove one major friction point and retire one old step within 30 days."],
  },
};

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

  if (!process.env.LOOPS_PROCESS_CHECK_TRANSACTIONAL_ID) {
    return json(res, 500, { success: false, message: "Results email is not configured" });
  }

  const body = req.body || {};
  const email = String(body.email || "").trim().toLowerCase();
  if (!isValidEmail(email)) {
    return json(res, 400, { success: false, message: "Please enter a valid email address." });
  }

  const loopsBody = {
    email,
    firstName: String(body.firstName || "").trim() || undefined,
    source: "Process Pain Check",
    userGroup: "Process Pain Check",
  };

  if (process.env.LOOPS_MAILING_LIST_ID) {
    loopsBody.mailingLists = { [process.env.LOOPS_MAILING_LIST_ID]: true };
  }

  Object.keys(loopsBody).forEach((key) => {
    if (loopsBody[key] === undefined) delete loopsBody[key];
  });

  try {
    const loopsResponse = await fetch(LOOPS_CONTACT_UPDATE_URL, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${process.env.LOOPS_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loopsBody),
    });
    const loopsData = await loopsResponse.json().catch(() => ({}));
    if (!loopsResponse.ok || loopsData.success === false) {
      return json(res, loopsResponse.status || 502, {
        success: false,
        message: loopsData.message || "Email capture is temporarily unavailable.",
      });
    }
    const diagnosis = String(body.diagnosis || "").trim();
    const result = RESULTS[diagnosis];
    if (!result) return json(res, 400, { success: false, message: "The assessment result could not be recognised." });
    const money = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", maximumFractionDigits: 0 });
    const annual = Number(body.annualCapacityValue), low = Number(body.recoverableLow), high = Number(body.recoverableHigh);
    const emailResponse = await fetch(LOOPS_TRANSACTIONAL_URL, {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.LOOPS_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        transactionalId: process.env.LOOPS_PROCESS_CHECK_TRANSACTIONAL_ID,
        dataVariables: {
          firstName: String(body.firstName || "").trim(), processName: String(body.process || "").trim(), diagnosis,
          diagnosisSummary: result.summary,
          annualCapacityValue: money.format(Number.isFinite(annual) ? annual : 0),
          recoverableRange: `${money.format(Number.isFinite(low) ? low : 0)}–${money.format(Number.isFinite(high) ? high : 0)}`,
          consequence: result.consequence, actionOne: result.actions[0], actionTwo: result.actions[1], actionThree: result.actions[2],
          gameplanUrl: "https://www.corbelle.ai/usecasegameplan",
        },
      }),
    });
    const emailData = await emailResponse.json().catch(() => ({}));
    if (!emailResponse.ok || emailData.success === false) return json(res, emailResponse.status || 502, { success: false, message: emailData.message || "Your results email could not be sent." });
    return json(res, 200, { success: true });
  } catch {
    return json(res, 502, { success: false, message: "Email capture is temporarily unavailable." });
  }
}
