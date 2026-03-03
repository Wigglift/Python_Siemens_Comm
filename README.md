# Comunicação PLC Siemens com Python (Snap7)

## 📌 Descrição

Projeto desenvolvido para realizar a comunicação entre PLCs da Siemens e aplicações em Python utilizando a biblioteca **Snap7**.

O programa estabelece conexão com o PLC, acessa uma **Data Block (DB)** específica, extrai os dados de uma ferramenta de prensa industrial e gera automaticamente um arquivo `.txt` contendo as informações coletadas.

---

## 🏗️ Arquitetura do Projeto

O fluxo de funcionamento é o seguinte:

1. Configuração dos parâmetros de conexão (IP, Rack e Slot)
2. Conexão com o PLC Siemens via Snap7
3. Leitura da Data Block (DB)
4. Conversão dos dados brutos para os tipos corretos
5. Geração de arquivo `.txt` com os dados extraídos
6. Mantém o arquivo `.txt` sendo atualizado com os dados a cada meio segundo

---

## ⚙️ Tecnologias Utilizadas

- Python 3.14
- Snap7 (python-snap7)
- PLC Siemens (S7-300, podendo se comunicar com a linha 400, 1200 e 1500)

---

## 🔌 Requisitos

Antes de executar o projeto, é necessário:

- PLC configurado e acessível via rede
- Data Block com permissão de acesso externo (PUT/GET habilitado)
- Python instalado
- Biblioteca Snap7 instalada

Instalação do Snap7:

```bash
pip install python-snap7
