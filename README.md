## _**Estudo Técnico do U-RNN em cima do artigo e repositório**_ **U-RNN high-resolution spatiotemporal nowcasting of urban flooding** 

## **1. Problema resolvido pelo U-RNN e por que ele se relaciona com inundações urbanas.** 

O U-RNN foi desenvolvido para realizar o nowcasting de inundações urbanas, ou seja, a previsão da evolução da lâmina d'água em curto prazo. Esse problema está diretamente relacionado às inundações urbanas, pois métodos hidrodinâmicos tradicionais, embora precisos, apresentam elevado custo computacional e não conseguem fornecer resultados em tempo hábil durante eventos extremos. O U-RNN utiliza técnicas de Aprendizado Profundo para aprender o comportamento das inundações a partir de simulações anteriores, produzindo previsões rápidas que podem auxiliar sistemas de monitoramento e resposta a enchentes. 

## **2. Entradas e saídas do modelo** 

O modelo recebe como entrada informações estáticas e dinâmicas do ambiente: 

- **Dados de Terreno:** Na pasta do dataset reduzido (urbanflood24_lite), o modelo lê matrizes estáticas com as características geográficas da região, que incluem a topografia/elevação (absolute_DEM.npy), o uso do solo/impermeabilidade (impervious.npy) e a localização da rede de drenagem (manhole.npy). 

- **Dados de Chuva:** As séries temporais e históricos de precipitação em milímetros que alimentam a janela deslizante ( _Sliding Window_ ) para calcular o acúmulo de água. 

Esses dados representam as características do terreno e a evolução da chuva ao longo do tempo. 

As Saídas (Outputs): 

- **Métricas e Matrizes:** Correspondem aos resultados numéricos salvos na pasta metrics/ (como a planilha Excel de validação que gerou) e as matrizes de predição em save_res_data/. 

- **Mapas Dinâmicos:** É exatamente a imagem que obteve no terminal (water_depth_spatial_temporal.png), que plota visualmente a evolução da lâmina d'água em metros (escala de 0 a 2 metros) ao longo do tempo (1 min, 12 min, 24 min e 36 min). 

As saídas são representadas por matrizes que indicam a altura da lâmina d'água em cada ponto da área estudada. 

## **3. Arquitetura U-like/ConvGRU e Sliding Window-based Pre-warming** 

A arquitetura do U-RNN combina uma estrutura do tipo U-Net com unidades recorrentes ConvGRU. A parte em formato de "U" é responsável por extrair características espaciais do terreno e da precipitação em diferentes escalas, enquanto as células ConvGRU modelam a dependência temporal dos dados, permitindo que a rede considere a evolução da inundação ao longo do tempo. 

O paradigma Sliding Window-based Pre-warming utiliza uma janela deslizante contendo os instantes anteriores à previsão para inicializar o estado interno da rede recorrente. Dessa forma, o modelo começa a previsão considerando o estado hidrológico recente da região, resultando em estimativas mais consistentes. 

## **4. Fontes utilizadas como guia técnico** 

## **Para o desenvolvimento deste trabalho foram utilizadas três fontes principais:** 

- **Artigo científico:** utilizado para compreender o problema de nowcasting de inundações, a arquitetura proposta, o método de treinamento e as métricas de avaliação (R², RMSE, MAE e CSI). 

- **Repositório oficial no GitHub:** utilizado como referência para a estrutura do projeto, arquivos de configuração, implementação da arquitetura (ConvRNN), scripts de treinamento e inferência e organização do código-fonte. 

- **Dataset UrbanFlood24 Lite e pesos pré-treinados:** utilizados para realizar a inferência em ambiente com recursos computacionais limitados, empregando a versão reduzida do conjunto de dados e os modelos disponibilizados pelos autores. 

## **Relatório de Adaptações e Configuração de Ambiente: Projeto U-RNN high-resolution spatiotemporal nowcasting of urban flooding** 

O objetivo deste trabalho foi adaptar o fluxo de execução e a arquitetura do modelo U-RNN para possibilitar sua execução em um computador da biblioteca da instituição, o qual possui recursos computacionais limitados e não dispõe de placa de vídeo dedicada (GPU NVIDIA). Dessa forma, toda a execução foi realizada exclusivamente em CPU, exigindo modificações na configuração do ambiente e em alguns trechos do código-fonte para garantir a compatibilidade do modelo. 

A primeira adaptação consistiu na substituição do conjunto de dados UrbanFlood24 pela versão UrbanFlood24 Lite. Essa escolha foi motivada pelas limitações de armazenamento em disco e memória RAM do computador disponível na biblioteca, uma vez que a versão completa do dataset ocupa aproximadamente 115 GB. A versão Lite possui menor resolução espacial e temporal, reduzindo significativamente a demanda por recursos computacionais e permitindo sua utilização em máquinas convencionais. 

Outra alteração importante foi a utilização dos pesos pré-treinados disponibilizados pelos autores do projeto, em vez de realizar o treinamento completo do modelo. Segundo a documentação oficial, o treinamento foi desenvolvido para ser executado em GPUs de alto desempenho, como uma NVIDIA RTX 4090, levando cerca de três horas para ser concluído. Como o computador da biblioteca não possui placa de vídeo dedicada e utiliza apenas o processador para processamento, o treinamento do zero seria inviável, podendo levar vários dias para ser concluído. Assim, optou-se pela utilização dos pesos já treinados, permitindo executar apenas a etapa de inferência. 

Também foram realizadas modificações no arquivo de configuração _lite.yaml_ . O parâmetro **use_checkpoint** , originalmente configurado como **true** , foi alterado para **false** , pois o mecanismo de _Gradient Checkpointing_ do PyTorch foi desenvolvido para otimizar o uso de memória durante o treinamento em GPUs e realiza chamadas relacionadas ao ambiente CUDA. Como não havia suporte a CUDA no equipamento utilizado, sua desativação foi necessária para evitar erros de execução. Além disso, o parâmetro **num_workers** foi alterado de **4** para **0** , centralizando o carregamento dos dados na thread principal. Essa configuração é recomendada em ambientes Windows para evitar problemas de sincronização e falhas no funcionamento do _DataLoader_ . 

Na execução dos testes, o parâmetro **--device 0** , destinado ao processamento em GPU, foi substituído por **--device cpu** , garantindo que toda a inferência fosse realizada utilizando exclusivamente o processador do computador da biblioteca. 

Além das alterações nos arquivos de configuração, foi necessária uma modificação direta no código-fonte do projeto. No arquivo **src/lib/model/networks/ConvRNN.py** , a instrução **.cuda()** , responsável por enviar tensores diretamente para a memória da placa de vídeo, foi substituída por **.cpu()** . Essa alteração eliminou a dependência de hardware gráfico dedicado, permitindo que todos os cálculos fossem executados utilizando apenas a memória RAM e a CPU. 

Essas adaptações permitiram compatibilizar o modelo com um ambiente significativamente mais simples do que o recomendado pelos desenvolvedores. A utilização da versão Lite do benchmark, que reduz a resolução espacial em quatro vezes e a resolução temporal em dez vezes, resultando em imagens de 128 × 128 pixels distribuídas em 36 passos de tempo, diminuiu o custo computacional da inferência. Da mesma forma, o uso de pesos pré-treinados eliminou a necessidade de um processo de treinamento extremamente demorado, tornando viável a execução do projeto no computador da biblioteca. 

Após as adaptações, o modelo concluiu com sucesso todos os cenários de teste em aproximadamente 83 segundos. Os resultados obtidos foram compatíveis com aqueles apresentados pelos autores para a versão Lite do benchmark, alcançando um coeficiente de determinação (R²) médio de 0,9890, indicando aproximadamente 98,9% de precisão na representação da dinâmica da inundação, um erro quadrático médio (RMSE) de 0,0156 metro, correspondente a cerca de 1,5 centímetro de erro na estimativa da altura da água, e um tempo médio de resposta de aproximadamente 0,58 segundo por passo de previsão, demonstrando viabilidade para aplicações de nowcasting em tempo quase real. 

Conclui-se que, mesmo utilizando um computador da biblioteca sem placa de vídeo dedicada e executando todo o processamento exclusivamente em CPU, foi possível adaptar o modelo U-RNN de forma satisfatória. As modificações realizadas garantiram a execução correta da inferência e preservaram a precisão dos resultados, demonstrando que o modelo pode ser utilizado em ambientes computacionais mais modestos quando devidamente configurado. 

Saída: 

<p align="center">
  <img src="figs/Resultados de Nowcasting U-RNN.png" alt="Resultados de Nowcasting U-RNN" width="80%">
</p>


## **4. Resultados e Evidências** 



As visualizações geradas pelo script test.py estão organizadas na pasta U-RNN/exp/20260316_130418_443889/figs/epoch@100/, sendo cada subpasta correspondente a um evento de teste (ex.: r100y_p0.5_d3h). Em cada caso, o arquivo water_depth_spatial_temporal.png apresenta a comparação entre a simulação de referência (MIKE+), as previsões do modelo U-RNN e o erro absoluto. 

A primeira linha das figuras corresponde à simulação hidrodinâmica de referência nos instantes t = 0, 11, 23 e 35. Observa-se a evolução progressiva do evento de precipitação, com expansão da área inundada ao longo do domínio e aumento das profundidades da lâmina d’água. As maiores acumulações ocorrem em regiões de convergência do escoamento e canais principais da malha urbana, atingindo valores próximos de 2,0 m. 

A segunda linha apresenta as previsões do modelo U-RNN para os mesmos instantes. Verifica-se elevada concordância com a referência, tanto em termos espaciais quanto temporais. O modelo reproduz adequadamente os padrões de propagação da inundação e a dinâmica de crescimento das áreas alagadas, mantendo consistência com o desempenho global reportado (R² ≈ 98,9%). 

A terceira linha corresponde ao erro absoluto, definido como |y_pred − y_ref| e expresso em metros. Os maiores desvios concentram-se nas regiões de transição da frente de inundação, especialmente nas fases iniciais do evento. Com a evolução temporal, observa-se redução progressiva do erro e predominância de valores baixos ao longo do domínio. O erro médio global é de RMSE = 0,0156 m (≈ 1,56 cm), indicando elevada precisão do modelo. 

O comportamento espaço-temporal do evento, representado nos instantes de 1, 12, 24 e 36 minutos, evidencia inicialmente um sistema em fase de resposta à precipitação, ainda sem acumulações significativas. Na fase intermediária ocorre rápida expansão da inundação, com formação de zonas de acúmulo e intensificação das 

profundidades. Na fase final, observa-se tendência de estabilização do campo de escoamento, com manutenção das principais áreas inundadas e menor variação temporal. 

<p align="center">
  <img src="figs/URNN -Gráfico.png" alt="Resultados de Nowcasting U-RNN" width="80%">
</p>

## **Análise do Processo de Treinamento e Limitações de Hardware** 

O treinamento do U-RNN não foi realizado neste trabalho devido às limitações do ambiente computacional utilizado. Conforme descrito na documentação oficial, o treinamento do modelo requer uma GPU NVIDIA com suporte a CUDA e, para o cenário Lite, recomenda-se uma placa com pelo menos 8 GB de memória, sendo utilizado como referência uma NVIDIA RTX 4090, capaz de concluir aproximadamente 1000 épocas em cerca de 3,5 horas. Como o computador da biblioteca utilizado neste projeto possui apenas CPU com gráficos integrados, sem GPU dedicada, a execução do treinamento seria inviável devido ao elevado tempo de processamento e ao alto consumo de memória. 

Dessa forma, optou-se pela utilização dos pesos pré-treinados disponibilizados pelos autores do projeto, permitindo executar apenas a etapa de inferência. Essa abordagem é prevista pela própria documentação e possibilita avaliar o desempenho do modelo sem a necessidade de repetir o treinamento. O treinamento original é realizado pelo script **main.py** , responsável por carregar o conjunto de dados, inicializar a arquitetura U-RNN, calcular a função de perda e atualizar iterativamente os pesos da rede. Ao final do treinamento, são gerados arquivos de checkpoint (.pth.tar), que armazenam os pesos aprendidos. Neste trabalho foi utilizado o checkpoint **checkpoint_143_0.065581453.pth.tar** , correspondente ao modelo pré-treinado disponibilizado pelos autores. 

Além disso, o projeto disponibiliza um módulo para otimização do modelo utilizando **TensorRT** (urnn_to_tensorrt.py) e suporte ao treinamento distribuído por múltiplas GPUs por meio do **Distributed Data Parallel (DDP)** . Entretanto, esses recursos dependem de hardware NVIDIA e do ambiente CUDA, não sendo compatíveis com o computador utilizado. 

Mesmo com essas restrições, todas as etapas de inferência foram executadas com sucesso utilizando apenas a CPU. Os resultados obtidos mantiveram desempenho consistente e qualidade compatível com os valores reportados pelos autores, demonstrando que o U-RNN pode ser utilizado para avaliação e validação do modelo mesmo em ambientes computacionais sem GPU dedicada. 

## **4. Aplicação ao Americas Techguard** 

O modelo U-RNN pode apoiar a **Americas TechGuard** no monitoramento e na gestão de inundações urbanas ao realizar o **nowcasting** da evolução da lâmina d'água com baixo tempo de resposta. A partir de dados de precipitação e características do terreno, o modelo gera mapas dinâmicos de inundação que podem auxiliar na identificação antecipada de áreas críticas, emissão de alertas preventivos e apoio à tomada de decisão por órgãos como a Defesa Civil e gestores municipais. 

Em uma aplicação operacional, o U-RNN pode ser integrado a dados em tempo real provenientes de radares meteorológicos, sensores hidrológicos, estações pluviométricas, imagens de satélite e Sistemas de Informação Geográfica (SIG). Essa integração possibilita a atualização contínua das previsões, a geração de alertas georreferenciados e a avaliação de impactos sobre infraestruturas críticas, como hospitais, escolas, vias de transporte e redes de energia. 

A solução desenvolvida neste trabalho corresponde a uma validação acadêmica da arquitetura, utilizando o dataset **UrbanFlood24 Lite** , pesos pré-treinados e execução em CPU. Para uma Prova de Conceito (PoC) em ambiente real, seria necessária a utilização de dados hidrológicos em tempo real, modelos calibrados para a região de interesse, infraestrutura computacional com suporte a GPUs e integração com plataformas de monitoramento e resposta a desastres. 

## **Guia de Confecção e Execução do U-RNN (CPU / Windows) confeccionado a partir do repositório holmescao/U-RNN** 

Este guia descreve o procedimento utilizado para configurar e executar o projeto **U-RNN** em um computador com sistema operacional Windows utilizando exclusivamente a CPU, uma vez que o equipamento não possui placa de vídeo NVIDIA. 

## **1. Clonando o repositório** 

Crie uma pasta para armazenar o projeto. Em seguida, abra o **Anaconda Prompt** (ou outro terminal) nessa pasta e execute: 

git clone https://github.com/holmescao/U-RNN cd U-RNN 

## **2. Instalação do Anaconda ou Miniconda** 

Caso o computador ainda não possua o Anaconda ou Miniconda instalado: 

1. Acesse o site oficial do **Anaconda** ou **Miniconda** . 

2. Baixe a versão para Windows. 

3. Execute o instalador seguindo as configurações padrão. 

4. Ao final da instalação, abra o **Anaconda Prompt** . 

## **3. Criação do ambiente virtual** 

Crie um ambiente virtual utilizando o Python 3.10 e ative-o: 

conda create -n urnn python=3.10 -y conda activate urnn 

## **4. Abrindo o projeto** 

Entre na pasta do projeto e abra-o no Visual Studio Code: 

cd caminho_da_pasta\U-RNN code . 

Depois, acesse a pasta onde estão os scripts: 

cd code 

## **5. Instalação das dependências** 

Instale inicialmente a versão do PyTorch destinada exclusivamente à execução em CPU: 

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu 

Em seguida, instale as demais dependências do projeto: 

pip install -r requirements.txt 

## **6. Download do conjunto de dados** 

Neste projeto foi utilizada a versão **UrbanFlood24 Lite** , recomendada para computadores com recursos limitados. 

Faça o download do conjunto de dados no link: 

https://drive.google.com/file/d/1_P4tNlYCneCmKr2X9r-TAoiCKk1-AauI/view?usp=sharing 

Após o download: 

1. Crie uma pasta chamada **data** na raiz do projeto **U-RNN** 

2. Extraia o conteúdo do arquivo nessa pasta. 

A estrutura deverá ficar semelhante à seguinte: 

U-RNN/ ├── data/ │   └── urbanflood24_lite/ 

- │       ├── train/ 

- │       │   ├── flood/ 

│       │   └── geodata/ 

│       └── test/ └── code/ 

Todos os scripts deverão ser executados a partir da pasta **code** . 

## **7. Download dos pesos pré-treinados** 

Como o computador utilizado não possui GPU dedicada, o treinamento completo do modelo não foi realizado. Para a inferência foram utilizados os pesos pré-treinados disponibilizados pelos autores. 

Faça o download em: 

https://drive.google.com/file/d/1ehvXWkLBMoa4Jvf4l_KtM734ZIaw_7DK/view?usp=sharing 

Após o download: 

1. Crie uma pasta chamada **exp** na raiz do projeto. 

2. Extraia o conteúdo do arquivo nessa pasta. 

A estrutura deverá ficar semelhante a: 

U-RNN/ └── exp/ └── 20260316_130418_443889/ └── save_model/ └── checkpoint_143_0.065581453.pth.tar 

## **8. Ajustes de compatibilidade para execução em CPU** 

Como o código original foi desenvolvido para execução em GPU com suporte ao CUDA, algumas adaptações foram necessárias para permitir sua execução em um computador Windows utilizando apenas a CPU. 

## **8.1 Alterações no arquivo code/configs/lite.yaml** 

Abra o arquivo **lite.yaml** e altere os seguintes parâmetros: 

num_workers: 0 use_checkpoint: false 

Essas alterações possuem as seguintes finalidades: 

- **num_workers: 0** : evita erros relacionados ao carregamento paralelo de dados ( _DataLoader_ ) no Windows. 

- ● **use_checkpoint: false** : desativa o mecanismo de _Gradient Checkpointing_ , que realiza chamadas ao CUDA durante a execução. 

## **8.2 Alteração no arquivo code/src/lib/model/networks/ConvRNN.py** 

Abra o arquivo **ConvRNN.py** e localize a instrução: 

.cuda() 

Substitua-a por: 

.cpu() 

No trecho correspondente, o código ficará semelhante ao seguinte: 

if inputs is None: x = torch.zeros( htprev.size(0), self.input_channels, self.shape[0], self.shape[1] ).cpu() 

Essa alteração garante que todos os tensores sejam alocados na memória RAM e processados exclusivamente pela CPU. 

## **9. Executando a inferência** 

Com todas as dependências instaladas, os arquivos configurados e o ambiente virtual ativado, execute o seguinte comando na pasta **code** : 

python test.py --exp_config configs/lite.yaml --timestamp 20260316_130418_443889 --device cpu 

O parâmetro **--timestamp** indica a pasta onde foram armazenados os pesos pré-treinados. 

## **10. Validação dos resultados** 

Após a execução, o pipeline realizará automaticamente os cenários de teste utilizando apenas a CPU. Ao término do processamento, serão geradas as métricas de avaliação do modelo. 

O arquivo contendo os resultados será salvo em: 

exp/ └── 20260316_130418_443889/ └── metrics/ └── metrics_epoch100.xlsx 

O arquivo **metrics_epoch100.xlsx** reúne as principais métricas utilizadas para avaliar o desempenho do modelo durante a etapa de inferência, como o coeficiente de determinação (R²), o erro quadrático médio (RMSE) e os demais indicadores calculados pelo pipeline. 

## **11. Verificação das figuras comparativas** 

Além das métricas numéricas, o script **test.py** gera automaticamente figuras comparativas para cada cenário de teste. Essas imagens permitem analisar visualmente a qualidade das previsões produzidas pelo modelo U-RNN. 

Para visualizar os resultados, abra o seguinte diretório utilizando o Explorador de Arquivos do Windows ou o Visual Studio Code: 

U-RNN/ └── exp/ └── 20260316_130418_443889/ └── figs/ └── epoch@100/ 

Dentro dessa pasta serão encontradas subpastas correspondentes a cada um dos cenários hidrológicos avaliados (por exemplo, **r100y_p0.5_d3h** ). 

Em cada uma dessas pastas, abra a imagem: 

water_depth_spatial_temporal.png 

Essa figura apresenta uma comparação entre os resultados obtidos pelo modelo e os dados de referência, organizada em três linhas: 

- **Primeira linha:** profundidade da lâmina d'água obtida pelo modelo hidrodinâmico de referência (MIKE+); 

- **Segunda linha:** profundidade da lâmina d'água prevista pelo modelo U-RNN; 

- **Terceira linha:** mapa do erro absoluto entre a previsão do U-RNN e os valores de referência. 

A inspeção dessas figuras permite verificar visualmente a qualidade das previsões e identificar regiões onde o modelo apresentou maior ou menor erro durante o processo de nowcasting. 

Essa organização mantém a continuidade do guia, passando naturalmente da **validação numérica (métricas)** para a **validação visual (figuras)** , o que é o fluxo normalmente adotado em trabalhos acadêmicos. 

