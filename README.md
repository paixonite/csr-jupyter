# CSR Jupyter
Uma solução mínima para executar python no servidor a partir de uma interface web

<img width="600" height="600" alt="csr logo" src="https://github.com/user-attachments/assets/f7d4bbcc-69e3-41a0-bdf0-80207d0b04ca" />

>É a antena do CSR mirando pra Júpiter. Legal né?

## Como Executar

1. Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.
2. Na raiz do projeto, execute o comando:
   ```bash
   docker-compose up --build
   ```
3. Acesse a interface web pelo navegador no endereço: `http://localhost:6543`

## Estrutura do projeto / stack

O projeto foi estruturado com uma divisão bem clara de responsabilidades:
* **Frontend**: Usei HTML, CSS e JavaScript puros para montar uma interface simples e responsiva. O script JS captura os dados do formulário e os envia no formato JSON para a API utilizando o método HTTP POST.
* **Backend**: Escolhi o framework Flask em Python para servir a página estática e expor a rota `/execute`, que recebe os scripts enviados pelo usuário.
* **Execução**: Utilizei o módulo nativo `subprocess` do Python. Ele isola a execução do código em um processo independente, captura a saída (`stdout` ou `stderr`) e devolve o resultado para o frontend formatado em JSON.

Além disso, a aplicação inteira foi conteinerizada com Docker.

## Raciocínio / Decisões

Em projetos anteriores, já tive a oportunidade de utilizar todas as tecnologias que escolhi para esse desafio, o que me deu segurança nas decisões. 

O Flask se mostrou a melhor opção para subir um servidor mínimo em Python. Ele facilita muito o roteamento e a manipulação de JSON sem a dor de cabeça de configurar tudo na mão (como seria se eu usasse a biblioteca nativa `http.server`), e sem o peso de um framework robusto demais para o escopo, como o Django ou Node.js. 

O módulo `subprocess` é essencial pra esse tipo de aplicação. Executar o código em um processo separado do servidor web evita que a aplicação trave caso o código enviado cause um erro fatal.

No frontend, a comunicação cliente-servidor assíncrona com AJAX é uma forma simples de fazer uma aplicação responsiva, que não precisa recarregar a página a cada execução. Optei por não usar bibliotecas de interface mais robustas (como o React) porque isso fugiria totalmente do escopo mínimo desse teste, então mantive uma interface estática bem básica. 

A decisão de empacotar esse projeto em um container encaixou como uma luva. Com o Docker, eu resolvo a questão das dependências (o Docker se torna a única exigência para rodar o projeto) e ainda adiciono uma camada extra de proteção entre o código arbitrário que está sendo executado e a máquina de quem está usando.

Utilizei da IA para auxiliar na redação da maior parte do código. Meu foco foi atuar no papel de arquiteto, planejando os fluxos, definindo as tecnologias, pensando nas decisões de segurança e revisando a lógica implementada.

## Limitações

* **Proteção fraca do Docker**: O container proteje o computador que está hospedando a aplicação, mas o isolamento não é perfeito por dentro. Se o usuário enviar um script malicioso (como tentar apagar diretórios do sistema), o comando vai rodar e quebrar o ambiente interno do container. Se isso acontecesse, o sitema precisaria de um `docker-compose up` novamente para funcionar.
* **Timeout travado**: Para evitar que um loop infinito trave o servidor, um timeout de 5 segundos foi implementado. Isso ignifica que qualquer código de realmente demore mais de 5 segundos pra executar, falhará.
* **Bloqueio da entrada**: Na forma atual que o `subprocesses` funciona, o backend apenas envia a saída do script. Ou seja, se o código pedisse por algum tipo de input, nada aconteceria, e a execução falharia por timeout. 

## Sugestões de Melhorias

Para uma versão de produção, essas seriam as prioridades de melhoria:

**- Segurança**

1. **Restringir recursos**: Usar o `docker-compose` pra limitar os recursos de CPU e RAM, impedindo que scripts malicosos derrubem o servidor.

2. **Isolar a rede**: Configuar o container para desabilitar o acesso à internet, impedindo que o usuário faça requisições para baixar malware, por exemplo.

3. **Limitar privilégios**: Usar o Dockerfile para criar um usuário não-root exclusivamente para rodar a aplicação, caso o usuário consiga sair do interpretador de python.

**- Performance**

4. **Cache de execuções**: Implementar uma camada de cache temporário. Se um usuário enviar exatamente o mesmo bloco de código que acabou de ser executado, o sistema retorna o resultado no cache, o que economiza CPU.

**- UX e Funcionalidades**

5. **Melhorar os logs**: Implementar ferramentas de APM (Application Performance Monitoring) para obter informações mais detalhadas de tempo de execução, consumo de recursos, etc.

6. **Editor de código avançado**: Trocar a tag `<textarea>` atual por um motor de IDE pronto para navegador, o que possibilitaria highlight de sintaxe, contagem de linhas, autocomplete, etc.
   
8. **Suporte pra input de dados**: Adicionar um campo na interface onde o usuário possa digitar entradas de texto. Essas entradas seriam injetadas no processo via `subprocess.Popen`, fazendo os inputs em tempo de execução funcionarem sem timeout.

9. **Execução de múltiplos arquivos**: Alterar a API para receber um arquivo `.zip` com uma estrutura de pastas, para que o usuário crie scripts mais complexos com vários módulos importados entre si.

10. **Melhorias na interface**: Uma interface com título descritivo, manual de uso, footer e header com links úteis, botões e wrappers mais polidos, bonitos e responsíveis, e, principalmente, um tema escuro! Possívelmente, um framework como React ou Vue seriam ideais.
