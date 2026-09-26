// Global variables
let fileData = null;
let predictionResults = null;
let visualizationData = null;
let currentTab = 'teks';

// Tab switching - preserve data
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const targetTab = this.getAttribute('data-tab');
        
        // Save current tab
        currentTab = targetTab;
        
        // Remove active class from all tabs
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        this.classList.add('active');
        const tabId = targetTab + '-tab';
        document.getElementById(tabId).classList.add('active');
        
        // Don't reset data - keep it visible
    });
});

// Text prediction
document.getElementById('predict-text-btn').addEventListener('click', async function() {
    const textInput = document.getElementById('text-input').value.trim();
    
    if (!textInput) {
        alert('Silakan masukkan teks terlebih dahulu!');
        return;
    }
    
    // Show loading
    document.getElementById('text-loading').style.display = 'block';
    document.getElementById('text-result').style.display = 'none';
    
    try {
        const response = await fetch('/predict/text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Display results
            document.getElementById('result-original-text').textContent = data.teks_asli;
            document.getElementById('result-preprocessed-text').textContent = data.teks_preprocessing;
            
            const stanceBadge = document.getElementById('result-stance');
            stanceBadge.textContent = data.stance;
            stanceBadge.className = 'badge-result ' + data.stance.toLowerCase();
            
            const topicBadge = document.getElementById('result-topic');
            topicBadge.textContent = data.topik_label;
            topicBadge.className = 'badge-result';
            
            document.getElementById('text-result').style.display = 'block';
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Terjadi kesalahan: ' + error.message);
    } finally {
        document.getElementById('text-loading').style.display = 'none';
    }
});

// File upload
document.getElementById('upload-btn').addEventListener('click', function() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Silakan pilih file terlebih dahulu!');
        return;
    }
    
    if (!file.name.endsWith('.csv')) {
        alert('File harus berformat CSV!');
        return;
    }
    
    fileData = file;
    document.getElementById('file-info').style.display = 'block';
    document.getElementById('file-info-text').textContent = `File "${file.name}" berhasil diunggah. Klik "Prediksi" untuk memproses.`;
    document.getElementById('predict-file-btn').style.display = 'inline-block';
});

// File prediction with realistic progress tracking
document.getElementById('predict-file-btn').addEventListener('click', async function() {
    if (!fileData) {
        alert('Silakan unggah file terlebih dahulu!');
        return;
    }
    
    // Show loading
    document.getElementById('file-loading').style.display = 'block';
    document.getElementById('results-table-container').style.display = 'none';
    document.getElementById('visualizations-container').style.display = 'none';
    
    // Reset progress bar
    updateProgress(0, 'Mengunggah file...');
    
    const formData = new FormData();
    formData.append('file', fileData);
    
    try {
        updateProgress(5, 'File terupload, memulai prediksi...');
        
        // Start realistic progress simulation
        let currentProgress = 5;
        const progressInterval = setInterval(() => {
            if (currentProgress < 70) {
                currentProgress += 3;
                updateProgress(currentProgress, 'Memproses prediksi...');
            } else if (currentProgress < 85) {
                currentProgress += 2;
                updateProgress(currentProgress, 'Membuat visualisasi...');
            }
        }, 800);
        
        const response = await fetch('/predict/file', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        updateProgress(95, 'Menyelesaikan...');
        
        const data = await response.json();
        
        updateProgress(100, 'Selesai!');
        
        if (response.ok) {
            predictionResults = data.results;
            visualizationData = data.visualizations; // Store visualizations
            
            // Smooth scroll and display results
            setTimeout(() => {
                document.getElementById('file-loading').style.display = 'none';
                displayResults(data.results);
                displayVisualizations(data.visualizations);
                document.getElementById('analyze-btn').style.display = 'inline-block';
                scrollToElement('results-table-container');
            }, 500);
        } else {
            alert('Error: ' + data.error);
            document.getElementById('file-loading').style.display = 'none';
        }
    } catch (error) {
        alert('Terjadi kesalahan: ' + error.message);
        document.getElementById('file-loading').style.display = 'none';
    }
});

// Update progress bar with message
function updateProgress(percent, message = '') {
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const loadingMessage = document.querySelector('#file-loading p');
    
    progressBar.style.width = percent + '%';
    progressBar.setAttribute('aria-valuenow', percent);
    progressText.textContent = percent + '%';
    
    if (message && loadingMessage) {
        loadingMessage.textContent = message;
    }
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Display results in table
function displayResults(results) {
    const tableBody = document.getElementById('results-table-body');
    tableBody.innerHTML = '';
    
    results.forEach((result, index) => {
        const row = document.createElement('tr');
        
        // Truncate text if too long
        const truncatedText = result.teks_asli.length > 50 
            ? result.teks_asli.substring(0, 50) + '...' 
            : result.teks_asli;
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${truncatedText}</td>
            <td><span class="badge ${getStanceBadgeClass(result.stance)}">${result.stance}</span></td>
            <td>${result.topik_label}</td>
        `;
        
        tableBody.appendChild(row);
    });
    
    document.getElementById('results-table-container').style.display = 'block';
}

// Get badge class based on stance
function getStanceBadgeClass(stance) {
    const lowerStance = stance.toLowerCase();
    if (lowerStance.includes('neutral')) return 'bg-secondary';
    if (lowerStance.includes('support') || lowerStance.includes('favor')) return 'bg-success';
    if (lowerStance.includes('against') || lowerStance.includes('oppose')) return 'bg-danger';
    return 'bg-info';
}

// Analyze button - toggle to show visualizations and hide table
document.getElementById('analyze-btn').addEventListener('click', function() {
    if (!visualizationData) {
        alert('Tidak ada visualisasi yang tersedia!');
        return;
    }
    
    // Hide table, show visualizations
    document.getElementById('results-table-container').style.display = 'none';
    document.getElementById('visualizations-container').style.display = 'block';
    document.getElementById('analyze-btn').style.display = 'none';
    document.getElementById('back-to-table-btn').style.display = 'inline-block';
    
    scrollToElement('visualizations-container');
});

// Back to table button - toggle to show table and hide visualizations
document.getElementById('back-to-table-btn').addEventListener('click', function() {
    // Hide visualizations, show table
    document.getElementById('visualizations-container').style.display = 'none';
    document.getElementById('results-table-container').style.display = 'block';
    document.getElementById('back-to-table-btn').style.display = 'none';
    document.getElementById('analyze-btn').style.display = 'inline-block';
    
    scrollToElement('results-table-container');
});

// Display wordclouds by stance
function displayWordcloudsByStance(wordclouds) {
    const container = document.getElementById('wordcloud-stance-container');
    container.innerHTML = '';
    
    for (const [stance, imgData] of Object.entries(wordclouds)) {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';
        col.innerHTML = `
            <h6 class="text-center">${stance}</h6>
            <img src="data:image/png;base64,${imgData}" alt="${stance}" class="img-fluid rounded">
        `;
        container.appendChild(col);
    }
}

// Display wordclouds by topic
function displayWordcloudsByTopic(wordclouds) {
    const container = document.getElementById('wordcloud-topic-container');
    container.innerHTML = '';
    
    for (const [topic, imgData] of Object.entries(wordclouds)) {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';
        col.innerHTML = `
            <h6 class="text-center">${topic}</h6>
            <img src="data:image/png;base64,${imgData}" alt="${topic}" class="img-fluid rounded">
        `;
        container.appendChild(col);
    }
}

// Display all visualizations at once
function displayVisualizations(visualizations) {
    // Display bar chart
    document.getElementById('barchart-img').src = 'data:image/png;base64,' + visualizations.barchart;
    
    // Display wordclouds by stance
    displayWordcloudsByStance(visualizations.wordcloud_stance);
    
    // Display wordclouds by topic
    displayWordcloudsByTopic(visualizations.wordcloud_topic);
    
    // Show visualizations container
    document.getElementById('visualizations-container').style.display = 'block';
}

// File input change handler - don't reset on tab switch
document.getElementById('file-input').addEventListener('change', function() {
    // Only reset if user selects a new file
    document.getElementById('predict-file-btn').style.display = 'none';
    document.getElementById('analyze-btn').style.display = 'none';
    document.getElementById('file-info').style.display = 'none';
    fileData = null;
    
    // Don't reset results and visualizations - they should persist
});
