# Documentação do Script de Atualização DuckDNS

## Descrição Geral
Este script automatiza a atualização do endereço IP de um domínio DuckDNS. Ele detecta o IP do adaptador VPN e atualiza o domínio DuckDNS correspondente. Após a configuração inicial, o script pode ser executado automaticamente para atualizar o IP sem a necessidade de parâmetros adicionais.

## Requisitos
- **Python 3.12**: Certifique-se de que o Python 3.12 esteja instalado no seu sistema. Você pode instalar diretamente pela Microsoft Store no Windows ou pelo gerenciador de pacotes no Linux.
- **Conta no DuckDNS**: Você precisará de uma conta no DuckDNS e de um domínio configurado.

## Instalação
Baixe o script que contém o código. Para instalar as dependências, execute o comando abaixo utilizando o script `setup.py`. No **Linux Shell**, torne o script de instalação executável com `chmod +x setup.py` e instale as dependências com `./setup.py install`. No **Windows CMD** (necessário privilégios administrativos), instale as dependências usando Python com `python setup.py install`. Para configurar permissões, torne o script executável no **Linux Shell** com `chmod +x domgen.py`.

## Configuração Inicial
Configure o script com o token e o domínio DuckDNS, o que criará um arquivo de configuração JSON (`duckdns_config.json`). No **Linux Shell**, use `./domgen.py --config <token> <dominio>`. No **Windows CMD**, use `python domgen.py --config <token> <dominio>`.

## Parâmetros de Uso
- Para o parâmetro `--config`, que configura o script com o token e o domínio DuckDNS, criando o arquivo de configuração JSON, no **Linux Shell**, use `./domgen.py --config <token> <dominio>`. No **Windows CMD**, use `python domgen.py --config <token> <dominio>`.
- Para o parâmetro `--update`, que atualiza o DuckDNS usando as informações armazenadas no arquivo de configuração, no **Linux Shell**, use `./domgen.py --update`. No **Windows CMD**, use `python domgen.py --update`.
- Para o parâmetro `--cron`, que configura uma tarefa agendada para executar o script de atualização do DuckDNS a cada minuto, no **Linux Shell**, use `./domgen.py --cron`. No **Windows CMD**, use `python domgen.py --cron`.

## Logs
Todas as atividades do script, incluindo erros e sucessos, são registradas em um arquivo de log (`duckdns_update.log`) localizado no mesmo diretório do script. Verifique este arquivo para rastrear as execuções e resolver problemas.

## Considerações Finais
- **Segurança**: Mantenha o arquivo de configuração (`duckdns_config.json`) seguro, pois ele contém o token do DuckDNS.
- **Automatização**: O script pode ser configurado para executar automaticamente, garantindo atualizações regulares do IP.
- **Compatibilidade**: O script funciona tanto em sistemas Linux quanto Windows, com instruções específicas para cada plataforma.

## Documentação Adicional
Para mais informações, consulte a [documentação completa em PDF](Docs/Domgen_DOC.pdf).
