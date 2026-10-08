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

(() => {
  const input = document.getElementById('essay-search');
  if (!input) return;
  const essays = [...document.querySelectorAll('[data-essay]')];
  input.addEventListener('input', () => {
    const terms = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    essays.forEach(essay => { essay.hidden = !terms.every(term => essay.dataset.essay.includes(term)); });
    const count = essays.filter(essay => !essay.hidden).length;
    document.getElementById('essay-count').textContent = `${count} of ${essays.length} essays and reflections`;
    document.getElementById('essay-empty').hidden = count !== 0;
  });
})();
