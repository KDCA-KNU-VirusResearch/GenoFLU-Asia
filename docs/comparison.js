(() => {
  const search = document.getElementById('comparison-search');
  const category = document.getElementById('comparison-category');
  const groups = [...document.querySelectorAll('#comparison-table tbody')];
  function filter() {
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    groups.forEach(group => {
      const match = (category.value === 'all' || group.dataset.category === category.value)
        && terms.every(term => group.dataset.search.includes(term));
      group.hidden = !match;
      if (match) count++;
    });
    document.getElementById('comparison-count').textContent = `${count} of ${groups.length} genotypes`;
    document.getElementById('comparison-empty').hidden = count !== 0;
  }
  search.addEventListener('input', filter);
  category.addEventListener('change', filter);
  filter();
})();
