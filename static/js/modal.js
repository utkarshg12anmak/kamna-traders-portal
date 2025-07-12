document.addEventListener('DOMContentLoaded', () => {
  // OPEN
  document.querySelectorAll('[data-open]').forEach(btn => {
    const modal = document.getElementById(btn.dataset.open);
    if (modal) btn.addEventListener('click', () => modal.classList.add('active'));
  });

  // CLOSE
  document.querySelectorAll('[data-close]').forEach(btn => {
    const modal = document.getElementById(btn.dataset.close);
    if (modal) btn.addEventListener('click', () => modal.classList.remove('active'));
  });

  // CLICK-OUTSIDE
  document.addEventListener('click', e => {
    document.querySelectorAll('.modal-overlay.active').forEach(modal => {
      const box    = modal.querySelector('.modal-box');
      const opener = document.querySelector(`[data-open="${modal.id}"]`);
      if (box && !box.contains(e.target) && (!opener || !opener.contains(e.target))) {
        modal.classList.remove('active');
      }
    });
  });
});
