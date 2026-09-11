(() => {
  const canvas = document.getElementById('flow-field');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0, phase = 0, last = 0, visible = true;
  let width = 0, height = 0;
  function draw() {
    ctx.clearRect(0, 0, width, height);
    const size = Math.min(width, height) * .38;
    for (let line = 0; line < 32; line++) {
      ctx.beginPath();
      for (let step = 0; step <= 160; step++) {
        const angle = step / 160 * Math.PI * 2;
        const twist = phase * .25 + line * .045;
        const radius = size * (1 + .17 * Math.sin(angle * 3 + twist));
        const x = width * .52 + Math.cos(angle + twist) * radius;
        const y = height * .5 + Math.sin(angle) * radius * Math.cos(line * .048 + phase * .15);
        if (!step) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = `rgba(${130 + line * 2},${170 + line},255,${.12 + line / 140})`;
      ctx.lineWidth = .8;
      ctx.stroke();
    }
  }
  function loop(now) {
    frame = 0;
    if (!visible || document.hidden) return;
    if (last) phase += Math.min(now - last, 50) * .00025;
    last = now;
    draw();
    frame = requestAnimationFrame(loop);
  }
  function sync() {
    cancelAnimationFrame(frame); frame = 0; last = 0;
    draw();
    if (visible && !document.hidden) frame = requestAnimationFrame(loop);
  }
  function resize() {
    const bounds = canvas.getBoundingClientRect();
    width = bounds.width; height = bounds.height;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0); draw();
  }
  document.addEventListener('visibilitychange', sync);
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }).observe(canvas);
  const reveals = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      if (!preference.matches) entry.target.classList.add('revealed');
      reveals.unobserve(entry.target);
    });
  }, {threshold: .08});
  document.querySelectorAll('.project, .role, .edu article').forEach(el => reveals.observe(el));
  resize(); sync();
})();
