document.addEventListener("DOMContentLoaded", () => {
  animateXPBars();
  animateProjectBars();
  initAchievementHovers();
  initUnlockPopup();
});


function animateXPBars() {
  document.querySelectorAll(".ds-xp-bar__fill").forEach(bar => {
    const target = bar.style.width;
    bar.style.width = "0%";
    setTimeout(() => { bar.style.width = target; }, 100);
  });
}

function animateProjectBars() {
  document.querySelectorAll(".ds-project-bar__fill").forEach(bar => {
    const target = bar.style.width;
    bar.style.width = "0%";
    setTimeout(() => { bar.style.width = target; }, 200);
  });
}


function initAchievementHovers() {
  document.querySelectorAll(".ds-achievement:not(.ds-achievement--locked)").forEach(card => {
    const rarityEl = card.querySelector(".ds-achievement__rarity");
    if (!rarityEl) return;

    const color = rarityEl.style.color;

    card.addEventListener("mouseenter", () => {
      card.style.borderColor = color;
      card.style.boxShadow = `0 0 12px ${color}40`;
    });

    card.addEventListener("mouseleave", () => {
      card.style.borderColor = "";
      card.style.boxShadow = "";
    });
  });
}


function initUnlockPopup() {
  const newlyUnlocked = document.querySelectorAll(".ds-achievement--newly-unlocked");
  if (newlyUnlocked.length === 0) return;

  let delay = 500;
  newlyUnlocked.forEach(card => {
    const name = card.querySelector(".ds-achievement__name")?.textContent?.trim();
    const icon = card.querySelector(".ds-achievement__icon i")?.className || "";
    setTimeout(() => showPopup(name, icon), delay);
    delay += 2000;
  });
}

function showPopup(name, iconClass) {
  const popup = document.createElement("div");
  popup.className = "ds-unlock-popup";
  popup.innerHTML = `
    <div class="ds-unlock-popup__inner">
      <i class="${iconClass}"></i>
      <div class="ds-unlock-popup__text">
        <span class="ds-unlock-popup__label">Achievement Unlocked</span>
        <span class="ds-unlock-popup__name">${name}</span>
      </div>
    </div>
  `;
  document.body.appendChild(popup);

  requestAnimationFrame(() => {
    popup.classList.add("ds-unlock-popup--visible");
  });

  setTimeout(() => {
    popup.classList.remove("ds-unlock-popup--visible");
    setTimeout(() => popup.remove(), 500);
  }, 3000);
}