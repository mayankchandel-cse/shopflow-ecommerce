// ShopFlow — small front-end helpers (no framework needed)
document.addEventListener("DOMContentLoaded", function () {
  // Auto-hide flash messages after 5 seconds
  document.querySelectorAll(".flash").forEach(function (el) {
    setTimeout(function () { el.style.display = "none"; }, 5000);
  });
});
