# Sand box Python

Este projeto foi desenvolvido em pouco mais de 2 dias durante um fim de semana. A principal motivação para sua criação foi a nostalgia de um jogo de navegador da minha infância, o [Powder Game](https://dan-ball.jp/en/javagame/dust/). O objetivo foi criar algo semelhante ao jogo original, embora, no meu projeto, existam apenas 6 tipos diferentes de elementos, em contraste com a grande variedade do jogo original.

# Índice

1. [Sand Box Python](#sand-box-python)
2. [Dificuldades e Como As Contornei](#dificuldades-e-como-as-contornei)
   1. [Problemas](#problemas)
   2. [Solução Parcial](#solução-parcial)
   3. [Solução Final](#solução-final)
3. [Como Executar e Instalar](#como-executar-e-instalar)
4. [Configurando Propriedades](#configurando-propriedades)
5. [Elementos](#elementos-e-comandos)
6. [Contribuições](#contribuições)
7. [Licença](#licença)
8. [Contato](#contato)

# Dificuldades e Como As Contornei

A ideia original era desenvolver o jogo em uma engine como Unity ou Unreal. No entanto, devido ao tempo limitado, optei por usar uma tecnologia com a qual já tinha familiaridade: Python.

## Problemas

O principal problema surgiu ao tentar iniciar o jogo com [Python](https://www.python.org/) puro, usando arrays nativos para uma tela de 500x500 pixels, resultando em um array com 250.000 itens. Percorrer cada item a cada quadro resultava em um desempenho muito ruim, com apenas 1 a 5 fps sem mencionar o uso de memória, que era gigantesco.

## Solução Parcial

Para melhorar a performance, substituí o array nativo por um array do [NumPy](https://numpy.org/), que oferece vantagens significativas em termos de desempenho e uso de memória. Cada pixel foi representado por 5 números `uint8`, o que resultou em uma melhoria modesta, alcançando 5 a 10 fps, mas ainda não o suficiente para uma jogabilidade aceitável.

### por que 5 numeros?

```python
    class Types(Enum):
        BG =     (0, 0, 0, 0, 0)
        SAND =   (203, 189, 147, 1, 0)
        WATER =  (28, 163, 236, 2, 0)
        STONE =  (115, 112, 112, 3, 0)
        VACUUM = (20, 20, 20, 4, 0)
        CLONER = (108, 60, 12, 5, 0)
```

- Os três primeiros números representam a cor do pixel, permitindo leves variações dentro do mesmo elemento.
- O quarto valor é o ID do pixel, por exemplo, o ID da água é 2.
- O último valor é para dados adicionais, utilizado principalmente pelo elemento "cloner", mas pode ser usado para outros tipos de elementos, se necessário.

Dessa forma, cada pixel na minha tela é representado por 5 números uint8, totalizando 5 bytes por pixel. Para um array de 250.000 pixels, isso resulta em 1.250.000 bytes ou 1,25 MB, um valor baixo e eficiente.

#### python + numpy 320 x 320 exemplo AVG: 7 fps

![python and numpy example](https://github.com/LucasKalil-Programador/sand-box-python/blob/master/gifs/python+numpy.gif)

## Solução Final

Recentemente, descobri a possibilidade de compilar código em tempo de execução (JIT) usando [Numba](https://numba.pydata.org/). Embora o Numba tenha algumas limitações quanto aos tipos de dados que pode manipular, consegui adaptar o código para utilizá-lo. Isso resultou em um aumento drástico na performance, elevando a taxa de quadros para 150 a 200 fps, tornando o jogo jogável.

#### python + numpy + numba 1000 x 1000 exemplo AVG: 120 fps

![python and numpy example](https://github.com/LucasKalil-Programador/sand-box-python/blob/master/gifs/python+numpy+numba.gif)

# Como Executar e Instalar

```bash

     # Clone o repositório
    git clone https://github.com/LucasKalil-Programador/sand-box-python.git

    # Acesse a pasta do projeto
    cd sand-box-python

    # Crie um novo ambiente virtual
    python -m venv .venv

    # Ative o ambiente virtual
    # No Windows:
    .venv\Scripts\activate
    # No macOS/Linux:
    source .venv/bin/activate

    # Atualize o pip para a versão mais recente
    python -m pip install --upgrade pip

    # Instale as dependências do projeto
    pip install .

    # Execute o código
    python main.py
```

# configurando propiedades

Para ajustar as configurações básicas do jogo, abra o arquivo [main.py](./main.py). No final do arquivo, você encontrará a instância da classe Game, onde é possível modificar as propriedades. Veja o exemplo abaixo:

```python
    game = Game(size=(160, 160), fps=120, scale=4, font_size=30, test_mode=False)
    game.run()
```

- `size`: Define o tamanho da tela como uma tupla (largura, altura).
- `scale`: Define o multiplicador do tamanho da janela. Por exemplo, com size=(160, 160) e scale=4, a janela será de 640x640 pixels (160 \* 4).
- `fps`: Define a taxa de quadros por segundo.
- `font_size`: Define o tamanho da fonte.
- `test_mode`: Ativa ou desativa o modo de teste. Quando ativado, um elemento aleatório é gerado em um local aleatório a cada quadro, o que é útil para testar a performance e a estabilidade.

# Elementos e Controle

- `Background` elemento padrao nao possui nenhum efeito especial
- `Sand` comportase como areia possui gravidade e afunda na agua
- `Water` simula um fluido portanto tende a se acomodar e escorrer em superficies
- `Stone` elemento estatico nao se move e impede a passagem de outros elemento
- `Vacuum` exclui elementos que entram em contato
- `Cloner` copia o primeiro elemento que o toca e gera mais desse elemento a cada quadro

## Controle

- Números de `1 a 6` controlam o elemento selecionado, seguindo a ordem anterior.
- Use o botão esquerdo do mouse para gerar (spawn) o novo elemento.
- Pressione a tecla `+` para aumentar o tamanho do spawn e `-` para diminuir.
- Segure `CTRL` + `+` ou `CTRL` + `-` para aumentar ou diminuir o tamanho do spawn em incrementos de 10.

### exemplo

![exemplo](https://github.com/LucasKalil-Programador/sand-box-python/blob/master/gifs/example1.gif)

# Contribuições

Infelizmente, este projeto está descontinuado. Caso você queira fazer alguma adição ou melhoria, sinta-se à vontade para fazer um fork e modificar o código para uso próprio.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](./LICENCE) para mais detalhes.

## Contato

Lucas - [lucas.prokalil2020@outlook.com](mailto:lucas.prokalil2020@outlook.com)

Repositório no GitHub: [sand-box-python](https://github.com/LucasKalil-Programador/sand-box-python)
