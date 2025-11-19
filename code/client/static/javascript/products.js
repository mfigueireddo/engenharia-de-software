const ICON_EDIT = "✏️";
const ICON_CONFIRM = "✅";
const ICON_DELETE = "🗑️";

apiGetMultiple(
    "http://127.0.0.1:5000/produtos",
    "produtos",
    (item) => {                   
      insertList(item.nome, item.marca, item.categoria, item.preco, item.preco_promocional, item.id);
    }
);

// Função para criar um botão close para cada item da lista
const insertCloseButton = (parent) => 
{
    let span = document.createElement("span");
    let txt = document.createTextNode(ICON_DELETE);
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
}

// Função para criar um botão edit para cada item da lista
const insertEditButton = (parent) => 
{
    let span = document.createElement("span");
    let txt = document.createTextNode(ICON_EDIT);
    span.className = "edit";
    span.appendChild(txt);
    parent.appendChild(span);
}

// Função para inserir items na lista apresentada
const insertList = (nome, marca, categoria, preco, preco_promocional, id) => 
{
    var item = [nome, marca, categoria, preco, preco_promocional]
    var table = document.getElementById('myTable');
    var row = table.insertRow();

    row.dataset.id = id;

    for (var i = 0; i < item.length; i++) 
    {
        var cel = row.insertCell(i);
        cel.textContent = item[i];
    }

    insertEditButton(row.insertCell(-1))
    insertCloseButton(row.insertCell(-1))
    document.getElementById("newNome").value = "";
    document.getElementById("newMarca").value = "";
    document.getElementById("newCategoria").value = "";
    document.getElementById("newPreco").value = "";
    document.getElementById("newPrecoPromocional").value = "";

    editElement(table)
    removeElement()
}

// ========= Funções que fazem requests =========

const newItem = async () => 
{
    let nomeProduct = document.getElementById("newNome").value;
    let marcaProduct = document.getElementById("newMarca").value;
    let categoriaProduct = document.getElementById("newCategoria").value;
    let precoProduct = document.getElementById("newPreco").value;
    let precoPromocionalProduct = document.getElementById("newPrecoPromocional").value;

    if (nomeProduct === '') 
        alert("Escreva o nome de um item!");

    else if (isNaN(precoProduct) || isNaN(precoPromocionalProduct)) 
        alert("Preço e preço promocional precisam ser números!");
    
    else 
    {
        const data = await apiPost(
            "http://127.0.0.1:5000/produto",
            {
                nome: nomeProduct,
                marca: marcaProduct,
                categoria: categoriaProduct,
                preco: precoProduct,
                preco_promocional: precoPromocionalProduct ? precoPromocionalProduct : null
            }
        );

        if (!data) {
            alert("Erro ao adicionar item!");
            return;
        }

        insertList(
            nomeProduct,
            marcaProduct,
            categoriaProduct,
            precoProduct,
            precoPromocionalProduct,
            data.id
        );        
        
    }
}

const editElement = (table) => 
{
    let editButtons = document.getElementsByClassName("edit");

    for (let i = 0; i < editButtons.length; i++) 
    {
        editButtons[i].onclick = function () 
        {
            let row = this.parentElement.parentElement;
            let id = row.dataset.id;

            if (this.textContent === ICON_EDIT) 
            {
                for (let j = 0; j < row.cells.length - 2; j++) 
                {
                    row.cells[j].contentEditable = true;
                    row.cells[j].style.backgroundColor = "#ffffcc";
                }
                this.textContent = ICON_CONFIRM;
            } 
            else 
            {
                let nome = row.cells[0].textContent;
                let marca = row.cells[1].textContent;
                let categoria = row.cells[2].textContent;
                let preco = row.cells[3].textContent;
                let preco_promocional = row.cells[4].textContent;

                if (confirm("Deseja salvar as alterações deste item?")) 
                {
                    apiPatch(
                        "http://127.0.0.1:5000/produto", 
                        {
                            id: Number(id),
                            nome: nome,
                            marca: marca,
                            categoria: categoria,
                            preco: Number(preco),
                            preco_promocional: Number(preco_promocional)
                        })
                    ;
                }

                for (let j = 0; j < row.cells.length - 2; j++)
                {
                    row.cells[j].contentEditable = false;
                    row.cells[j].style.backgroundColor = "#ffffff";
                }

                this.textContent = ICON_EDIT;
            }
        };
    }  
};

const removeElement = () => 
{
    let close = document.getElementsByClassName("close");
    let i;

    for (i = 0; i < close.length; i++) 
    {
        close[i].onclick = function () 
        {
            let div = this.parentElement.parentElement;
            const nomeItem = div.getElementsByTagName('td')[0].innerHTML

            if (confirm("Você tem certeza?")) 
            {
                div.remove()
                apiDelete
                (       
                    "http://127.0.0.1:5000/produto",
                    "nome", 
                    nomeItem 
                );
            }
        }
    }
}