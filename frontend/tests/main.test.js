import { describe, it, expect, vi, beforeEach } from 'vitest';
import { previewImage, resetUIForLoading, updateUIWithResults, updateUIWithError } from '../src/ui.js';
import { uploadImage } from '../src/api.js';

describe('API Utils', () => {
  it('should successfully upload image and return data', async () => {
    const mockData = { confidence: 0.9, predicted_species: 'Test Species' };
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockData
    });
    
    const file = new File([''], 'test.png');
    const result = await uploadImage(file, 'http://test.url');
    expect(result).toEqual(mockData);
    expect(global.fetch).toHaveBeenCalled();
  });

  it('should throw an error on API failure', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false
    });
    
    const file = new File([''], 'test.png');
    await expect(uploadImage(file, 'http://test.url')).rejects.toThrow('API Error');
  });
});

describe('UI Utils', () => {
  let elements;
  beforeEach(() => {
    document.body.innerHTML = `
      <img id="previewImage" />
      <div id="resultCard"></div>
      <div id="loadingStatus"></div>
      <div id="confidenceText"></div>
      <div id="confidenceBar"></div>
      <div id="speciesName"></div>
      <div id="scientificName"></div>
      <ul id="aiReasons"></ul>
      <div id="symbolicFeatures"></div>
    `;
    elements = {
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
    global.URL.createObjectURL = vi.fn(() => 'blob:test');
  });

  it('should preview image', () => {
    const file = new File([''], 'test.png');
    previewImage(file, elements.previewImage);
    expect(elements.previewImage.src).toContain('blob:test');
  });

  it('should not throw if preview image elements are missing', () => {
    expect(() => previewImage(null, null)).not.toThrow();
  });

  it('should reset UI for loading', () => {
    resetUIForLoading(elements);
    expect(elements.resultCard.style.display).toBe('block');
    expect(elements.loadingStatus.innerText).toBe('Analyzing...');
    expect(elements.speciesName.classList.contains('text-error')).toBe(false);
  });

  it('should update UI with results for high confidence', () => {
    const data = {
      confidence: 0.95,
      predicted_species: 'Caretta caretta',
      reasons: ['Reason 1'],
      symbolic_features: { feature_1: 0.8 }
    };
    updateUIWithResults(data, elements, 40);
    expect(elements.speciesName.innerText).toBe('Caretta caretta');
    expect(elements.confidenceText.innerText).toBe('95%');
    expect(elements.reasonsList.innerHTML).toContain('Reason 1');
    expect(elements.featuresBox.innerHTML).toContain('80.0%');
  });

  it('should handle no reasons and no features', () => {
    const data = {
      confidence: 0.95,
      predicted_species: 'Caretta caretta'
    };
    updateUIWithResults(data, elements, 40);
    expect(elements.reasonsList.innerHTML).toContain('Belirgin kural saptanamadı');
    expect(elements.featuresBox.innerHTML).toContain('Özellik çıkarılamadı');
  });

  it('should update UI with error state on low confidence', () => {
    const data = { confidence: 0.3 };
    updateUIWithResults(data, elements, 40);
    expect(elements.speciesName.innerText).toBe('Tür tam olarak belirlenemedi');
    expect(elements.speciesName.classList.contains('text-error')).toBe(true);
  });

  it('should update UI with error', () => {
    updateUIWithError(new Error('Test'), elements);
    expect(elements.loadingStatus.innerText).toBe('Error');
    expect(elements.speciesName.innerText).toBe('Analysis Failed');
  });
});

describe('Main App', () => {
  it('should handle file upload successfully', async () => {
    document.body.innerHTML = `
      <input type="file" id="fileInput" />
      <img id="previewImage" />
      <div id="resultCard"></div>
      <div id="loadingStatus"></div>
      <div id="confidenceText"></div>
      <div id="confidenceBar"></div>
      <div id="speciesName"></div>
      <div id="scientificName"></div>
      <ul id="aiReasons"></ul>
      <div id="symbolicFeatures"></div>
    `;
    global.URL.createObjectURL = vi.fn(() => 'blob:test');
    
    // Setup mock API response
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        confidence: 0.9,
        predicted_species: 'Main Species'
      })
    });

    // Import main.js to attach handleFileUpload to window
    await import('../src/main.js');

    const file = new File([''], 'test.png');
    const event = { target: { files: [file] } };
    
    await window.handleFileUpload(event);
    
    expect(document.getElementById('speciesName').innerText).toBe('Main Species');
  });

  it('should handle file upload failure', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('API Failure'));
    
    const file = new File([''], 'test.png');
    const event = { target: { files: [file] } };
    
    await window.handleFileUpload(event);
    
    expect(document.getElementById('speciesName').innerText).toBe('Analysis Failed');
  });

  it('should do nothing if no file selected', async () => {
    const event = { target: { files: [] } };
    await window.handleFileUpload(event);
    // Should not crash
  });
});
