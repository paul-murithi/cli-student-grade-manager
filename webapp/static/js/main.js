document.addEventListener("DOMContentLoaded", () => {
  const countdown = document.getElementById("counter");

  document.getElementById("menuToggle")?.addEventListener("click", () => {
    document.querySelector(".nav-right")?.classList.toggle("open");
  });

  setTimeout(() => {
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach((msg) => msg.classList.add("inactive"));
  }, 5000);

  setTimeout(() => {
    countdown.classList.add("shrink");
  }, 250);
});
