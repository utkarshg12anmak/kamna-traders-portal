document.addEventListener('DOMContentLoaded', () => {
  // 1) open
  document.querySelectorAll('[data-open]').forEach(btn => {
    const id = btn.dataset.open;
    const modal = document.getElementById(id);
    if (!modal) return;
    btn.addEventListener('click', () => modal.classList.add('active'));
  });

  // 2) close
  document.querySelectorAll('[data-close]').forEach(btn => {
    const id = btn.dataset.close;
    const modal = document.getElementById(id);
    if (!modal) return;
    btn.addEventListener('click', () => modal.classList.remove('active'));
  });

  // 3) click-outside
  document.addEventListener('click', e => {
    document.querySelectorAll('.modal-overlay.active').forEach(modal => {
      const box = modal.querySelector('.modal-box');
      const opener = document.querySelector(`[data-open="${modal.id}"]`);
      if (box && !box.contains(e.target) && !opener.contains(e.target)) {
        modal.classList.remove('active');
      }
    });
  });
});
