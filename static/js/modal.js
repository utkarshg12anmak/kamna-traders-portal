// static/js/modal.js
document.addEventListener('DOMContentLoaded', () => {
  // delegate open buttons by [data-open]
  document.querySelectorAll('[data-open]').forEach(btn => {
    const target = btn.dataset.open;
    btn.addEventListener('click', () => {
      document.getElementById(target).classList.add('active');
    });
  });

  // delegate close buttons by [data-close]
  document.querySelectorAll('[data-close]').forEach(btn => {
    const target = btn.dataset.close;
    btn.addEventListener('click', () => {
      document.getElementById(target).classList.remove('active');
    });
  });

  // Close when clicking on the backdrop itself
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      // only if the click wasn’t inside the modal-box
      if (e.target === overlay) {
        overlay.classList.remove('active');
      }
    });
  });
});  