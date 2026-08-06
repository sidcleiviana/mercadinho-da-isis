# Design System

**Documento:** 10_DESIGN_SYSTEM.md

---

# 1. Objetivo

Este documento define o padrão visual de todo o sistema.

Seu objetivo é garantir consistência entre todas as telas, componentes e futuras funcionalidades.

Nenhuma tela deverá criar novos estilos sem necessidade.

Sempre reutilizar componentes existentes.

---

# 2. Filosofia Visual

O sistema deverá transmitir a sensação de um software profissional utilizado em um pequeno supermercado.

Não deverá parecer um jogo.

Também não deverá parecer um sistema empresarial complexo.

O equilíbrio desejado é:

**Profissional + Simples + Acolhedor**

A criança deve sentir que está utilizando um sistema "de verdade".

---

# 3. Princípios

Toda decisão de design deverá seguir estes princípios:

* simplicidade;
* clareza;
* previsibilidade;
* consistência;
* conforto visual.

Sempre priorizar facilidade de uso em vez de efeitos visuais.

---

# 4. Identidade

A interface deverá transmitir:

* organização;
* limpeza;
* tranquilidade;
* confiança.

Evitar excesso de informação.

Cada tela deve possuir um único foco principal.

---

# 5. Paleta de Cores

Utilizar uma paleta neutra.

Cores principais:

* Branco
* Tons claros de cinza
* Azul como cor primária
* Verde para sucesso
* Vermelho para erros
* Amarelo para avisos

Evitar cores excessivamente saturadas.

Nunca utilizar muitas cores simultaneamente.

---

# 6. Tipografia

Utilizar apenas uma família tipográfica em todo o sistema.

Características desejadas:

* excelente legibilidade;
* aparência moderna;
* boa leitura em tablets.

Hierarquia:

Título

Subtítulo

Texto

Legenda

Nunca utilizar mais de quatro níveis tipográficos.

---

# 7. Espaçamento

Utilizar espaçamento consistente.

Todos os componentes deverão seguir uma mesma escala.

Evitar elementos "grudados".

A interface deve respirar.

---

# 8. Bordas

Utilizar cantos levemente arredondados.

Nunca exagerar no arredondamento.

A aparência deve permanecer profissional.

---

# 9. Sombras

Sombras discretas.

Apenas para separar elementos.

Nunca utilizar sombras fortes.

---

# 10. Ícones

Todos os ícones deverão seguir o mesmo estilo.

Preferencialmente:

* simples;
* contorno fino;
* fácil reconhecimento.

Nunca misturar estilos diferentes.

---

# 11. Botões

Todos os botões seguem um padrão único.

Estados:

* Normal
* Hover
* Pressionado
* Desabilitado

Botões importantes:

Cor primária.

Botões secundários:

Cor neutra.

Botões destrutivos:

Vermelho.

---

# 12. Campos de Entrada

Todos os campos deverão possuir:

* altura consistente;
* bordas discretas;
* foco claramente identificado.

Mensagens de erro aparecem logo abaixo do campo.

---

# 13. Cards

Os cards são o principal componente visual.

Exemplos:

Produto

Cliente aguardando

Resumo

Indicador financeiro

Todos seguem:

* mesma borda;
* mesmo espaçamento;
* mesma sombra.

---

# 14. Tabelas

As tabelas deverão possuir:

* cabeçalho destacado;
* linhas alternadas discretamente;
* alinhamento consistente.

Nunca utilizar excesso de linhas divisórias.

---

# 15. Fotografias dos Produtos

As fotos são extremamente importantes.

Sempre utilizar:

* boa qualidade;
* fundo limpo;
* enquadramento semelhante.

A fotografia deverá ser mais importante que o texto.

---

# 16. Feedback Visual

Toda ação relevante gera retorno imediato.

Exemplos:

Produto encontrado.

Venda concluída.

Estoque atualizado.

Cliente chegou.

Cliente desistiu.

Essas mensagens deverão aparecer discretamente.

Desaparecer automaticamente.

Nunca bloquear a operação do usuário.

---

# 17. Notificações

As notificações aparecem no canto superior direito.

Devem ser pequenas.

Discretas.

Fáceis de fechar.

Não utilizar janelas modais para simples avisos.

---

# 18. Modais

Utilizar modais apenas quando necessário.

Exemplos:

Adicionar estoque.

Registrar saída.

Excluir produto.

Nunca abrir múltiplos modais simultaneamente.

---

# 19. Dashboard

O Dashboard deve parecer um painel administrativo.

Poucos elementos.

Grandes indicadores.

Informação clara.

Nunca parecer uma planilha.

---

# 20. Central de Atendimento

A fila deverá ser extremamente limpa.

Cada atendimento ocupa um card.

Informações:

* nome;
* tempo aguardando;
* botão Atender.

Nenhuma informação desnecessária.

---

# 21. Modo Atendimento

Este é o principal diferencial visual do projeto.

Ao iniciar um atendimento:

Toda a interface muda.

O usuário entra em um ambiente exclusivo.

O menu desaparece.

O Dashboard desaparece.

Toda a atenção passa para a venda.

A tela deverá lembrar um sistema de PDV moderno.

---

# 22. Área do Cliente

O topo da tela apresenta:

* nome do cliente;
* status do atendimento.

Logo abaixo:

O chat.

A conversa utiliza balões simples.

Sem avatares.

Sem emojis.

---

# 23. Área da Venda

Durante o atendimento, a maior área da tela será destinada aos produtos.

Sempre mostrar:

* produtos solicitados;
* produtos registrados;
* total da compra.

O valor total deverá possuir grande destaque visual.

---

# 24. Leitura do Código de Barras

Ao reconhecer um código:

Emitir um pequeno som de confirmação.

Exibir rapidamente:

* fotografia;
* nome;
* quantidade;
* confirmação visual.

Essa animação deverá durar aproximadamente dois segundos.

Depois desaparecer automaticamente.

---

# 25. Estados Visuais

Todo componente possui estados claros.

Exemplos:

Disponível

Indisponível

Selecionado

Em atendimento

Concluído

Desistiu

Os estados devem ser compreendidos rapidamente.

---

# 26. Responsividade

Notebook:

Aproveitar toda a largura.

Tablet:

Reorganizar componentes verticalmente.

Nunca ocultar funcionalidades.

---

# 27. Animações

As animações deverão existir apenas para melhorar a compreensão.

Nunca para chamar atenção.

Exemplos aceitáveis:

* abertura de modal;
* chegada de notificação;
* confirmação de leitura;
* atualização do total.

Todas devem ser rápidas.

---

# 28. Sons

O sistema utilizará sons discretos apenas quando agregarem valor.

Exemplos:

Leitura correta do código de barras.

Cliente chegou.

Venda concluída.

Erro de leitura.

Os sons deverão ser curtos e suaves.

Nunca utilizar músicas.

Nunca reproduzir sons continuamente.

---

# 29. Linguagem

Toda a interface utilizará linguagem simples.

Exemplos:

Correto:

Adicionar Estoque

Registrar Saída

Produto Encontrado

Cliente Aguardando

Evitar termos técnicos desnecessários.

---

# 30. Consistência

Toda funcionalidade nova deverá utilizar os componentes já existentes.

Evitar criar novos estilos.

Reutilização é prioridade.

---

# 31. Experiência Esperada

Ao utilizar o sistema, a criança deve sentir que está operando o caixa de um pequeno mercado real.

As ações devem parecer naturais:

* abrir o expediente;
* atender clientes;
* passar produtos no leitor;
* finalizar vendas;
* organizar estoque;
* conferir o caixa;
* encerrar o expediente.

O sistema deve transmitir responsabilidade, organização e autonomia, sem deixar de ser leve e agradável.

---

# 32. Regra Final

Sempre que surgir dúvida sobre uma decisão de design, deverá prevalecer a solução que torne a interface mais simples, mais consistente e mais próxima de um software real de supermercado.

O Design System existe para garantir que todo o projeto pareça ter sido desenvolvido por uma única equipe, mantendo identidade visual, clareza e qualidade em todas as telas.
