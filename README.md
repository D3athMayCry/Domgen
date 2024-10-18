# Documentação do Script de Atualização DuckDNS

## Descrição Geral

Este script automatiza a atualização do endereço IP de um domínio DuckDNS. Ele detecta o IP do adaptador VPN e atualiza o domínio DuckDNS correspondente. Após a configuração inicial, o script pode ser executado automaticamente para atualizar o IP sem a necessidade de parâmetros adicionais.

## Requisitos

- **Python 3.x**: Certifique-se de que o Python 3.x esteja instalado no seu sistema.
- **Bibliotecas Python**: Instale as seguintes bibliotecas Python:
  - argparse
  - requests
  - socket
  - psutil
  - time
  - platform
  - os
  - subprocess
  - json
  - sys
- **Conta no DuckDNS**: Você precisará de uma conta no DuckDNS e de um domínio configurado.

## Instalação

### Clonar ou Copiar o Script

Baixe o script ou clone o repositório que contém o código.

### Instalar Dependências

Execute o comando abaixo para instalar todas as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Configurar Permissões

Torne o script executável com o comando:

```bash
chmod +x domgen.py
```


# Parâmetros de Uso

### Parâmetro --config

Configura o script com o token e o domínio DuckDNS, criando o arquivo de
configuração JSON

- #### Uso:

```bash
./domgen.py --config <token> <dominio>
```

### Parâmetro --cron

Configura uma tarefa agendada (cron job) no Linux para executar o script de
atualização do DuckDNS a cada minuto.

- #### Uso:

```bash
./domgen.py --cron
```


# Configuração do Cron

O script adicionará a seguinte linha ao crontab:

```bash
* * * * * /caminho/para/o/script/domgen.py --update
```

Nota: Certifique-se de que o script domgen.py tenha permissões de execução
e que o caminho para o script esteja correto.

Para verificar a configuração do cron, execute:

```bash
crontab -l
```

# Logs

Todas as atividades do script, incluindo erros e sucessos, são registradas em
um arquivo de log (`duckdns_update.log`) localizado no mesmo diretório do
script. Verifique este arquivo para rastrear as execuções e resolver problemas.


# Exemplo de Uso Completo

## Configuração Inicial:

```bash
./domgen.py --config abc12345 meu-dominio
```

## Configuração Inicial:

```bash
./domgen.py --update
```

## Configuração Inicial:

```bash
./domgen.py --cron
```

# Considerações Finais

- `Segurança`: Mantenha o arquivo de configuração `(duckdns_config.json)`
seguro, pois ele contém o token do DuckDNS.
