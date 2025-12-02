// Variáveis globais
let products = [];
let saleItems = [];
let saleTotal = 0;

// Reseta completamente a venda atual
const resetCurrentSale = () => {
    // Limpa array de itens
    saleItems.length = 0;
    saleTotal = 0;
    
    // Limpa campos do formulário
    document.getElementById('productSelect').value = '';
    document.getElementById('productQuantity').value = '1';
    
    // Atualiza interface
    updateSaleItemsTable();
    updateSaleTotal();
};

// Carrega produtos no select e vendas existentes
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    loadSales();
});

// Carrega todos os produtos para o select
const loadProducts = async () => {
    try {
        const response = await apiGetMultiple(
            "http://127.0.0.1:5000/produtos",
            "produtos",
            (product) => {
                products.push(product);
            }
        );
        
        populateProductSelect();
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
        alert('Erro ao carregar produtos!');
    }
};

// Popula o select de produtos
const populateProductSelect = () => {
    const select = document.getElementById('productSelect');
    select.innerHTML = '<option value="">Selecione um produto</option>';
    
    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = `${product.nome} - R$ ${product.preco_promocional || product.preco}`;
        option.dataset.price = product.preco_promocional || product.preco;
        option.dataset.name = product.nome;
        select.appendChild(option);
    });
};

// Adiciona produto à venda
const addProductToSale = () => {
    const productSelect = document.getElementById('productSelect');
    const quantityInput = document.getElementById('productQuantity');
    
    const productId = productSelect.value;
    const quantity = parseInt(quantityInput.value);
    
    if (!productId) {
        alert('Selecione um produto!');
        return;
    }
    
    if (!quantity || quantity <= 0) {
        alert('Digite uma quantidade válida!');
        return;
    }
    
    const selectedOption = productSelect.selectedOptions[0];
    const productName = selectedOption.dataset.name;
    const unitPrice = parseFloat(selectedOption.dataset.price);
    
    // Verifica se o produto já está na venda
    const existingItemIndex = saleItems.findIndex(item => item.product_id === parseInt(productId));
    
    if (existingItemIndex >= 0) {
        // Atualiza a quantidade se o produto já existe
        saleItems[existingItemIndex].quantity += quantity;
        saleItems[existingItemIndex].total_price = saleItems[existingItemIndex].quantity * unitPrice;
    } else {
        // Adiciona novo item
        const saleItem = {
            product_id: parseInt(productId),
            product_name: productName,
            quantity: quantity,
            unit_price: unitPrice,
            total_price: quantity * unitPrice
        };
        saleItems.push(saleItem);
    }
    
    // Reseta os campos
    productSelect.value = '';
    quantityInput.value = '1';
    
    // Atualiza a tabela
    updateSaleItemsTable();
    updateSaleTotal();
};

// Atualiza a tabela de itens da venda
const updateSaleItemsTable = () => {
    const table = document.getElementById('saleItemsTable');
    
    // Remove todas as linhas exceto o cabeçalho
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }
    
    // Adiciona os itens
    saleItems.forEach((item, index) => {
        const row = table.insertRow();
        
        row.insertCell(0).textContent = item.product_name;
        row.insertCell(1).textContent = `R$ ${item.unit_price.toFixed(2)}`;
        row.insertCell(2).textContent = item.quantity;
        row.insertCell(3).textContent = `R$ ${item.total_price.toFixed(2)}`;
        
        const actionCell = row.insertCell(4);
        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remover';
        removeBtn.className = 'removeItemBtn';
        removeBtn.onclick = () => removeItemFromSale(index);
        actionCell.appendChild(removeBtn);
    });
    
    // Habilita/desabilita o botão finalizar
    const finalizeBtn = document.querySelector('.finalizeBtn');
    finalizeBtn.disabled = saleItems.length === 0;
};

// Remove item da venda
const removeItemFromSale = (index) => {
    saleItems.splice(index, 1);
    updateSaleItemsTable();
    updateSaleTotal();
};

// Atualiza o total da venda
const updateSaleTotal = () => {
    saleTotal = saleItems.reduce((total, item) => total + item.total_price, 0);
    document.getElementById('saleTotal').textContent = saleTotal.toFixed(2);
};

// Finaliza a venda
const finalizeSale = async () => {
    if (saleItems.length === 0) {
        alert('Adicione pelo menos um produto à venda!');
        return;
    }
    
    try {
        const saleData = {
            items: saleItems.map(item => ({
                product_id: item.product_id,
                quantity: item.quantity
            }))
        };
        
        // Para vendas, use fetch diretamente com JSON
        const response = await fetch("http://127.0.0.1:5000/venda", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(saleData)
        });
        
        if (response.ok) {
            const result = await response.json();
            alert('Venda realizada com sucesso!');
            
            // Reseta completamente a venda
            resetCurrentSale();
            
            // Recarrega as vendas
            loadSales();
        } else {
            const errorData = await response.json();
            alert(`Erro ao realizar a venda: ${errorData.message || 'Erro desconhecido'}`);
        }
    } catch (error) {
        console.error('Erro ao finalizar venda:', error);
        alert('Erro ao finalizar venda!');
    }
};

// Carrega vendas existentes
const loadSales = async () => {
    try {
        // Limpa a tabela antes de carregar
        const table = document.getElementById('salesTable');
        while (table.rows.length > 1) {
            table.deleteRow(1);
        }
        
        const response = await fetch("http://127.0.0.1:5000/vendas", {
            method: 'GET'
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.vendas && Array.isArray(data.vendas)) {
                data.vendas.forEach(sale => {
                    insertSaleInTable(sale);
                });
            }
        }
    } catch (error) {
        console.error('Erro ao carregar vendas:', error);
    }
};

// Insere venda na tabela
const insertSaleInTable = (sale) => {
    const table = document.getElementById('salesTable');
    const row = table.insertRow();
    
    row.insertCell(0).textContent = sale.id;
    row.insertCell(1).textContent = new Date(sale.data_venda).toLocaleString('pt-BR');
    row.insertCell(2).textContent = `R$ ${sale.total_amount.toFixed(2)}`;
    
    const actionsCell = row.insertCell(3);
    
    const viewBtn = document.createElement('button');
    viewBtn.textContent = 'Ver';
    viewBtn.className = 'viewSaleBtn';
    // Usar closure com parâmetros específicos em vez de objeto completo
    viewBtn.onclick = () => showSaleInfo(sale.id);
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Excluir';
    deleteBtn.className = 'deleteSaleBtn';
    deleteBtn.onclick = () => deleteSale(sale.id, row);
    
    actionsCell.appendChild(viewBtn);
    actionsCell.appendChild(deleteBtn);
};

// Busca e mostra detalhes da venda específica por ID
const showSaleInfo = async (saleId) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/venda?id=${saleId}`, {
            method: 'GET'
        });
        
        if (response.ok) {
            const sale = await response.json();
            
            let details = `Venda #${sale.id}\n`;
            details += `Data: ${new Date(sale.data_venda).toLocaleString('pt-BR')}\n\n`;
            details += `Itens:\n`;
            
            sale.items.forEach(item => {
                details += `- ${item.product_name}: ${item.quantity}x R$ ${item.unit_price.toFixed(2)} = R$ ${item.total_price.toFixed(2)}\n`;
            });
            
            details += `\nTotal: R$ ${sale.total_amount.toFixed(2)}`;
            
            alert(details);
        } else {
            const errorText = await response.text();
            alert('Erro ao buscar detalhes da venda: ' + errorText);
        }
    } catch (error) {
        console.error('Erro ao buscar venda:', error);
        alert('Erro ao carregar detalhes da venda');
    }
};

// Exclui venda
const deleteSale = async (saleId, row) => {
    if (confirm('Tem certeza que deseja excluir esta venda?')) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/venda?id=${saleId}`, {
                method: "DELETE"
            });
            
            if (response.ok) {
                row.remove();
                alert('Venda excluída com sucesso!');
            } else {
                alert('Erro ao excluir venda!');
            }
        } catch (error) {
            console.error('Erro ao excluir venda:', error);
            alert('Erro ao excluir venda!');
        }
    }
};