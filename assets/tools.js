(function () {
  const text = (selector, value) => {
    const element = document.querySelector(selector);
    if (element && value) element.textContent = value;
  };

  const renderParagraphs = (selector, paragraphs) => {
    const container = document.querySelector(selector);
    if (!container || !Array.isArray(paragraphs)) return;
    container.innerHTML = "";
    paragraphs.forEach((copy) => {
      const paragraph = document.createElement("p");
      paragraph.textContent = copy;
      container.appendChild(paragraph);
    });
  };

  const renderToolCard = (tool) => {
    const isLive = tool.state === "live" && tool.url;
    const card = document.createElement(isLive ? "a" : "div");
    card.className = `tool-card ${isLive ? "tool-card-live" : "tool-card-soon"}`;

    if (isLive) {
      card.href = tool.url;
      card.target = "_blank";
      card.rel = "noopener";
    }

    const status = document.createElement("span");
    status.className = "tool-status";
    status.textContent = tool.status;

    const title = document.createElement("h3");
    title.textContent = tool.title;

    const description = document.createElement("p");
    description.textContent = tool.description;

    card.append(status, title, description);

    if (isLive) {
      const link = document.createElement("span");
      link.className = "tool-link";
      link.textContent = tool.linkLabel || "Open assessment";
      card.appendChild(link);
    }

    return card;
  };

  const loadToolsContent = async () => {
    const response = await fetch("content/tools.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Could not load tools content");
    const content = await response.json();

    text("[data-tools-hero-eyebrow]", content.hero && content.hero.eyebrow);
    text("[data-tools-hero-title]", content.hero && content.hero.title);
    renderParagraphs("[data-tools-hero-copy]", content.hero && content.hero.copy);

    text("[data-tools-intro-eyebrow]", content.intro && content.intro.eyebrow);
    text("[data-tools-intro-title]", content.intro && content.intro.title);
    text("[data-tools-intro-copy]", content.intro && content.intro.copy);

    const grid = document.querySelector("[data-tools-grid]");
    if (grid && Array.isArray(content.tools)) {
      grid.innerHTML = "";
      content.tools.forEach((tool) => grid.appendChild(renderToolCard(tool)));
    }

    text("[data-tools-note-copy]", content.note && content.note.copy);

    const cta = document.querySelector("[data-tools-note-cta]");
    if (cta && content.note) {
      cta.textContent = content.note.ctaLabel || cta.textContent;
      cta.href = content.note.ctaUrl || cta.href;
    }
  };

  loadToolsContent().catch(() => {
    document.documentElement.dataset.contentFallback = "tools";
  });
})();
