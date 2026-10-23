const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const resultsContainer = document.getElementById('results');
const summaryText = document.getElementById('summary-text');

async function fetchProducts(query = '') {
  const response = await fetch(`/api/products?q=${encodeURIComponent(query)}`);
  const data = await response.json();
  return data;
}

function renderProducts(products) {
  if (!products.length) {
    resultsContainer.innerHTML = `
      <div class="empty-state">
        <h3>No products found</h3>
        <p>Try searching for a different product or category.</p>
      </div>
    `;
    return;
  }

  resultsContainer.innerHTML = products
    .map(
      (product) => `
        <article class="product-card">
          <div class="product-tag">${product.source}</div>
          <h3>${product.name}</h3>
          <div class="meta-line">
            <span>${product.brand}</span>
            <span>${product.category}</span>
          </div>
          <div class="price-row">
            <span class="price">₹${product.price}</span>
            <span class="original-price">${product.original_price ? `₹${product.original_price}` : ''}</span>
          </div>
          <div class="attributes">
            <span>⭐ ${product.rating}</span>
            <span>${product.reviews} reviews</span>
            <span>${product.delivery}</span>
          </div>
          <div class="attributes">
            ${product.tags.map((tag) => `<span>${tag}</span>`).join('')}
          </div>
          <a class="link-button" href="${product.url}" target="_blank" rel="noreferrer">View listing</a>
        </article>
      `
    )
    .join('');
}

async function loadDefaultResults() {
  const data = await fetchProducts();
  summaryText.textContent = data.summary;
  renderProducts(data.products);
}

searchForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const query = searchInput.value.trim();
  const data = await fetchProducts(query);
  summaryText.textContent = data.summary;
  renderProducts(data.products);
});

loadDefaultResults();
