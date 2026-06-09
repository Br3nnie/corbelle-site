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
    return json(res, 500, {
      success: false,
      message: "Loops API key is not configured",
    });
  }

  const body = req.body || {};
  const email = String(body.email || "").trim().toLowerCase();

  if (!isValidEmail(email)) {
    return json(res, 400, {
      success: false,
      message: "Please enter a valid email address",
    });
  }

  const loopsBody = {
    email,
    firstName: String(body.firstName || "").trim() || undefined,
    source: "Performance Ceiling Index",
    userGroup: "Performance Ceiling Index",
    pciJobTitle: String(body.jobTitle || "").trim() || undefined,
    pciScore: Number.isFinite(body.score) ? body.score : undefined,
    pciProfile: String(body.profile || "").trim() || undefined,
    pciStrategicAlignment: Number.isFinite(body.strategicAlignment)
      ? body.strategicAlignment
      : undefined,
    pciDecisionConfidence: Number.isFinite(body.decisionConfidence)
      ? body.decisionConfidence
      : undefined,
    pciTechGovernance: Number.isFinite(body.techGovernance)
      ? body.techGovernance
      : undefined,
    pciInfrastructure: Number.isFinite(body.infrastructure)
      ? body.infrastructure
      : undefined,
    pciDataOwnership: Number.isFinite(body.dataOwnership)
      ? body.dataOwnership
      : undefined,
    pciAiClarity: Number.isFinite(body.aiClarity) ? body.aiClarity : undefined,
    pciOptionality: Number.isFinite(body.optionality) ? body.optionality : undefined,
    pciRoiVisibility: Number.isFinite(body.roiVisibility)
      ? body.roiVisibility
      : undefined,
  };

  if (process.env.LOOPS_MAILING_LIST_ID) {
    loopsBody.mailingLists = {
      [process.env.LOOPS_MAILING_LIST_ID]: true,
    };
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
        message: loopsData.message || "Loops rejected the contact update",
      });
    }

    return json(res, 200, { success: true, id: loopsData.id });
  } catch (error) {
    return json(res, 502, {
      success: false,
      message: "Could not reach Loops",
    });
  }
};
