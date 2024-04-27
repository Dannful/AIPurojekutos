Matriculas:
Guilherme Ismael Flach - 00342108\
Tiago Lucas Flach - 00275896\
Vinicius Daniel Spadotto - 00341554\

Exercício 1)

    Para os valores do bias e do weight, foram escolhidos 0 e 1, respectivamente, dado que os dados inicialmente visualizados se assemelham à função f(x) = x.
    A taxa de aprendizagem mostrou-se necessitar ser extremamente baixa, apresentando alta sensibilidade a sutis variações.
    Após uma quantidade extensiva de testes, observou-se que o alpha produz resultados palpáveis somente no intervalo aproximado de [0.01, 0.02], onde o número específico 0.023 apresentou o menor erro quadrático médio.
    Nesse contexto, obteve-se um erro quadrático médio aproximado de 3,237 com 1000 iterações, mudando apenas a quarta casa decimal em diante ao aumentar mais a quantidade de iterações, sendo desnecessário para a precisão almejada com este exercício.

Exercício 2)

    Questão 1 -
    	| Dataset       |  Tamanho das Imagens |  Num. de Classes | Num. de Amostras de Treino | Num. Amostras de Teste |
    	|---------------|----------------------|------------------|----------------------------|------------------------|
    	| CIFAR-10      | 32x32x3              | 10               | 50 000                     | 10 000                 |
    	| CIFAR-100     | 32x32x3              | 100              | 50 000                     | 10 000                 |
    	| MNIST         | 28x28x1              | 10               | 60 000                     | 10 000                 |
    	| Fashion_MNIST | 28x28x1              | 10               | 60 000                     | 10 000                 |

    	Simplesmente olhando para as características de cada dataset, seria "fácil" estimar que os datasets CIFAR são mais difíces que os MNIST.
    	Eles não só possuem imagens maiores, como também introduzem uma nova dimensão de informação: cores, na forma de seus três canais por pixel, levando a uma quantidade significativamente maior de informação que precisa ser processada e aprendida.

    	Dentro dessas categorias, também é fácil estimar que o CIFAR-100 seja significativamente mais difícil que o CIFAR-10, dado que possui 10x mais classes, fazendo com que simplesmente acertar "no chute" seja bem mais difícil.
    	Ainda, como o número de imagens totais é o mesmo, isso significa que há um número 10x menor de amostras por cada classe para serem usadas durante o treinamento, agravando a situação.
    	Isso pode ser confirmado com a busca rápida em sites de benchmark, como o *[Papers With Code](paperswithcode.com)*, no qual, mesmo redes que conseguem desempenhos acima de 99% no CIFAR-10, ainda possuem dificuldade para chegar para alcançar desempenhos semelhantes no CIFAR-100. Por exemplo, segundo as métricas do site a rede que segue o [modelo Resnet com maior desempenho](https://paperswithcode.com/paper/large-scale-learning-of-general-visual), consegue uma precisão de **99.37%** no CIFAR-10, mas apenas **93.51%** no CIFAR-100.

    	Dito isso, apenas olhando para as características estruturais dos dois não fica tão óbvio qual seria a grande diferença entre eles: ambos possuem o mesmo número de imagens, o mesmo tamanho e o mesmo número de classes.
    	Pórém, a chave para entender isso se encontra no conteúdo em sí dos dois datasets. Enquanto o MNIST é um dataset de números (desenhados a mão, com linhas em um fundo preto), o Fashion MNIST é um dataset de imagens de artigos de roupa (daí o *Fashion* no nome). Pode parecer pequeno, mas essa mudança semântica faz com que o Fashion MNIST seja um dataset significativamente mais difícil que o MNIST tradicional.
    	Uma explicação razoávelmente intutiva para isso pode ser encontrada pensando na "organização" da informação em cada um dos datasets.
    	Enquanto no MNIST clássico, quase toda a informação pertinente para a classificação encontra-se no formato geral do objeto (os números), no Fashion MNIST a informação encontra-se muito mais distribuída pela imagem: além do formato, a "textura" e detalhes finos se tornam muito mais importantes. O formato de um *sneaker* não é tão diferente assim de uma *sandal*, pelo menos não tanto quando a diferença de um 8 para um 9.
    	A própria natureza dos elementos de certa forma reflete esses fatos: a forma dos algarismos evoluiu por milhares de anos para que eles sejam facilmente reconhecidos a distância por apenas alguns traços, enquanto eu até hoje não sei diferenciar um terno de um blazer.
    	Novamente, olhando para o benchmark dentro do *Papers With Code*, podemos ver essa diferença claramente: [quase qualquer modelo](https://paperswithcode.com/sota/image-classification-on-mnist) consegue uma precisão maior que 99% no MNIST, enquanto a [maior precisão dentro do Fashion MNIST](https://paperswithcode.com/paper/fine-tuning-darts-for-image-classification) é de 96.91%.

    	Colocando desta forma, o Fashion MNIST é até mesmo comparável ao CIFAR-10, se não mais difícil. Isso pode ser analisado por alguns motivos:
    		- é um dataset considerado "fácil", então não são tantos os modelos de ponta que usam ele como benchmark;
    		- é um dataset em escala de cinza, novamente contribuindo com que talvez seja uma escolha menos "popular";
    		- a baixa resolução das imagens e a falta de cor na verdade atua como um dificultador no processo, "ocludindo" informações importantes para o reconhecimento (honestamente, como um ser humano, algumas daquelas imagens não fazem sentido nenhum pra mim).



    Questão 2 -
    	O primeiro dataset para o qual foram construídas redes foi o CIFAR-10.
    	As versões iniciais da rede eram bastante simples, seguindo apenas o modelo de Layer Convolucional -> MaxPooling2D -> Layer Convolucional -> ... -> Layer Denso.
    	Essas redes tinham resultados bastante abaixo da curva, limitadas a apenas cerca 35%.
    	Alterar a ordem, quantidade de filtros e tamanho dos kernels sem uma lógica (surpreendentemente) também não gerou resultados muito significativos.
    	Buscando resultados melhores, decidiu-se seguir a ideia de aumentar o número de filtros e diminuir o tamanho e stride do kernel ao longo dos layers (inspirada principalmente no modelo ResNet). Isso gerou resultados melhores (50%+ em alguns treinos), mas, devido ao baixo tamanho das imagens, era uma estratégia bastante limitada (poucas camadas já começavam a dar tamanhos negativos) e muito "manual".

    	A partir disso, quatro grandes coisas surtiram efeitos muito positivos:

    	- Adicionar layers de Dropout (padrão de 0.25 de chance de desligamento), ou seja, layers que "desligam" aleatóriamente certos neurônios durante partes do treinamento. Apesar de não terem tido um impacto imediato muito grande certamente ajudaram a rede a longo prazo, já que ajudam-a a não ficar "sobre-dependente" em alguns pontos.

    	- Adicionar uma camada de GlobalAveragePooling ao final da rede (antes da parte densa). Ainda que essa não seja a aplicação mais correta do layer, ajudou fortemente a "reter" melhor as informações dos layers convolucionais. Quebrou a barreira dos 60%.

    	- Inclusão de Layers Residuais / Skip Connections: aproveitando a inspiração na ResNet, decidiu-se avaliar o impacto que layers residuais teriam no desempenho final. A princípio, a inclusão de um Layer Residual inclusive teve impacto negativo (diminui a precisão final), mas após aumentar a profundidade das camadas "puladas", foram a chave para conseguir chegar aos 70%. A teoria atual é de que, como inicialmente a rede era menor, o "caos" gerado por esses layers na loss era maior do que os problema de vanishing e exploding gradient que eles buscam resolver. Porém, conforme a rede foi ficando maior, os ganhos superaram as perdas.

    	- Adição de um layer convolucional com um kernel 2x2, stride 2 e um número alto de filtros. Honestamente, é ainda um pouco misterioso, mas a teoria é que talvez essa quantidade alta de filtros permita que diversas features diferentes sejam absorvidos e passados pra frente na rede. Possívelmente porque, ele efetivamente "diminui" a resolução da imagem de forma diferente e assim facilita a detecção de features de vários tamanhos (?). Mexer nesse layer foi o que fez a rede chegar em quase 75%.

    	Após esses resultados satisfatórios com o CIFAR-10, foi a hora de apresentar o modelo a outros datasets.

    	Ele foi bem mal com o CIFAR-100: 30% de precisão. Porém, testes mostraram uma lição valiosa: tirar os layers densos que formavam a cabeça (get_basic_head no notebook) e deixar apenas o GlobalAveragePooling aumentou a precisão em 5%. Vamos voltar para o CIFAR-100 depois.

    	O MNIST foi trivial: mais de 99% no conjunto de testes já no primeiro treinamento, mesmon após reduzir significativamente o número de filtros para a
    	O Fashion MNIST também: 91% no primeiro treinamento.

    	Apesar desses dois datasets serem bastante simples e o resultado satisfatório neles não ser muito surpreendente, eles revelam uma particularidade bastante interessante sobre o modelo: sua resistência a overfitting parece ser alta, uma vez que em ambos os casos, mesmo com datasets simples, o modelo conseguiu resultados parecidos nos conjuntos de treino e teste. Isso possívelmente se dá pela natureza completamente convolucional da rede (que é invariante ao tamanho) e pelos layers de dropout, que dificulta que certos neurônios "decorem" o conjunto de treino.

    	Por fim, decidiu-se voltar aos básicos e cortar alguns dos layers convolucionais e residuais do final, o que aumentou em cerca de uns 4% a precisão dos modelos, indicando que talvez estivesse ocorrendo um pouco de overfitting.

    	Nota: treinando esses modelos, foram recebidos 3 "soft-bans" do Google Collab por uso excessivo de recursos.

    	Nota2: Existe uma versão "expensive" dessas redes, que não faz o downsampling (essencialmente não usa maxpoolings e muda o stride da primera camada para 1).
    	Essa versão precisou ser treinada no Collab Pro, já que precisa de muito processamento então não resultados dela não estão inclusos, mas o modelo está lá. Ela conseguiu 81.07% no CIFAR-10 e 51.93% no CIFAR-100.
