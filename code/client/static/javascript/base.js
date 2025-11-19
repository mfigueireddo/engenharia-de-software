function appendIfNotEmpty(formData, key, value) {
    if (value !== "" && value !== null && value !== undefined) {
        formData.append(key, value);
    }
}

async function apiPost(endpoint, fields) 
{
    const formData = new FormData();

    Object.entries(fields).forEach(([key, value]) => { appendIfNotEmpty(formData, key, value); });

    try 
    {
        const response = await fetch
        (
            endpoint, 
            {
                method: "POST",
                body: formData
            }
        );

        return await response.json(); 
    } 
    catch (error) 
    {
        console.error("POST Error:", error);
        return null;
    }
}

async function apiPatch(endpoint, fields) 
{
    const formData = new FormData();

    Object.entries(fields).forEach(([key, value]) => { appendIfNotEmpty(formData, key, value); });

    try 
    {
        const response = await fetch
        (
            endpoint, 
            {
                method: "PATCH",
                body: formData
            }
        );

        return await response.json();
    } 
    catch (error) 
    {
        console.error("PATCH Error:", error);
        return null;
    }
}

async function apiDelete(endpoint, paramName, paramValue) 
{
    const url = `${endpoint}?${paramName}=${encodeURIComponent(paramValue)}`;

    try 
    {
        const response = await fetch
        (
            url, 
            {method: "DELETE"}
        );

        return await response.json();
    } 
    catch (error) 
    {
        console.error("DELETE Error:", error);
        return null;
    }
}

async function apiGetOne(endpoint, itemKey, onResult)
{
    try 
    {
        const response = await fetch
        (
            endpoint, 
            { method: 'GET' }
        );

        if (!response.ok) 
            throw new Error(`Erro ao fazer GET: ${response.status}`);

        const data = await response.json();

        if (!(itemKey in data)) 
            throw new Error(`A chave '${itemKey}' não existe na resposta da API.`);

        const item = data[itemKey];

        if (Array.isArray(item)) 
            throw new Error(`A chave '${itemKey}' contém uma lista, mas era esperado apenas um item.`);

        onResult(item);
  
    } 
    catch (error) 
    {
        console.error("Erro no apiGetOne:", error);
    }
};

async function apiGetMultiple (endpoint, listKey, onItem)
{
    try 
    {
        const response = await fetch
        (
            endpoint, 
            { method: 'GET' }
        );

        if (!response.ok)
            throw new Error(`Erro ao fazer GET: ${response.status}`);

        const data = await response.json();

        if (!Array.isArray(data[listKey]))
            throw new Error(`A chave '${listKey}' não contém uma lista.`);

        data[listKey].forEach(item => onItem(item));

    } 
    catch (error) 
    {
        console.error("Erro no getList:", error);
    }
};