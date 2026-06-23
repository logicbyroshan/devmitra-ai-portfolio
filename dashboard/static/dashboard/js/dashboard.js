// dashboard.js — Main admin JS utilities

document.addEventListener('DOMContentLoaded', () => {

    // ── Auto-dismiss alerts ─────────────────────────────────
    document.querySelectorAll('.alert').forEach(alert => {
        // Dismiss button
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => alert.remove());
        }
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // ── Toggle status switches (AJAX) ───────────────────────
    document.querySelectorAll('.status-toggle').forEach(toggle => {
        toggle.addEventListener('change', async function () {
            const url = this.dataset.url;
            if (!url) return;
            const row = this.closest('tr');
            const badge = row ? row.querySelector('.status-badge') : null;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                if (data.status !== 'ok') throw new Error('Server error');

                // Update badge text/class
                if (badge) {
                    const isOn = Object.values(data).find(v => typeof v === 'boolean');
                    if (isOn) {
                        badge.className = badge.className.replace(/\b(draft|inactive|hidden)\b/g, '');
                        badge.classList.add('published', 'active', 'visible');
                        badge.innerHTML = '<i class="fa-solid fa-eye fa-xs"></i> Visible';
                    } else {
                        badge.className = badge.className.replace(/\b(published|active|visible)\b/g, '');
                        badge.classList.add('hidden');
                        badge.innerHTML = '<i class="fa-solid fa-eye-slash fa-xs"></i> Hidden';
                    }
                }
                showToast('Status updated', 'success');
            } catch {
                this.checked = !this.checked; // revert
                showToast('Failed to update status', 'error');
            }
        });
    });

    // ── Confirm delete buttons ──────────────────────────────
    // Handled via separate confirm_delete.html page (no JS needed)

    // ── Simple toast notification ───────────────────────────
    window.showToast = function (message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type}`;
        toast.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;min-width:220px;animation:fadeIn 0.3s;';
        const icon = document.createElement('i');
        icon.className = `fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-xmark'}`;
        const text = document.createTextNode(' ' + message);
        toast.appendChild(icon);
        toast.appendChild(text);
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.4s';
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    };

    // ── CSRF token helper ───────────────────────────────────
    function getCsrfToken() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
    }

    // ── Formset management (add/remove rows) ───────────────
    document.querySelectorAll('.formset-add-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const prefix = btn.dataset.prefix;
            const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
            if (!totalForms) return;
            const count = parseInt(totalForms.value);
            const template = document.querySelector(`.formset-empty-form[data-prefix="${prefix}"]`);
            if (!template) return;
            const newForm = template.cloneNode(true);
            newForm.classList.remove('formset-empty-form');
            newForm.removeAttribute('data-prefix');
            newForm.style.display = '';
            newForm.innerHTML = newForm.innerHTML.replaceAll(`__prefix__`, count);
            template.parentNode.insertBefore(newForm, btn.closest('.formset-wrapper').querySelector('.formset-footer'));
            totalForms.value = count + 1;
        });
    });

    // Formset delete checkbox
    document.querySelectorAll('.formset-delete-checkbox').forEach(cb => {
        cb.addEventListener('change', function () {
            const item = this.closest('.formset-item');
            if (item) item.classList.toggle('marked-delete', this.checked);
        });
    });

    // ── Table search filter ─────────────────────────────────
    const tableSearch = document.getElementById('table-search');
    if (tableSearch) {
        tableSearch.addEventListener('input', function () {
            const q = this.value.toLowerCase();
            document.querySelectorAll('.data-table tbody tr').forEach(row => {
                row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
            });
        });
    }

});
