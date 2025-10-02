# 🎨 Processador de Imagens com Paralelismo

Sistema de processamento de imagens com filtros aplicados usando threads Python.

## 🚀 Como Usar

### Processar uma imagem:
```bash
python image_processor.py sua_imagem.jpg filtro
```

### Filtros disponíveis:
- `sepia` - Tons clássicos marrom/amarelo
- `vintage` - Contraste + saturação + blur
- `black_white` - Preto e branco com contraste
- `sharpen` - Aumenta a nitidez
- `blur` - Aplica desfoque

## 📁 Estrutura

```
├── image_processor.py     # Processador principal
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
├── minhas_imagens/        # Suas imagens (coloque aqui)
├── output/                # Imagens processadas
└── venv/                  # Ambiente virtual
```

## 🔧 Instalação

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências (já instaladas)
pip install -r requirements.txt
```

## 💡 Exemplos

```bash
# 1. Coloque suas imagens na pasta minhas_imagens/
cp /caminho/para/sua/foto.jpg minhas_imagens/

# 2. Processe com diferentes filtros
python image_processor.py minhas_imagens/foto.jpg sepia
python image_processor.py minhas_imagens/foto.jpg vintage
python image_processor.py minhas_imagens/foto.jpg black_white
```

## 📊 Resultados

- Imagens processadas são salvas em `output/`
- Logs detalhados são gerados em `image_processing.log`
- Processamento com paralelismo interno (3 threads)