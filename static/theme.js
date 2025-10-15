// Dark mode & Light mode toggle button

document.addEventListener('DOMContentLoaded', function () {
  if (!document.getElementById('theme-switch')) {
    const switchButton = document.createElement('button');
    switchButton.id = 'theme-switch';
    switchButton.innerHTML = '<span id="theme-icon" class="theme-icon" aria-hidden="true">🌙</span>';
    switchButton.setAttribute('aria-label', 'Toggle theme');
    switchButton.title = 'Toggle theme';
    // Placement
    switchButton.style.position = 'fixed';
    switchButton.style.top = '24px';
    switchButton.style.right = '24px';
    switchButton.style.zIndex = '1000';
    // Circular icon button
    switchButton.style.width = '46px';
    switchButton.style.height = '46px';
    switchButton.style.padding = '0';
    switchButton.style.borderRadius = '999px';
    switchButton.style.border = '1px solid rgba(0,0,0,0.08)';
    switchButton.style.display = 'flex';
    switchButton.style.alignItems = 'center';
    switchButton.style.justifyContent = 'center';
    switchButton.style.background = 'linear-gradient(135deg, #f8f9fb 0%, #e3e7ee 100%)';
    switchButton.style.color = '#111';
    switchButton.style.boxShadow = '0 6px 16px rgba(0,0,0,0.15)';
    switchButton.style.cursor = 'pointer';
    switchButton.style.backdropFilter = 'blur(6px)';
    switchButton.style.webkitBackdropFilter = 'blur(6px)';
    switchButton.style.transition = 'transform 0.15s ease, background 0.3s ease, color 0.3s ease, border-color 0.3s ease';
    switchButton.onmouseover = function() {
      switchButton.style.transform = 'translateY(-2px)';
    };
    switchButton.onmouseout = function() {
      switchButton.style.transform = 'translateY(0)';
    };
    document.body.appendChild(switchButton);

    // Helper to apply button theme
    function styleButtonForTheme(isDark){
      if(isDark){
        switchButton.style.background = 'linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%)';
        switchButton.style.borderColor = 'rgba(255,255,255,0.14)';
        switchButton.style.color = '#fff';
        switchButton.style.boxShadow = '0 8px 20px rgba(0,0,0,0.4)';
      } else {
        switchButton.style.background = 'linear-gradient(135deg, #f8f9fb 0%, #e3e7ee 100%)';
        switchButton.style.borderColor = 'rgba(0,0,0,0.08)';
        switchButton.style.color = '#111';
        switchButton.style.boxShadow = '0 6px 16px rgba(0,0,0,0.15)';
      }
    }

    // Check for saved theme in localStorage
    if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark-mode');
      document.getElementById('theme-icon').innerText = '☀️';
      styleButtonForTheme(true);
    }

    switchButton.addEventListener('click', function () {
      document.body.classList.toggle('dark-mode');
      if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        const icon = document.getElementById('theme-icon');
        icon.innerText = '☀️';
        icon.classList.add('spin');
        setTimeout(() => icon.classList.remove('spin'), 450);
        styleButtonForTheme(true);
      } else {
        localStorage.setItem('theme', 'light');
        const icon = document.getElementById('theme-icon');
        icon.innerText = '🌙';
        icon.classList.add('spin');
        setTimeout(() => icon.classList.remove('spin'), 450);
        styleButtonForTheme(false);
      }
    });
  }
});

// Add dark mode styles
const style = document.createElement('style');
style.innerHTML = `
  /* Theme switch icon animation */
  .theme-icon { font-size: 20px; line-height: 1; display: inline-block; transition: transform .45s ease; }
  .theme-icon.spin { transform: rotate(360deg); }
  body.dark-mode {
    background-color: #181818 !important;
    color: #f1f1f1 !important;
  }
  body.dark-mode a { color: #8ab4f8 !important; }
  body.dark-mode input, body.dark-mode textarea, body.dark-mode select {
    background: #222 !important;
    color: #f1f1f1 !important;
    border-color: #444 !important;
  }
  body.dark-mode .card, body.dark-mode .container, body.dark-mode .navbar {
    background: #232323 !important;
    color: #f1f1f1 !important;
  }
  body.dark-mode table {
    background: #232323 !important;
    color: #f1f1f1 !important;
    border-color: #444 !important;
  }
  body.dark-mode th, body.dark-mode td {
    background: #232323 !important;
    color: #f1f1f1 !important;
    border-color: #444 !important;
  }
  body.dark-mode th {
    background: #0a3042 !important;
    color: #fff !important;
  }
  body.dark-mode tr {
    border-bottom: 1px solid #444 !important;
  }
  body.dark-mode .btn {
    color: #fff !important;
    border-color: #444 !important;
  }
  body.dark-mode .btn-view {
    background: #1976d2 !important;
    color: #fff !important;
  }
  body.dark-mode .btn-warning {
    background: #f0ad4e !important;
    color: #222 !important;
  }
  body.dark-mode .btn-primary {
    background: #007bff !important;
    color: #fff !important;
  }
  body.dark-mode .btn-success {
    background: #28a745 !important;
    color: #fff !important;
  }
`;
document.head.appendChild(style);
