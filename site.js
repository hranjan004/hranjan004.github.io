(() => {
  const input = document.getElementById('essay-search');
  if (input) {
    const essays = [...document.querySelectorAll('[data-essay]')];
    input.addEventListener('input', () => {
      const terms = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      essays.forEach(essay => { essay.hidden = !terms.every(term => essay.dataset.essay.includes(term)); });
      const count = essays.filter(essay => !essay.hidden).length;
      document.getElementById('essay-count').textContent = `${count} of ${essays.length} essays and reflections`;
      document.getElementById('essay-empty').hidden = count !== 0;
    });
  }
  const search = document.getElementById('project-search');
  if (search) {
    const projects = [...document.querySelectorAll('[data-project]')];
    const status = document.getElementById('project-status');
    const stage = document.getElementById('project-stage');
    const filter = () => {
      const terms = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      projects.forEach(project => {
        project.hidden = !terms.every(term => project.dataset.project.includes(term))
          || (status.value !== '' && project.dataset.status !== status.value)
          || (stage.value !== '' && project.dataset.stage !== stage.value);
      });
      const count = projects.filter(project => !project.hidden).length;
      document.getElementById('project-count').textContent = `${count} of ${projects.length} projects`;
      document.getElementById('project-empty').hidden = count !== 0;
    };
    search.addEventListener('input', filter);
    status.addEventListener('change', filter);
    stage.addEventListener('change', filter);
  }
})();

// Motion is intentional: respect system preferences and stop work outside the viewport.
(() => {
  const diagrams = [...document.querySelectorAll('svg.topic-visual')];
  if (!diagrams.length) return;
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  let preference = null;
  try { preference = localStorage.getItem('portfolio-motion'); } catch (_) {}
  let enabled = preference ? preference === 'on' : !media.matches;
  const visible = new WeakSet();
  const buttons = [...document.querySelectorAll('[data-motion-toggle]')];
  function update(svg) {
    if (typeof svg.pauseAnimations !== 'function') return;
    if (enabled && !document.hidden && visible.has(svg)) svg.unpauseAnimations();
    else svg.pauseAnimations();
  }
  function sync() {
    document.body.dataset.motionState = enabled ? 'playing' : 'paused';
    buttons.forEach(button => {
      button.hidden = false;
      button.querySelector('[data-motion-label]').textContent = enabled ? 'Pause motion' : 'Play motion';
      button.querySelector('.motion-icon').textContent = enabled ? 'Ⅱ' : '▷';
    });
    diagrams.forEach(update);
  }
  diagrams.forEach(svg => {
    const rect = svg.getBoundingClientRect();
    if (rect.bottom > 0 && rect.top < innerHeight) visible.add(svg);
    if (!enabled && typeof svg.setCurrentTime === 'function') svg.setCurrentTime(0);
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
        update(entry.target);
      });
    }, { threshold: 0 });
    diagrams.forEach(svg => observer.observe(svg));
  } else diagrams.forEach(svg => visible.add(svg));
  buttons.forEach(button => button.addEventListener('click', () => {
    enabled = !enabled;
    preference = enabled ? 'on' : 'off';
    try { localStorage.setItem('portfolio-motion', preference); } catch (_) {}
    sync();
  }));
  media.addEventListener('change', () => { if (!preference) { enabled = !media.matches; sync(); } });
  document.addEventListener('visibilitychange', sync);
  sync();
})();
