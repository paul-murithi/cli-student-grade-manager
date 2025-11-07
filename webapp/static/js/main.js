document.getElementById("menuToggle")?.addEventListener("click", () => {
  document.querySelector(".nav-right")?.classList.toggle("open");
});

// Remove flash messages after 5 seconds
setTimeout(() => {
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach((msg) => msg.remove());
}, 5000);
