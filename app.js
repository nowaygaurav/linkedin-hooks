// Screen-only behaviour for the web version: autosave fields, tick boxes,
// fit pages to phones, and build a filled-in PDF in the browser.
(() => {
  const KEY = 'hooks-guide-v1';
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* private mode: still works, just no autosave */ } };

  document.querySelectorAll('[data-save]').forEach(el => {
    const k = el.dataset.save;
    if (saved[k]) el.value = saved[k];
    el.addEventListener('input', () => { saved[k] = el.value; save(); });
  });
  document.querySelectorAll('[data-check]').forEach(li => {
    const k = li.dataset.check;
    if (saved[k]) li.classList.add('on');
    li.addEventListener('click', () => { li.classList.toggle('on'); saved[k] = li.classList.contains('on'); save(); });
  });

  // shrink the 1080px pages to fit the screen (print ignores this, see style.css)
  const root = document.documentElement;
  function fit() {
    const z = Math.min(1, (root.clientWidth - 16) / 1080);
    root.style.setProperty('--fit', z);
    root.style.setProperty('--unfit', Math.min(1 / z, 1.8));  // keeps the bar tappable
  }
  fit();
  addEventListener('resize', fit);

  const load = src => new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = src; s.onload = res; s.onerror = rej;
    document.head.appendChild(s);
  });

  async function makePdf(btn, opts = {}) {
    const label = btn.textContent;
    btn.disabled = true;
    const overlays = [];
    try {
      btn.textContent = 'getting ready…';
      if (!window.html2canvas) await load('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
      if (!window.jspdf) await load('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
      await document.fonts.ready;

      // swap every field for plain text so the capture shows what they wrote
      root.classList.add('capturing');
      document.querySelectorAll('[data-save]').forEach(el => {
        const d = document.createElement('div');
        d.className = el.className + ' filled';
        d.textContent = el.value;
        el.after(d);
        overlays.push(d);
      });
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));

      const pages = [...document.querySelectorAll('.page')];
      const kept = [];
      const pdf = new window.jspdf.jsPDF({ unit: 'pt', format: [1080, 1350], orientation: 'portrait', compress: true });
      for (let i = 0; i < pages.length; i++) {
        btn.textContent = `making it… ${i + 1}/${pages.length}`;
        const pg = pages[i];
        const canvas = await window.html2canvas(pg, {
          scale: 1.5, useCORS: true, logging: false, backgroundColor: null,
          windowWidth: 1080, scrollX: -window.scrollX, scrollY: -window.scrollY,
        });
        if ((opts.keep || []).includes(i + 1)) kept.push(canvas.toDataURL('image/jpeg', 0.8));
        if (i) pdf.addPage([1080, 1350], 'portrait');
        pdf.addImage(canvas.toDataURL('image/jpeg', 0.9), 'JPEG', 0, 0, 1080, 1350);
        // keep the links clickable in the image PDF
        const P = pg.getBoundingClientRect();
        pg.querySelectorAll('a[href]').forEach(a => {
          const r = a.getBoundingClientRect();
          pdf.link(r.left - P.left, r.top - P.top, r.width, r.height, { url: a.href });
        });
      }
      if (opts.dry) return { pages: pages.length, bytes: pdf.output('blob').size, kept };  // test mode, no download
      pdf.save('my-10-hooks.pdf');
    } catch (e) {
      console.error(e);
      alert("couldn't build the pdf on this device. try the blank pdf, or open this page on a laptop.");
    } finally {
      overlays.forEach(d => d.remove());
      root.classList.remove('capturing');
      fit();
      btn.textContent = label;
      btn.disabled = false;
    }
  }

  const mine = document.querySelector('.bar .mine');
  if (mine) mine.addEventListener('click', () => makePdf(mine));
  window.__makePdf = makePdf;  // handy for testing
})();
