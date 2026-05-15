document.getElementById('runButton').addEventListener('click', async () => {
    const code = document.getElementById('codeInput').value;
    const outputArea = document.getElementById('outputArea');
    const runButton = document.getElementById('runButton');
    
    // Feedback visual
    outputArea.textContent = "Executando...";
    runButton.disabled = true;

    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();
        
        // Retorno do backend
        outputArea.textContent = data.result || "Código executado.";
    } catch (error) {
        outputArea.textContent = "Erro ao conectar com o servidor.";
    } finally {
        // Reabilita o botão
        runButton.disabled = false;
    }
});