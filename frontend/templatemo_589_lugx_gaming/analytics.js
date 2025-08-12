const ANALYTICS_URL =
  location.hostname === 'localhost'
    ? 'http://localhost:8083/track'   // local browser via SSH tunnel
    : 'http://192.168.49.2:30020/track'; // direct access from inside EC2 (Minikube IP + NodePort)
function sendEvent(event_type) {
  fetch(ANALYTICS_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ event_type })
  }).catch(err => console.error("Analytics error:", err));
}

// Track page view
window.addEventListener("load", () => sendEvent("page_view"));

// Track button clicks
document.addEventListener("click", (e) => {
  if (e.target.tagName === "BUTTON" || e.target.classList.contains("button")) {
    sendEvent("button_click");
  }
});

// Track scroll depth
window.addEventListener("scroll", () => {
  const y = window.scrollY;
  if (y > 100) sendEvent("scroll_depth_100");
  if (y > 500) sendEvent("scroll_depth_500");
});
