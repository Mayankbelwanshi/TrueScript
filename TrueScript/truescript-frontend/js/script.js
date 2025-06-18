document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];

  if (!file) {
    alert('Please select a file');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    const output = `
      <h3>Plagiarism Score: ${data.score}%</h3>
      <ul>
        ${data.details.map(d => `<li>${d.file}: ${d.similarity}</li>`).join('')}
      </ul>
    `;
    document.getElementById('resultOutput').innerHTML = output;
  } catch (err) {
    alert('Error uploading file');
  }
});
