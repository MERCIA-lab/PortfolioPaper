const API_BASE = window.PORTFOLIO_API_BASE.replace(/\/+$/, "");
const IMAGE_BASE = API_BASE.replace(/\/api$/, "");

function apiUrl(path) {
  return `${API_BASE}/${path.replace(/^\/+/, "")}`;
}

function csrfToken() {
  return document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("csrftoken="))
    ?.split("=")[1];
}

async function ensureCsrfToken() {
  if (csrfToken()) return;
  const response = await fetch(apiUrl("accounts/csrf/"), { credentials: "include" });
  if (!response.ok || !csrfToken()) throw new Error("Could not start a secure session. Check the backend API.");
}

async function apiRequest(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const bodyIsFormData = options.body instanceof FormData;
  if (options.body && !bodyIsFormData && typeof options.body !== "string") {
    headers.set("Content-Type", "application/json");
    options.body = JSON.stringify(options.body);
  }
  if (!["GET", "HEAD"].includes((options.method || "GET").toUpperCase())) {
    await ensureCsrfToken();
    const token = csrfToken();
    if (token) headers.set("X-CSRFToken", decodeURIComponent(token));
  }
  const response = await fetch(apiUrl(path), {
    ...options,
    headers,
    credentials: "include",
  });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();
  if (!response.ok) {
    const detail = typeof payload === "string"
      ? payload
      : payload.detail || Object.entries(payload).map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(", ") : value}`).join(" ");
    const error = new Error(detail || `Request failed (${response.status}).`);
    error.status = response.status;
    throw error;
  }
  return payload;
}

function showStatus(element, message, isError = false) {
  element.textContent = message;
  element.classList.toggle("is-error", isError);
}

function escapeText(value) {
  return String(value ?? "");
}

function portfolioHref(portfolio) {
  return `portfolio.html?slug=${encodeURIComponent(portfolio.slug)}`;
}

function photoUrl(path) {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  return `${IMAGE_BASE}${path.startsWith("/") ? "" : "/"}${path}`;
}

function safeExternalUrl(url) {
  try {
    const parsed = new URL(url);
    return ["http:", "https:"].includes(parsed.protocol) ? parsed.href : "";
  } catch {
    return "";
  }
}

function initials(name) {
  return escapeText(name)
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

function createPortfolioCard(portfolio) {
  const link = document.createElement("a");
  link.className = "portfolio-card";
  link.href = portfolioHref(portfolio);

  const imagePath = photoUrl(portfolio.photo);
  if (imagePath) {
    const image = document.createElement("img");
    image.className = "portfolio-photo";
    image.src = imagePath;
    image.alt = `${escapeText(portfolio.full_name)} portrait`;
    image.loading = "lazy";
    link.append(image);
  } else {
    const placeholder = document.createElement("span");
    placeholder.className = "portfolio-initials";
    placeholder.textContent = initials(portfolio.full_name);
    link.append(placeholder);
  }

  const info = document.createElement("span");
  info.className = "portfolio-info";
  const name = document.createElement("strong");
  name.textContent = escapeText(portfolio.full_name);
  const role = document.createElement("small");
  role.textContent = escapeText(portfolio.job_title);
  info.append(name, role);
  if (portfolio.skills?.length) {
    const tags = document.createElement("span");
    tags.className = "portfolio-tags";
    portfolio.skills.slice(0, 3).forEach((skill) => {
      const tag = document.createElement("span");
      tag.textContent = escapeText(skill.name);
      tags.append(tag);
    });
    info.append(tags);
  }
  link.append(info);
  return link;
}

async function getPublicPortfolios() {
  const result = await apiRequest("directory/");
  const list = Array.isArray(result) ? result : result.results;
  if (!Array.isArray(list)) throw new Error("The directory API returned an unsupported response.");
  return list;
}

function setupMobileMenu() {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".mobile-nav");
  if (!toggle || !nav) return;
  toggle.addEventListener("click", () => {
    const open = nav.hidden;
    nav.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
    nav.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open navigation");
  }));
}

function setupDirectory(root = document) {
  const list = root.querySelector("[data-portfolio-list]");
  if (!list) return;

  const status = root.querySelector("[data-status]");
  const filters = root.querySelector(".tag-filters");
  const searchForm = root.querySelector(".directory-search");
  const searchInput = searchForm?.querySelector('input[type="search"]');
  let portfolios = [];
  let selectedTag = "";
  let query = "";

  const render = () => {
    const visible = portfolios.filter((portfolio) => {
      const text = `${portfolio.full_name} ${portfolio.job_title} ${portfolio.location || ""} ${(portfolio.skills || []).map((skill) => skill.name).join(" ")}`.toLowerCase();
      const hasTag = !selectedTag || (portfolio.skills || []).some((skill) => skill.name.toLowerCase() === selectedTag);
      return hasTag && text.includes(query);
    });
    list.replaceChildren(...visible.map(createPortfolioCard));
    if (visible.length) {
      showStatus(status, "");
    } else {
      showStatus(status, portfolios.length ? "No portfolios match. Try another search or skill." : "No public portfolios have been published yet.");
    }
  };

  const setFilters = () => {
    if (!filters) return;
    const tags = [...new Set(portfolios.flatMap((portfolio) => (portfolio.skills || []).map((skill) => skill.name.trim()).filter(Boolean)))].sort((a, b) => a.localeCompare(b));
    const buttons = [""].concat(tags).map((tag) => {
      const button = document.createElement("button");
      button.className = "tag-filter";
      button.type = "button";
      button.textContent = tag || "All portfolios";
      button.setAttribute("aria-pressed", String(selectedTag === tag.toLowerCase()));
      button.addEventListener("click", () => {
        selectedTag = tag.toLowerCase();
        filters.querySelectorAll("button").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
        render();
      });
      return button;
    });
    filters.replaceChildren(...buttons);
  };

  searchForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    query = searchInput.value.trim().toLowerCase();
    render();
  });
  searchInput?.addEventListener("input", () => {
    query = searchInput.value.trim().toLowerCase();
    render();
  });

  getPublicPortfolios()
    .then((results) => {
      portfolios = results;
      setFilters();
      render();
    })
    .catch((error) => showStatus(status, `Could not load portfolios: ${error.message}`, true));
}

function setupAuthForm() {
  const form = document.querySelector("[data-auth-form]");
  if (!form) return;
  const status = form.querySelector(".form-error");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;
    showStatus(status, "Please wait…");
    const values = Object.fromEntries(new FormData(form));
    const isRegister = form.dataset.authForm === "register";
    try {
      if (isRegister) {
        await apiRequest("accounts/register/", { method: "POST", body: values });
        const params = new URLSearchParams(location.search);
        location.href = `login.html?registered=1&next=${encodeURIComponent(params.get("next") || "form.html")}`;
        return;
      }
      await apiRequest("accounts/login/", {
        method: "POST",
        body: { email: values.email, password: values.password },
      });
      const next = new URLSearchParams(location.search).get("next");
      location.href = next && next.startsWith("/") === false && !next.includes(":")
        ? next
        : "form.html";
    } catch (error) {
      showStatus(status, error.message, true);
      button.disabled = false;
    }
  });

  if (form.dataset.authForm === "login" && new URLSearchParams(location.search).has("registered")) {
    showStatus(status, "Your account is ready. Sign in to continue.");
  }
}

function inputField(label, name, options = {}) {
  const wrapper = document.createElement("label");
  wrapper.className = "field";
  if (options.full) wrapper.classList.add("full");
  const title = document.createElement("span");
  title.textContent = label;
  let input;
  if (options.multiline) {
    input = document.createElement("textarea");
  } else {
    input = document.createElement("input");
    input.type = options.type || "text";
  }
  input.name = name;
  if (options.required) input.required = true;
  if (options.placeholder) input.placeholder = options.placeholder;
  if (options.step) input.step = options.step;
  wrapper.append(title, input);
  return wrapper;
}

function addRepeatItem(container, kind) {
  const definitions = {
    experience: [
      ["Company", "company", true],
      ["Role", "role", true],
      ["Location", "location"],
      ["Start date", "start_date"],
      ["End date", "end_date"],
      ["Description", "description", false, true],
    ],
    education: [
      ["School", "school", true],
      ["Degree", "degree", true],
      ["Start year", "start_year"],
      ["End year", "end_year"],
    ],
    projects: [
      ["Project title", "title", true],
      ["Category", "category"],
      ["Project link", "link"],
      ["Technologies", "technologies"],
      ["Description", "description", false, true],
    ],
    skills: [
      ["Skill or tag", "name", true],
      ["Level (1-5)", "level"],
    ],
  };
  const item = document.createElement("div");
  item.className = "repeat-item";
  const heading = document.createElement("div");
  heading.className = "repeat-heading";
  const title = document.createElement("h3");
  title.textContent = `${kind[0].toUpperCase()}${kind.slice(1)} item`;
  const remove = document.createElement("button");
  remove.className = "remove-item";
  remove.type = "button";
  remove.textContent = "Remove";
  remove.addEventListener("click", () => item.remove());
  heading.append(title, remove);
  const fields = document.createElement("div");
  fields.className = "form-grid";
  item.append(heading);
  definitions[kind].forEach(([label, name, required, multiline]) => {
    const field = inputField(label, name, { required, multiline, full: multiline });
    const control = field.querySelector("input, textarea");
    if (kind === "skills" && name === "level") {
      control.type = "number";
      control.min = "1";
      control.max = "5";
      control.value = "3";
      control.required = true;
    }
    if (name === "link") control.type = "url";
    fields.append(field);
  });
  item.append(fields);
  container.append(item);
  return item;
}

function setupPortfolioForm() {
  const form = document.querySelector("[data-portfolio-form]");
  if (!form) return;
  const status = form.querySelector(".form-error");
  const accountStatus = document.querySelector("[data-current-user]");
  const photoInput = form.querySelector('[name="photo"]');
  const photoPreview = form.querySelector(".photo-preview img");
  const photoPreviewLabel = form.querySelector(".photo-preview-label");

  photoInput.addEventListener("change", () => {
    const file = photoInput.files[0];
    if (!file) {
      photoPreview.removeAttribute("src");
      photoPreview.hidden = true;
      photoPreviewLabel.hidden = false;
      return;
    }
    if (!file.type.startsWith("image/")) {
      photoInput.value = "";
      showStatus(status, "Choose an image file for your profile photo.", true);
      return;
    }
    photoPreview.src = URL.createObjectURL(file);
    photoPreview.hidden = false;
    photoPreviewLabel.hidden = true;
  });

  form.querySelectorAll("[data-add-item]").forEach((button) => {
    button.addEventListener("click", () => addRepeatItem(form.querySelector(`[data-repeat="${button.dataset.addItem}"]`), button.dataset.addItem));
  });
  ["experience", "education", "skills", "projects"].forEach((kind) => {
    addRepeatItem(form.querySelector(`[data-repeat="${kind}"]`), kind);
  });

  apiRequest("accounts/user/")
    .then(async (user) => {
      accountStatus.textContent = `Signed in as ${user.email}`;
      try {
        const portfolio = await apiRequest("portfolio/");
        ["full_name", "job_title", "summary", "phone", "email", "location", "github", "github_summary"].forEach((name) => {
          form.elements[name].value = portfolio[name] || "";
        });
        form.elements.is_public.checked = portfolio.is_public;
        if (portfolio.photo) {
          photoPreview.src = photoUrl(portfolio.photo);
          photoPreview.hidden = false;
          photoPreviewLabel.hidden = true;
        }
        ["experience", "education", "skills", "projects"].forEach((kind) => {
          const values = portfolio[kind] || [];
          if (!values.length) return;
          const container = form.querySelector(`[data-repeat="${kind}"]`);
          container.replaceChildren();
          values.forEach((value) => {
            const item = addRepeatItem(container, kind);
            Object.entries(value).forEach(([key, fieldValue]) => {
              const control = item.querySelector(`[name="${key}"]`);
              if (control && fieldValue !== null) control.value = fieldValue;
            });
          });
        });
        form.querySelector('[type="submit"]').textContent = "Update portfolio";
        document.querySelector(".page-title").textContent = "Update your portfolio.";
      } catch (error) {
        if (error.status !== 404) throw error;
      }
      form.hidden = false;
    })
    .catch((error) => {
      if ([401, 403].includes(error.status)) {
        const next = encodeURIComponent("form.html");
        location.replace(`login.html?next=${next}`);
        return;
      }
      showStatus(accountStatus, `Could not connect to your account: ${error.message}`, true);
    });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;
    showStatus(status, "Saving portfolio…");
    try {
      const body = new FormData();
      ["full_name", "job_title", "summary", "phone", "email", "location", "github", "github_summary"].forEach((name) => {
        body.append(name, form.elements[name].value.trim());
      });
      body.append("is_public", String(form.elements.is_public.checked));
      if (photoInput.files[0]) body.append("photo", photoInput.files[0]);
      ["experience", "education", "skills", "projects"].forEach((kind) => {
        const keys = [...new Set([...form.querySelectorAll(`[data-repeat="${kind}"] input, [data-repeat="${kind}"] textarea`)].map((control) => control.name))];
        const items = [...form.querySelectorAll(`[data-repeat="${kind}"] .repeat-item`)];
        items.forEach((item, index) => {
          const hasContent = keys.some((key) => item.querySelector(`[name="${key}"]`)?.value.trim());
          if (!hasContent) return;
          keys.forEach((key) => {
            const control = item.querySelector(`[name="${key}"]`);
            if (control?.value.trim()) body.append(`${kind}[${index}]${key}`, control.value.trim());
          });
        });
      });
      const portfolio = await apiRequest("portfolio/", { method: "POST", body });
      if (portfolio.is_public && portfolio.slug) {
        location.href = `portfolio.html?slug=${encodeURIComponent(portfolio.slug)}`;
        return;
      }
      showStatus(status, "Portfolio saved privately. You can continue editing it here.");
      button.disabled = false;
    } catch (error) {
      showStatus(status, error.message, true);
      button.disabled = false;
    }
  });
}

function setProfileSection(container, title, content) {
  if (!content) return;
  const section = document.createElement("section");
  section.className = "profile-section";
  const heading = document.createElement("h2");
  heading.textContent = title;
  section.append(heading, content);
  container.append(section);
}

function textParagraph(value) {
  const paragraph = document.createElement("p");
  paragraph.textContent = escapeText(value);
  return paragraph;
}

function descriptionContent(value) {
  const lines = escapeText(value).split(/\r?\n/).map((line) => line.replace(/^\s*[-•]\s*/, "").trim()).filter(Boolean);
  if (lines.length <= 1) return textParagraph(lines[0] || "");
  const list = document.createElement("ul");
  lines.forEach((line) => {
    const item = document.createElement("li");
    item.textContent = line;
    list.append(item);
  });
  return list;
}

function entryBlock(title, subtitle, period, description) {
  const article = document.createElement("article");
  article.className = "profile-entry";
  const head = document.createElement("div");
  head.className = "profile-entry-heading";
  const name = document.createElement("strong");
  name.textContent = escapeText(title);
  head.append(name);
  if (period) {
    const time = document.createElement("time");
    time.textContent = escapeText(period);
    head.append(time);
  }
  article.append(head);
  if (subtitle) {
    const sub = document.createElement("p");
    sub.className = "profile-entry-subtitle";
    sub.textContent = escapeText(subtitle);
    article.append(sub);
  }
  if (description) article.append(descriptionContent(description));
  return article;
}

function renderProfile(portfolio) {
  const paper = document.querySelector(".profile-paper");
  document.title = `${portfolio.full_name} — Portfolio Paper`;
  const photo = paper.querySelector(".profile-photo");
  if (portfolio.photo) {
    photo.src = photoUrl(portfolio.photo);
    photo.alt = `${portfolio.full_name} profile photo`;
    photo.hidden = false;
  }
  paper.querySelector(".profile-heading h1").textContent = escapeText(portfolio.full_name);
  paper.querySelector(".profile-heading .profile-role").textContent = escapeText(portfolio.job_title);
  const contact = paper.querySelector(".profile-contact");
  contact.replaceChildren();
  [portfolio.location, portfolio.email, portfolio.phone].filter(Boolean).forEach((value, index, values) => {
    if (index) contact.append(document.createTextNode("  |  "));
    contact.append(document.createTextNode(escapeText(value)));
  });
  if (portfolio.email) {
    contact.replaceChildren();
    const values = [portfolio.location, portfolio.email, portfolio.phone].filter(Boolean);
    values.forEach((value, index) => {
      if (index) contact.append(document.createTextNode("  |  "));
      if (value === portfolio.email) {
        const link = document.createElement("a");
        link.href = `mailto:${encodeURIComponent(value)}`;
        link.textContent = value;
        contact.append(link);
      } else {
        contact.append(document.createTextNode(escapeText(value)));
      }
    });
  }
  const github = safeExternalUrl(portfolio.github);
  if (github) {
    if (contact.childNodes.length) contact.append(document.createTextNode("  |  "));
    const link = document.createElement("a");
    link.href = github;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = github.replace(/^https?:\/\//, "").replace(/\/$/, "");
    contact.append(link);
  }

  const sections = paper.querySelector(".profile-content");
  sections.replaceChildren();
  setProfileSection(sections, "SUMMARY", portfolio.summary ? textParagraph(portfolio.summary) : null);
  const experience = document.createElement("div");
  (portfolio.experience || []).forEach((item) => {
    experience.append(entryBlock(`${item.role} — ${item.company}`, item.location, [item.start_date, item.end_date].filter(Boolean).join(" – "), item.description));
  });
  setProfileSection(sections, "WORK EXPERIENCE", experience.childElementCount ? experience : null);
  const projects = document.createElement("div");
  (portfolio.projects || []).forEach((item) => {
    const projectDetails = [item.category, item.technologies].filter(Boolean).join(" · ");
    const entry = entryBlock(item.title, projectDetails, "", item.description);
    const projectUrl = safeExternalUrl(item.link);
    if (projectUrl) {
      const link = document.createElement("a");
      link.href = projectUrl;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = "View project";
      entry.append(link);
    }
    projects.append(entry);
  });
  setProfileSection(sections, "FEATURED PROJECTS", projects.childElementCount ? projects : null);
  setProfileSection(sections, "GITHUB ACTIVITY", portfolio.github_summary ? textParagraph(portfolio.github_summary) : null);
  const education = document.createElement("div");
  (portfolio.education || []).forEach((item) => {
    education.append(entryBlock(item.degree, item.school, [item.start_year, item.end_year].filter(Boolean).join(" – "), ""));
  });
  setProfileSection(sections, "EDUCATION", education.childElementCount ? education : null);
  if (portfolio.skills?.length) {
    const skills = document.createElement("div");
    skills.className = "profile-skills";
    portfolio.skills.forEach((item) => {
      const tag = document.createElement("span");
      tag.textContent = escapeText(item.name);
      skills.append(tag);
    });
    setProfileSection(sections, "SKILLS & TAGS", skills);
  }
  paper.hidden = false;
}

async function setupProfilePage() {
  const slug = new URLSearchParams(location.search).get("slug");
  const status = document.querySelector("[data-status]");
  if (!slug) {
    showStatus(status, "This portfolio link is missing its profile name.", true);
    return;
  }
  try {
    const portfolio = await apiRequest(`directory/${encodeURIComponent(slug)}/`);
    renderProfile(portfolio);
    showStatus(status, "");
  } catch (error) {
    showStatus(status, `Could not load this portfolio: ${error.message}`, true);
  }
}

setupMobileMenu();
setupDirectory();
setupAuthForm();
setupPortfolioForm();
if (document.body.dataset.page === "profile") setupProfilePage();
document.querySelector("[data-print]")?.addEventListener("click", () => window.print());
document.querySelector("[data-logout]")?.addEventListener("click", async () => {
  const button = document.querySelector("[data-logout]");
  button.disabled = true;
  try {
    await apiRequest("accounts/logout/", { method: "POST", body: {} });
    location.href = "index.html";
  } catch (error) {
    button.disabled = false;
    showStatus(document.querySelector(".form-error"), error.message, true);
  }
});
