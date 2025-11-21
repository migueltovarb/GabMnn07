// ===== CERRAR ALERTAS =====
document.addEventListener('DOMContentLoaded', function() {
    // Auto-cerrar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Cerrar alerta al hacer click en el botón close
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        });
    });
});

// ===== VALIDACIÓN DE FORMULARIOS =====
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('form-error');
            isValid = false;
        } else {
            input.classList.remove('form-error');
        }

        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.remove('form-error');
            }
        });
    });

    return isValid;
}

// ===== CONFIRMACIÓN DE ELIMINACIÓN =====
function confirmDelete(itemName = 'este elemento') {
    return confirm(`¿Estás seguro de que deseas eliminar ${itemName}? Esta acción no se puede deshacer.`);
}

// ===== COPIAR AL PORTAPAPELES =====
function copyToClipboard(text, elementId = null) {
    navigator.clipboard.writeText(text).then(() => {
        const element = elementId ? document.getElementById(elementId) : null;
        if (element) {
            const originalText = element.innerText;
            element.innerText = '¡Copiado!';
            setTimeout(() => {
                element.innerText = originalText;
            }, 2000);
        } else {
            alert('Copiado al portapapeles');
        }
    }).catch(err => {
        console.error('Error al copiar:', err);
    });
}

// ===== FORMATEAR FECHA =====
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(dateString).toLocaleDateString('es-CO', options);
}

// ===== FORMATEAR HORA =====
function formatTime(timeString) {
    const options = { 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(timeString).toLocaleTimeString('es-CO', options);
}

// ===== MOSTRAR/OCULTAR PASSWORD =====
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

// ===== FILTRAR TABLA =====
function filterTable(tableId, searchId) {
    const searchInput = document.getElementById(searchId);
    const table = document.getElementById(tableId);

    if (!searchInput || !table) return;

    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// ===== EXPORTAR TABLA A CSV =====
function exportTableToCSV(tableId, filename = 'reporte.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('td, th');
        const csvRow = [];
        cells.forEach(cell => {
            csvRow.push('"' + cell.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

// ===== DESCARGAR CSV =====
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// ===== IMPRIMIR PÁGINA =====
function printPage() {
    window.print();
}

// ===== MOSTRAR SPINNER DE CARGA =====
function showLoadingSpinner(message = 'Cargando...') {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;

    spinner.innerHTML = `
        <div style="
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0f3460;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        "></div>
        <p style="color: white; font-size: 16px;">${message}</p>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;

    document.body.appendChild(spinner);
}

// ===== OCULTAR SPINNER =====
function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// ===== ENVIAR FORMULARIO CON VALIDACIÓN =====
function submitFormWithValidation(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    if (validateForm(formId)) {
        showLoadingSpinner('Guardando datos...');
        return true;
    } else {
        const firstError = form.querySelector('.form-error');
        if (firstError) {
            firstError.focus();
        }
        return false;
    }
}

// ===== TABLA INTERACTIVA =====
class DataTable {
    constructor(tableId, options = {}) {
        this.table = document.getElementById(tableId);
        this.options = {
            itemsPerPage: options.itemsPerPage || 10,
            searchable: options.searchable !== false,
            sortable: options.sortable !== false,
            ...options
        };
        this.init();
    }

    init() {
        if (!this.table) return;

        if (this.options.searchable) {
            this.addSearchBox();
        }

        if (this.options.sortable) {
            this.addSortability();
        }
    }

    addSearchBox() {
        const searchBox = document.createElement('input');
        searchBox.type = 'text';
        searchBox.className = 'table-search';
        searchBox.placeholder = 'Buscar en la tabla...';
        searchBox.style.cssText = `
            margin-bottom: 15px;
            padding: 10px 15px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            width: 100%;
            max-width: 300px;
        `;

        this.table.parentElement.insertBefore(searchBox, this.table);

        searchBox.addEventListener('keyup', () => this.search(searchBox.value));
    }

    search(term) {
        const rows = this.table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(term.toLowerCase()) ? '' : 'none';
        });
    }

    addSortability() {
        const headers = this.table.querySelectorAll('thead th');
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.title = 'Click para ordenar';
            header.addEventListener('click', () => this.sort(index));
        });
    }

    sort(columnIndex) {
        const rows = Array.from(this.table.querySelectorAll('tbody tr'));
        const isNumeric = rows.every(row => !isNaN(parseFloat(row.cells[columnIndex].innerText)));

        rows.sort((a, b) => {
            const aVal = a.cells[columnIndex].innerText;
            const bVal = b.cells[columnIndex].innerText;

            if (isNumeric) {
                return parseFloat(aVal) - parseFloat(bVal);
            }
            return aVal.localeCompare(bVal);
        });

        rows.forEach(row => this.table.querySelector('tbody').appendChild(row));
    }
}

// ===== INICIALIZAR TABLAS =====
document.addEventListener('DOMContentLoaded', function() {
    // Buscar todas las tablas con clase 'data-table' e inicializarlas
    document.querySelectorAll('table.data-table').forEach(table => {
        new DataTable(table.id);
    });
});