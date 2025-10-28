document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.getElementById('search-btn');
  const searchInput = document.getElementById('search-input');
  const resultsContainer = document.getElementById('results');

  searchBtn.addEventListener('click', async () => {
    const query = searchInput.value.trim();
    if (!query) {
      alert("Please enter a search term!");
      return;
    }

    // Call YOUR Python backend, not SerpAPI directly
    const apiUrl = `http://localhost:3000/search?q=${encodeURIComponent(query)}`;

    try {
      console.log("Fetching:", apiUrl);
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      console.log("Data:", data);

      resultsContainer.innerHTML = '';

      if (data.results && data.results.length > 0) {
        data.results.slice(0, 6).forEach(item => {
          const div = document.createElement('div');
          div.classList.add("result-item");
          div.innerHTML = `

            <h4>${item.title}</h4>
            <p>${item.price || 'Price not available'}</p>
            <a href="${item.link}" target="_blank">View Product</a>
            <hr/>
          `;
          resultsContainer.appendChild(div);
        });
      } else {
        resultsContainer.innerHTML = "<p>No products found!</p>";
      }
    } catch (err) {
      console.error("Error:", err);
      alert("Failed to fetch products. Check console for details.");
    }
  });
});
