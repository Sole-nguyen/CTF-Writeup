(() => {
  const k = 'uvt_debug';
  const btn = document.getElementById('btn');
  const out = document.getElementById('out');

  function render() {
    const v = localStorage.getItem(k) || '0';
    out.textContent = `localStorage['${k}'] = ${v}\n` +
      'This page does not read files directly. Check stage2/logs for the intended path.';
  }

  btn.addEventListener('click', () => {
    const v = localStorage.getItem(k) === '1' ? '0' : '1';
    localStorage.setItem(k, v);
    render();
  });

  render();
})();
