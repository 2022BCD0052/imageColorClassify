document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    form.addEventListener('submit', function(e) {
        // Show loading indicator aur hide results
        loading.classList.remove('hidden');
        results.classList.add('hidden');

        // Form submit ke baad Flask process karega, results show karne ka logic Flask ke response pe depend karega
        // Yeh timeout sirf initial hide/show ke liye hai, actual timing Flask pe depend karega
        setTimeout(() => {
            // Flask ke response ke baad yeh chalega (page reload hoga)
        }, 100);
    });

    // Agar page reload ke baad results hain, to loading hide karo aur results show karo
    if (document.querySelector('.result-img')) {
        loading.classList.add('hidden');
        results.classList.remove('hidden');
    }
});