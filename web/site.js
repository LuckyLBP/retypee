"use strict";

/* Closes the tools menu when you click elsewhere or press Escape. */
document.addEventListener("click", (e) => {
  const open = document.querySelector("details.menu[open]");
  if (open && !open.contains(e.target)) open.removeAttribute("open");
});
document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  const open = document.querySelector("details.menu[open]");
  if (open) {
    open.removeAttribute("open");
    open.querySelector("summary").focus();
  }
});
