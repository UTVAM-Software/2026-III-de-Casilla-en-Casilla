(() => {
  const normalize = (value) => value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("es");

  document.querySelectorAll("[data-table-search]").forEach((input) => {
    const tableBody = document.getElementById(input.dataset.tableSearch);
    if (!tableBody) return;

    const rows = Array.from(tableBody.querySelectorAll("[data-search-row]"));
    const emptyState = tableBody.querySelector("[data-empty-state]");
    const noResults = tableBody.querySelector("[data-no-results]");

    const filterRows = () => {
      const query = normalize(input.value.trim());
      let visibleRows = 0;

      rows.forEach((row) => {
        const matches = normalize(row.textContent || "").includes(query);
        row.hidden = !matches;
        if (matches) visibleRows += 1;
      });

      if (emptyState) emptyState.hidden = rows.length > 0;
      if (noResults) {
        noResults.hidden = rows.length === 0 || query === "" || visibleRows > 0;
      }
    };

    input.addEventListener("input", filterRows);
    filterRows();
  });
})();
