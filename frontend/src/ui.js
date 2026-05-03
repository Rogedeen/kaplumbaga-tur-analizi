/**
 * Updates the image element with a preview of the selected file.
 * @param {File} file - The file to preview.
 * @param {HTMLImageElement} imageElement - The DOM element to update.
 */
export function previewImage(file, imageElement) {
  if (!file || !imageElement) return;
  imageElement.src = URL.createObjectURL(file);
}

/**
 * Resets the UI to a loading state.
 * @param {Object} elements - A dictionary of DOM elements.
 */
export function resetUIForLoading(elements) {
  elements.resultCard.style.display = 'block';
  elements.loadingStatus.innerText = 'Analyzing...';
  elements.confidenceText.innerText = '-%';
  elements.confidenceBar.style.width = '0%';
  elements.speciesName.innerText = 'Processing';
  elements.scientificName.innerText = 'Please wait';
  elements.speciesName.classList.remove('text-error');
}

/**
 * Updates the UI with the prediction results or an error state.
 * @param {Object} data - The prediction data returned by the API.
 * @param {Object} elements - A dictionary of DOM elements to update.
 * @param {number} threshold - The confidence score threshold (e.g. 40).
 */
export function updateUIWithResults(data, elements, threshold) {
  elements.loadingStatus.innerText = 'Confidence Score';
  const confPercent = Math.round((data.confidence || 0) * 100);
  elements.confidenceText.innerText = confPercent + '%';
  elements.confidenceBar.style.width = confPercent + '%';

  if (data.is_confident === false || confPercent < threshold) {
    elements.speciesName.innerText = 'Tür tam olarak belirlenemedi';
    elements.scientificName.innerText = 'Lütfen daha net bir fotoğraf yükleyin';
    elements.speciesName.classList.add('text-error');
  } else {
    elements.speciesName.innerText = data.common_name || data.predicted_species || 'Unknown';
    elements.scientificName.innerText = data.predicted_species || '';
    elements.speciesName.classList.remove('text-error');
  }

  // AI Reasons
  elements.reasonsList.innerHTML = '';
  if (data.reasons && data.reasons.length > 0) {
    data.reasons.forEach(reason => {
      elements.reasonsList.innerHTML += `
        <li class="flex items-start text-sm text-on-surface">
          <span class="material-symbols-outlined text-secondary mr-2 text-lg" style="font-size: 18px;">check_circle</span>
          <span>${reason}</span>
        </li>
      `;
    });
  } else {
    elements.reasonsList.innerHTML = `<li class="text-sm text-outline italic">Belirgin kural saptanamadı, sadece derin öğrenme modeli kullanıldı.</li>`;
  }

  // Symbolic Features
  elements.featuresBox.innerHTML = '';
  if (data.symbolic_features && Object.keys(data.symbolic_features).length > 0) {
    for (const [key, value] of Object.entries(data.symbolic_features)) {
      const scorePct = (value * 100).toFixed(1);
      const isHigh = value > 0.4;
      elements.featuresBox.innerHTML += `
        <div class="text-outline capitalize">${key.replace(/_/g, ' ')}</div>
        <div class="font-medium ${isHigh ? 'text-secondary font-bold' : 'text-outline'} text-right">${scorePct}%</div>
      `;
    }
  } else {
    elements.featuresBox.innerHTML = '<div class="col-span-2 text-outline italic">Özellik çıkarılamadı.</div>';
  }
}

/**
 * Updates the UI with an error message.
 * @param {Error} error - The error object.
 * @param {Object} elements - A dictionary of DOM elements.
 */
export function updateUIWithError(error, elements) {
  elements.loadingStatus.innerText = 'Error';
  elements.speciesName.innerText = 'Analysis Failed';
  elements.scientificName.innerText = 'Please ensure backend is running.';
}
