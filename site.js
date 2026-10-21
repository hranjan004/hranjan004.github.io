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
