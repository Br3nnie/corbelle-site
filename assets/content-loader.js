(function () {
  const applyContent = (selector, value, mode) => {
    document.querySelectorAll(selector).forEach((element) => {
      if (mode === "html") {
        element.innerHTML = value;
      } else {
        element.textContent = value;
      }
    });
  };

  const loadPageContent = async () => {
    const page = document.body.dataset.contentPage;
    if (!page) return;

    const response = await fetch(`content/${page}.json`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load ${page} content`);

    const content = await response.json();

    Object.entries(content.text || {}).forEach(([key, value]) => {
      applyContent(`[data-copy="${key}"]`, value, "text");
    });

    Object.entries(content.html || {}).forEach(([key, value]) => {
      applyContent(`[data-copy="${key}"]`, value, "html");
    });

    Object.entries(content.attrs || {}).forEach(([key, attrs]) => {
      document.querySelectorAll(`[data-copy="${key}"]`).forEach((element) => {
        Object.entries(attrs).forEach(([name, value]) => {
          if (value === false || value === null) {
            element.removeAttribute(name);
          } else {
            element.setAttribute(name, value);
          }
        });
      });
    });
  };

  loadPageContent().catch(() => {
    document.documentElement.dataset.contentFallback = document.body.dataset.contentPage || "page";
  });
})();
