/**
 * Uploads an image file to the prediction API.
 * @param {File} file - The file to upload.
 * @param {string} apiUrl - The API endpoint URL.
 * @returns {Promise<Object>} The API response data.
 * @throws {Error} If the API request fails.
 */
export async function uploadImage(file, apiUrl) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(apiUrl, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('API Error');
  }

  return response.json();
}
