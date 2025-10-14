// Dark mode & Light mode toggle button

document.addEventListener('DOMContentLoaded', function () {
  if (!document.getElementById('theme-switch')) {
    const switchButton = document.createElement('button');
    switchButton.id = 'theme-switch';
    switchButton.innerHTML = '<span id="theme-icon">🌙</span> <span id="theme-label">Dark Mode</span>';
    switchButton.style.position = 'fixed';
    switchButton.style.top = '24px';
    switchButton.style.right = '24px';
    switchButton.style.zIndex = '1000';
    switchButton.style.padding = '10px 22px';
    switchButton.style.borderRadius = '24px';
    switchButton.style.border = 'none';
    switchButton.style.background = 'linear-gradient(90deg, #232526 0%, #414345 100%)';
    switchButton.style.color = '#fff';
    switchButton.style.fontWeight = 'bold';
    switchButton.style.fontSize = '1rem';
    switchButton.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
    switchButton.style.cursor = 'pointer';
    switchButton.style.transition = 'background 0.3s, color 0.3s';
    switchButton.onmouseover = function() {
      switchButton.style.background = 'linear-gradient(90deg, #414345 0%, #232526 100%)';
    };
    switchButton.onmouseout = function() {
      switchButton.style.background = 'linear-gradient(90deg, #232526 0%, #414345 100%)';
    };
    document.body.appendChild(switchButton);

    // Check for saved theme in localStorage
    if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark-mode');
      document.getElementById('theme-icon').innerText = '☀️';
      document.getElementById('theme-label').innerText = 'Light Mode';
    }

    switchButton.addEventListener('click', function () {
      document.body.classList.toggle('dark-mode');
      if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        document.getElementById('theme-icon').innerText = '☀️';
        document.getElementById('theme-label').innerText = 'Light Mode';
      } else {
        localStorage.setItem('theme', 'light');
        document.getElementById('theme-icon').innerText = '🌙';
        document.getElementById('theme-label').innerText = 'Dark Mode';
      }
    });
  }
});

// Add dark mode styles
const style = document.createElement('style');
style.innerHTML = `
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
