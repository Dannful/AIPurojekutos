## Matrículas

Turma A - Guilherme Ismael Flach - 00342108
Turma A - Tiago Lucas Flach - 00275896
Turma A - Vinícius Daniel Spadotto - 00341554


## a) TTTM + Poda alfa-beta

Ao que tudo indica, o agente parece estar funcionando bem. Ele sempre empata consigo mesmo, mas nenhum humano conseguiu achar um estragégia para ganhar dele (no máximo empatar). Apesar disso, ele as vezes (cerca de 20% do tempo) acaba empatando com o random. A teoria é que, como o espaço de jogadas do tttm é bastante restrito e existem muitos eixos de simetria, não é difícil para o random achar a jogada ótima por puro acaso.

## b) (Mini) Torneio de  Othello

(Todos os jogos realizados com 5s de tempo de pensamento)

|                        	| Contagem de Peças 	| Valor Posicional 	| Heurística Customizada 	|
|------------------------	|-------------------	|------------------	|------------------------	|
| Contagem de Peças      	| 20 / 44           	| 22 / 42         	| 13 / 51                	|
| Valor Posicional       	| 46 / 18           	| 19 / 45         	| 19 / 45                	|
| Heurística Customizada 	| 54 / 10           	| 40 / 24         	| 25 / 39                	|

A tabela acima mostra os resultados dos jogos, onde o valor em cada célula é o número de peças no tabuleiro final para cada uma das cores (B / W), como o resultado do jogo. Por exemplo: no jogo onde Contagem de Peças jogo como Pretas (B) e Valor Posicional jogou como Brancas (W), o resultado final foram 22 B x 42 W.

Como é possível ver, a Heurística Customizada deu show nas outras, a avaliação estática foi a segunda melhor e a contagem de peças foi a pior de todas.

Isso é esperado, já que a contagem de peças não é uma heurística apropriada para o jogo de Othello (mais sobre isso abaixo), mas a ideia geral é que podem ocorrer variações muito grandes de um movimento para outro, então ela carrega pouca semântica. O valor posicional tenta capturar uma noção intuitiva do estado do tabuleiro, "batendo o olho" e vendo se a situação está boa com base em quem tem peças em quais lugares. Por fim a Heurística Customizada tenta capturar um aspecto de "jogo" que será mais discutido na próxima sessão.

## Construção da Heurística Customizada:

Foi tomada como principal referência o artigo
[Heuristics for Othello](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/miniproject1_vaishu_muthu/Paper/Final_Paper.pdfcsforOthello).

Buscou-se implementar uma combinação entre as diversas heurísticas apresentadas:
1. **Paridade (Contagem de Peças)**

    Como já foi visto, essa heurística não é muito apropriada para o jogo de Othello, uma vez que captura apenas um senso "vago" do tabulerio, dado que podem ocorrer mudanças muito drásticas de um movimento para outro no valor. Apesar de indicar quem ganha, é apenas no movimento final que ela realmente importa.

    Por causa disso, optou-se por apenas usar essa heurística quando o número de espaços vazios fica pequeno (< 10), indicando que o jogo está próximo do fim e que talvez seja uma boa estratégia tentar garantir o que for possível de peças capturadas.

2. **Mobilidade**

    Mobilidade é uma noção interessante, já que é difícil ser expressa concretamente no jogo de Othello, já que precisam ocorrer capturas para um movimento ser legal. Seguindo a recomendação do artigo, separamos a mobilidade em duas categorias:

    *Mobilidade atual:* Número de movimentos que um dado jogador pode fazer em um dado estado do tabuleiro.

    *Mobilidade potencial:* Número de movimentos que um dado jogador poderá vir a fazer no futuro a partir daquele estado. É calculada somando o total de espaços abertos ao redor das peças do oponente.

3. Captura de Cantos

    Cantos são bons no jogo de Othello, já que, uma vez que foram capturados por um jogador, não podem mais ser recapturados nunca mais. São as posições mais estáveis do tabuleiro.

4. Estabilidade

    Estabiliade é uma representação de quão difícil é para o oponentente capturar uma peça. Evidentemente, quanto mais estável um determinado estado de jogo, melhor. O artigo original entra em mais detalhes sobre a estabilidade e busca-se implementar melhor ela em algum trabalho futuro, mas por agora, estamos apenas contando o número de peças do jogador sem quadrados vazios ao seu redor. Quanto mais delas, melhor.

5. Valor Posicional

    Por fim, busca-se ainda capturar o ideia "intuitiva" do jogo, então usamos a heurística em conjunto com a outra.

Por fim, nem todas as heurísticas são usadas em todos os momentos do jogo. Separamos a duração de jogo em três momentos: early (30+ espaços vazios), mid (10 a 29 espaços vazios) e late game (10 ou menos espaços vazios). Como a heurística de cantos é extremamente barata e eles são sempre bons, é usada em todos os momentos do jogo.

Durante o early game, o agente joga de forma "principiada", olhando principalmente para o valor posicional e para a mobilidade potencial de um dado estado. O agente olha para a estabilidade de uma posição, mas essa heurística contribui apenas com 50% do seu valor real.

Durante o mid game, o agente busca pensar mais para consolidar suas vantagens: a heurística de valor posicional é cortada para 45% de seu valor normal e a mobilidade atual entra em jogo também, além da estabilidade passar a contribuir integralmente para a avaliação da posição.

Por fim, no late game, o agente valoriza mobilidade atual, estabilidade e a contagem de peças apenas. Usar essa heurística mais simples permite que mais espaços sejam explorados no mesmo intervalo de tempo, aumentando a profundidade da exploração.

**Aprofundamento Iterativo:**

*"Temos aprofundamento iterativo em casa". O aprofundamento iterativo em casa:*

        if free_spaces < 10:
            return minimax_move(state, 5, evaluate_custom)
        if free_spaces < 20:
            return minimax_move(state, 4, evaluate_custom)
        return minimax_move(state, 3, evaluate_custom)

A ideia geral é que, quanto menos peças, maior a chance de bater em estados terminais e de deixar que a poda alfa-beta resolva o problema de tempo. O valor de cada "nível" do """aprofundamento iterativo""" foi descoberto empíricamente.

## Nah I'd Lose

Assim, usando-se esta heurística customizada, cria-se o agente "Nah I'd Lose", uma implementação relativamente besta para tentar derrubar o famoso Agente Smith. O nome vem do fato de que ele provavelmente vai perder, deixando essa tarefa para seu sucessor "Nah I'd Win".