<<<<<<< HEAD
/* ── Stitch — client-side logic ─────────────────────────────────────────── */

// Generic form submit → fetch → render result
async function submitExtraction(formId, resultId, loaderId, downloadBtnId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const loader  = document.getElementById(loaderId);
    const resultEl = document.getElementById(resultId);
    const dlBtn   = downloadBtnId ? document.getElementById(downloadBtnId) : null;

    if (loader)   loader.classList.remove('hidden');
    if (resultEl) resultEl.textContent = '';
    if (dlBtn)    dlBtn.classList.add('hidden');

    const fd = new FormData(form);
    const action = form.getAttribute('action');

    try {
      const res = await fetch(action, { method: 'POST', body: fd });

      // Download endpoints return a zip blob
      if (res.headers.get('content-type')?.includes('zip')) {
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href = url;
        a.download = res.headers.get('content-disposition')
          ?.split('filename=')[1] || 'download.zip';
        a.click();
        URL.revokeObjectURL(url);
        if (resultEl) resultEl.textContent = '✓ Download started.';
        if (loader)   loader.classList.add('hidden');
        return;
      }

      const data = await res.json();

      if (data.error) {
        if (resultEl) resultEl.textContent = '✗ Error: ' + data.error;
      } else {
        const payload = data.data ?? JSON.stringify(data.data ?? data, null, 2);
        if (resultEl) resultEl.textContent = payload;

        // Offer plain-text download
        if (dlBtn) {
          dlBtn.classList.remove('hidden');
          dlBtn.onclick = () => {
            const blob = new Blob([payload], { type: 'text/plain' });
            const url  = URL.createObjectURL(blob);
            const a    = document.createElement('a');
            a.href = url;
            a.download = 'extraction_result.txt';
            a.click();
            URL.revokeObjectURL(url);
          };
        }

        // Refresh stats if present
        if (data.count !== undefined) {
          const countEl = document.getElementById('result-count');
          if (countEl) countEl.textContent = data.count;
        }
        if (data.elapsed !== undefined) {
          const timeEl = document.getElementById('result-elapsed');
          if (timeEl) timeEl.textContent = data.elapsed + 's';
        }
      }
    } catch (err) {
      if (resultEl) resultEl.textContent = '✗ Network error: ' + err.message;
    } finally {
      if (loader) loader.classList.add('hidden');
    }
  });
}

// Copy-to-clipboard helper
function copyResult(resultId) {
  const el = document.getElementById(resultId);
  if (!el) return;
  navigator.clipboard.writeText(el.textContent).then(() => {
    const btn = document.getElementById('copy-btn');
    if (btn) { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1500); }
  });
}

// Init on page load
document.addEventListener('DOMContentLoaded', () => {
  submitExtraction('scrape-form', 'result-output', 'result-loader', 'download-btn');
});
=======
/* ── Stitch — client-side logic ─────────────────────────────────────────── */

// Generic form submit → fetch → render result
async function submitExtraction(formId, resultId, loaderId, downloadBtnId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const loader  = document.getElementById(loaderId);
    const resultEl = document.getElementById(resultId);
    const dlBtn   = downloadBtnId ? document.getElementById(downloadBtnId) : null;

    if (loader)   loader.classList.remove('hidden');
    if (resultEl) resultEl.textContent = '';
    if (dlBtn)    dlBtn.classList.add('hidden');

    const fd = new FormData(form);
    const action = form.getAttribute('action');

    try {
      const res = await fetch(action, { method: 'POST', body: fd });

      // Download endpoints return a zip blob
      if (res.headers.get('content-type')?.includes('zip')) {
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href = url;
        a.download = res.headers.get('content-disposition')
          ?.split('filename=')[1] || 'download.zip';
        a.click();
        URL.revokeObjectURL(url);
        if (resultEl) resultEl.textContent = '✓ Download started.';
        if (loader)   loader.classList.add('hidden');
        return;
      }

      const data = await res.json();

      if (data.error) {
        if (resultEl) resultEl.textContent = '✗ Error: ' + data.error;
      } else {
        const payload = data.data ?? JSON.stringify(data.data ?? data, null, 2);
        if (resultEl) resultEl.textContent = payload;

        // Offer plain-text download
        if (dlBtn) {
          dlBtn.classList.remove('hidden');
          dlBtn.onclick = () => {
            const blob = new Blob([payload], { type: 'text/plain' });
            const url  = URL.createObjectURL(blob);
            const a    = document.createElement('a');
            a.href = url;
            a.download = 'extraction_result.txt';
            a.click();
            URL.revokeObjectURL(url);
          };
        }

        // Refresh stats if present
        if (data.count !== undefined) {
          const countEl = document.getElementById('result-count');
          if (countEl) countEl.textContent = data.count;
        }
        if (data.elapsed !== undefined) {
          const timeEl = document.getElementById('result-elapsed');
          if (timeEl) timeEl.textContent = data.elapsed + 's';
        }
      }
    } catch (err) {
      if (resultEl) resultEl.textContent = '✗ Network error: ' + err.message;
    } finally {
      if (loader) loader.classList.add('hidden');
    }
  });
}

// Copy-to-clipboard helper
function copyResult(resultId) {
  const el = document.getElementById(resultId);
  if (!el) return;
  navigator.clipboard.writeText(el.textContent).then(() => {
    const btn = document.getElementById('copy-btn');
    if (btn) { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1500); }
  });
}

// Init on page load
document.addEventListener('DOMContentLoaded', () => {
  submitExtraction('scrape-form', 'result-output', 'result-loader', 'download-btn');
});
>>>>>>> b18b9d46bedb02eaf41a121561f6edc1c2d361c9
