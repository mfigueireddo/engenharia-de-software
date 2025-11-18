/****************************************************
 * Função genérica para POST
 * endpoint: URL para enviar
 * fields: objeto JS com pares chave/valor
 * Ex: { nome: "Bola", quantidade: 5, valor: 10 }
 ****************************************************/
async function apiPost(endpoint, fields) {
    const formData = new FormData();

    // Insere cada atributo dinamicamente
    Object.entries(fields).forEach(([key, value]) => {
        formData.append(key, value);
    });

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            body: formData
        });

        return await response.json(); // Retorna o JSON completo
    } catch (error) {
        console.error("POST Error:", error);
        return null;
    }
}

/****************************************************
 * Função genérica para PATCH
 * endpoint: URL para enviar
 * fields: objeto JS com pares chave/valor
 ****************************************************/
async function apiPatch(endpoint, fields) {
    const formData = new FormData();

    Object.entries(fields).forEach(([key, value]) => {
        formData.append(key, value);
    });

    try {
        const response = await fetch(endpoint, {
            method: "PATCH",
            body: formData
        });

        return await response.json();
    } catch (error) {
        console.error("PATCH Error:", error);
        return null;
    }
}

/****************************************************
 * Função genérica para DELETE
 * endpoint: URL base
 * paramName: o nome do parâmetro de query (ex: "nome", "id")
 * paramValue: o valor desse parâmetro
 ****************************************************/
async function apiDelete(endpoint, paramName, paramValue) {
    const url = `${endpoint}?${paramName}=${encodeURIComponent(paramValue)}`;

    try {
        const response = await fetch(url, {
            method: "DELETE"
        });

        return await response.json();
    } catch (error) {
        console.error("DELETE Error:", error);
        return null;
    }
}

/*
API para realizar requisições GET de maneira genérica (retornando um único item)

Parâmetros
    endpoint: URL a ser enviada
    itemKey: Chave que contém o item retornado
    onResult: Callback a ser executada com o item retornado
*/
const apiGetOne = async (endpoint, itemKey, onResult) => 
{
    try 
    {
        const response = await fetch(endpoint, { method: 'GET' });

        if (!response.ok) 
            throw new Error(`Erro ao fazer GET: ${response.status}`);

        const data = await response.json();

        // Conferindo se a chave existe
        if (!(itemKey in data)) 
            throw new Error(`A chave '${itemKey}' não existe na resposta da API.`);

        const item = data[itemKey];

        // Conferindo se NÃO é lista (essa função espera 1 único item)
        if (Array.isArray(item)) 
            throw new Error(`A chave '${itemKey}' contém uma lista, mas era esperado apenas um item.`);

        // Executa a callback passando o item
        onResult(item);
  
    } 
    catch (error) 
    {
        console.error("Erro no apiGetOne:", error);
    }
};

const getList = async (endpoint, listKey, onItem) => {
    try {
      const response = await fetch(endpoint, { method: 'GET' });
  
      if (!response.ok) {
        throw new Error(`Erro ao fazer GET: ${response.status}`);
      }
  
      const data = await response.json();
  
      if (!Array.isArray(data[listKey])) {
        throw new Error(`A chave '${listKey}' não contém uma lista.`);
      }
  
      data[listKey].forEach(item => onItem(item));
  
    } catch (error) {
      console.error("Erro no getList:", error);
    }
  };
  