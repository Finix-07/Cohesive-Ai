// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    fetchData(); // Fetch and display data
    setupEventListeners(); // Setup dark mode and reset
});

// Fetch and load JSON data
async function fetchData() {
    try {
        const response = await fetch("data.json");
        const jsonData = await response.json();

        // Support both single and multiple entries
        if (Array.isArray(jsonData)) {
            jsonData.forEach(displayTable);
        } else {
            displayTable(jsonData);
        }
    } catch (error) {
        console.error("Error loading JSON data:", error);
    }
}

// Display table from JSON
function displayTable(data) {
    const companyName = document.getElementById("companyName");
    const companyLink = document.getElementById("companyLink");
    const tableHeader = document.getElementById("tableHeader");
    const tableBody = document.getElementById("tableBody");
    const columnPills = document.getElementById("columnPills");
    const columnCounter = document.getElementById("columnCounter");

    // Set company name and URL
    companyName.textContent = data.company.name || "Unknown";
    companyLink.textContent = data.company.url || "No URL";
    companyLink.href = data.company.url || "#";

    // Clear previous content
    tableHeader.innerHTML = "";
    tableBody.innerHTML = "";
    columnPills.innerHTML = "";

    // Create table headers and column pills
    data.columns.forEach((column, index) => {
        // Add table headers
        const th = document.createElement("th");
        th.textContent = column;
        th.dataset.index = index; // For toggle reference
        tableHeader.appendChild(th);

        // Add column pills for visibility toggle
        const pill = document.createElement("span");
        pill.className = "column-pill active";
        pill.textContent = column;
        pill.dataset.index = index; // Associate with the column
        pill.addEventListener("click", toggleColumn);
        columnPills.appendChild(pill);
    });

    // Create a single row from data
    const row = document.createElement("tr");
    data.columns.forEach(column => {
        const td = document.createElement("td");
        // Handle nested content structure properly
        td.textContent = data.data[column]?.content?.content || "N/A";
        row.appendChild(td);
    });
    tableBody.appendChild(row);

    // Update visible column count
    updateColumnCounter();
}

// Toggle visibility of a column
function toggleColumn(event) {
    const index = event.target.dataset.index;
    const header = document.querySelector(`#tableHeader th:nth-child(${+index + 1})`);
    const cells = document.querySelectorAll(`#tableBody td:nth-child(${+index + 1})`);

    // Toggle visibility
    const isVisible = header.style.display !== "none";
    header.style.display = isVisible ? "none" : "table-cell";
    cells.forEach(cell => {
        cell.style.display = isVisible ? "none" : "table-cell";
    });

    // Toggle active class for pill
    event.target.classList.toggle("active");

    // Update the visible column counter
    updateColumnCounter();
}

// Update the visible column counter
function updateColumnCounter() {
    const activePills = document.querySelectorAll(".column-pill.active").length;
    const totalPills = document.querySelectorAll(".column-pill").length;
    document.getElementById("columnCounter").textContent = `${activePills}/${totalPills}`;
}

// Setup dark mode toggle and reset functionality
function setupEventListeners() {
    // Dark mode toggle
    document.getElementById("toggleTheme").addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
    });

    // Reset button (reloads page)
    document.getElementById("resetTable").addEventListener("click", () => {
        location.reload();
    });
}

