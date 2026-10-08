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
