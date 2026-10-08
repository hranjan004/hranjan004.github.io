(() => {
  const filters = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('[data-group]');
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.group !== button.dataset.filter; });
    const count = [...cards].filter(card => !card.hidden).length;
    const status = document.getElementById('filter-status');
    if (status) status.textContent = `${count} featured projects shown`;
  }));
})();
