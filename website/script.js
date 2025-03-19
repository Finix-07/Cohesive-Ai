document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    const nextColumnBtn = document.getElementById('nextColumn');
    const resetColumnsBtn = document.getElementById('resetColumns');
    const toggleThemeBtn = document.getElementById('toggleTheme');
    const columnCounter = document.getElementById('columnCounter');
    const columnPills = document.getElementById('columnPills');
    
    // State variables
    let tableData = [];
    let allColumns = [];
    let visibleColumns = [];
    
    // Load data from JSON file
    async function loadData() {
        try {
            const response = await fetch('data.json');
            tableData = await response.json();
            
            if (tableData.length > 0) {
                allColumns = Object.keys(tableData[0]);
                updateColumnPills();
                updateColumnCounter();
            }
        } catch (error) {
            console.error('Error loading data:', error);
            
            // Fallback to sample data if fetch fails
            tableData = [
                {"Name": "Alice", "Age": 25, "City": "New York", "Score": 90},
                {"Name": "Bob", "Age": 30, "City": "Los Angeles", "Score": 85},
                {"Name": "Charlie", "Age": 35, "City": "Chicago", "Score": 88}
            ];
            
            allColumns = Object.keys(tableData[0]);
            updateColumnPills();
            updateColumnCounter();
        }
    }
    
    // Add the next column
    function addNextColumn() {
        if (visibleColumns.length < allColumns.length) {
            const nextColumnIndex = visibleColumns.length;
            const nextColumn = allColumns[nextColumnIndex];
            visibleColumns.push(nextColumn);
            
            // Add header cell
            const headerCell = document.createElement('th');
            headerCell.textContent = nextColumn;
            tableHeader.appendChild(headerCell);
            
            // If this is the first column, create rows for all data
            if (visibleColumns.length === 1) {
                tableData.forEach((row, index) => {
                    const tableRow = document.createElement('tr');
                    tableRow.id = `row-${index}`;
                    const cell = document.createElement('td');
                    cell.textContent = row[nextColumn];
                    tableRow.appendChild(cell);
                    tableBody.appendChild(tableRow);
                });
            } 
            // Otherwise, add cells to existing rows
            else {
                tableData.forEach((row, index) => {
                    const tableRow = document.getElementById(`row-${index}`);
                    const cell = document.createElement('td');
                    cell.textContent = row[nextColumn];
                    tableRow.appendChild(cell);
                });
            }
            
            updateColumnPills();
            updateColumnCounter();
            
            // Hide the next button if all columns are shown
            if (visibleColumns.length === allColumns.length) {
                nextColumnBtn.classList.add('hidden');
            }
        }
    }
    
    // Reset all columns
    function resetColumns() {
        visibleColumns = [];
        tableHeader.innerHTML = '';
        tableBody.innerHTML = '';
        updateColumnPills();
        updateColumnCounter();
        nextColumnBtn.classList.remove('hidden');
    }
    
    // Toggle dark/light theme
    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
    }
    
    // Update column pills display
    function updateColumnPills() {
        columnPills.innerHTML = '';
        allColumns.forEach(column => {
            const pill = document.createElement('span');
            pill.textContent = column;
            pill.classList.add('column-pill');
            
            if (visibleColumns.includes(column)) {
                pill.classList.add('active');
            } else {
                pill.classList.add('inactive');
            }
            
            columnPills.appendChild(pill);
        });
    }
    
    // Update column counter
    function updateColumnCounter() {
        columnCounter.textContent = `${visibleColumns.length}/${allColumns.length}`;
    }
    
    // Event listeners
    nextColumnBtn.addEventListener('click', addNextColumn);
    resetColumnsBtn.addEventListener('click', resetColumns);
    toggleThemeBtn.addEventListener('click', toggleTheme);
    
    // Initialize the app
    loadData();
});