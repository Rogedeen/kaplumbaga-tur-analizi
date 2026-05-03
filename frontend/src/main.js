import '../index.css';
import { CONFIG } from './config.js';
import { uploadImage } from './api.js';
import { previewImage, resetUIForLoading, updateUIWithResults, updateUIWithError } from './ui.js';

window.handleFileUpload = async function(event) {
  const file = event.target.files[0];
  if (!file) return;

  const elements = {
    previewImage: document.getElementById('previewImage'),
    resultCard: document.getElementById('resultCard'),
    loadingStatus: document.getElementById('loadingStatus'),
    confidenceText: document.getElementById('confidenceText'),
    confidenceBar: document.getElementById('confidenceBar'),
    speciesName: document.getElementById('speciesName'),
    scientificName: document.getElementById('scientificName'),
    reasonsList: document.getElementById('aiReasons'),
    featuresBox: document.getElementById('symbolicFeatures')
  };

  previewImage(file, elements.previewImage);
  resetUIForLoading(elements);

  try {
    const data = await uploadImage(file, CONFIG.API_URL);
    updateUIWithResults(data, elements, CONFIG.CONFIDENCE_THRESHOLD);
  } catch (error) {
    console.error(error);
    updateUIWithError(error, elements);
  }
};
