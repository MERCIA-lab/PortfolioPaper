const apiHost = ["localhost", "127.0.0.1"].includes(window.location.hostname)
  ? window.location.hostname
  : "localhost";
const apiProtocol = window.location.protocol === "https:" ? "https:" : "http:";
window.PORTFOLIO_API_BASE = `${apiProtocol}//${apiHost}:8000/api`;
