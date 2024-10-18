#!/usr/bin/env python3

import argparse
import requests
import socket
import psutil
import time
import platform
import os
import subprocess
import json
import sys
from datetime import datetime
import ctypes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "duckdns_config.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "duckdns_update.log")
pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')

def log_message(message):
    """ Registra mensagens com timestamps no arquivo de log. """
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def mostrar_loading(message, duration=6):
    """ Mostra uma animação de loading no console. """
    spin_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    spin_delay = 0.1
    spin_index = 0
    end_time = time.time() + duration
    while time.time() < end_time:
        print(f"\r{message} {spin_chars[spin_index]}", end='', flush=True)
        spin_index = (spin_index + 1) % len(spin_chars)
        time.sleep(spin_delay)
    print("\r" + " " * 50 + "\r", end='', flush=True)

def mostrar_banner():
    """ Exibe o banner do script. """
    banner = """
    
████████▄   ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄██████▄     ▄████████ ███▄▄▄▄   
███   ▀███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███ ███▀▀▀██▄ 
███    ███ ███    ███ ███   ███   ███   ███    █▀    ███    █▀  ███   ███ 
███    ███ ███    ███ ███   ███   ███  ▄███         ▄███▄▄▄     ███   ███ 
███    ███ ███    ███ ███   ███   ███ ▀▀███ ████▄  ▀▀███▀▀▀     ███   ███ 
███    ███ ███    ███ ███   ███   ███   ███    ███   ███    █▄  ███   ███ 
███   ▄███ ███    ███ ███   ███   ███   ███    ███   ███    ███ ███   ███ 
████████▀   ▀██████▀   ▀█   ███   █▀    ████████▀    ██████████  ▀█   █▀  
                                    
"""
    print(banner)

def get_adapter_ip():
    """Obtém o IP dos adaptadores disponíveis, priorizando VPNs e interfaces com IPs privados."""
    try:
        for iface_name, iface_addresses in psutil.net_if_addrs().items():
            for addr in iface_addresses:
                if addr.family == socket.AF_INET:
                    ip = addr.address
                    if ip.startswith(("10.", "172.", "192.168.")):
                        if any(keyword in iface_name.lower() for keyword in ['tun', 'vpn', 'openvpn', 'enp', 'eth0', 'wlp', 'wlan0', 'ethernet']):
                            return ip
        
        print(f"[-] Nenhum adaptador VPN ou de rede privada encontrado.")
        log_message("[-] Nenhum adaptador VPN ou de rede privada encontrado.")
    except Exception as e:
        print(f"[-] Erro ao obter o IP do adaptador: {e}")
        log_message(f"[-] Erro ao obter o IP do adaptador: {e}")
    
    return None

def atualiza_duckdns(domain, ip_interno, token):
    """ Atualiza o DuckDNS com o IP atual. """
    url = f"https://www.duckdns.org/update?domains={domain}&token={token}&ip={ip_interno}"
    try:
        mostrar_loading("[*] Atualizando DuckDNS", duration=2)
        response = requests.get(url)
        if response.text == "OK":
            print(f"[+] Atualização bem-sucedida: {domain}.duckdns.org aponta agora para {ip_interno}")
            teste_icmp(domain)
        else:
            print(f"[-] Erro na atualização: {response.text}")
            log_message(f"[-] Erro na atualização do DuckDNS: {response.text}")
    except requests.RequestException as e:
        print(f"[-] Erro ao atualizar o DuckDNS: {e}")
        log_message(f"[-] Erro ao atualizar o DuckDNS: {e}")

def teste_icmp(domain):
    """ Testa a conexão ICMP com o domínio. """
    try:
        ip = socket.gethostbyname(f"{domain}.duckdns.org")
        if platform.system() == "Windows":
            command = ["ping", "-n", "2", ip]
        else:
            command = ["ping", "-c", "2", ip]
     
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"[+] Conexão ICMP com {domain}.duckdns.org bem-sucedida.")
        else:
            print(f"[-] Erro na conexão ICMP com {domain}.duckdns.org: {result.stderr}")
            log_message(f"[-] Erro na conexão ICMP com {domain}.duckdns.org: {result.stderr}")
    except Exception as e:
        print(f"[-] Erro ao conectar com {domain}.duckdns.org via ICMP: {e}")
        log_message(f"[-] Erro ao conectar com {domain}.duckdns.org via ICMP: {e}")

def config_json(token, domain, ip_interno):
    """ Salva a configuração no arquivo JSON. """
    config = {
        "token": token,
        "domain": domain,
        "ip_interno": ip_interno
    }
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)
        log_message(f"[+] Configuração salva: token={token}, domain={domain}, ip_interno={ip_interno}")
    except IOError as e:
        print(f"[-] Erro ao salvar a configuração: {e}")
        log_message(f"[-] Erro ao salvar a configuração: {e}")

def carregar_config():
    """ Carrega a configuração do arquivo JSON. """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config
        except json.JSONDecodeError as e:
            print(f"[-] Erro ao ler o arquivo de configuração: {e}")
            log_message(f"[-] Erro ao ler o arquivo de configuração: {e}")
    else:
        print(f"[-] Arquivo de configuração não encontrado: {CONFIG_FILE}")
    return None

def verificar_e_atualizar():
    """ Verifica o IP atual e atualiza o DuckDNS se necessário. """
    config = carregar_config()
    if not config:
        print(f"[-] Nenhuma configuração encontrada. Execute o script com --config para configurar.")
        log_message("[-] Erro: Nenhuma configuração encontrada ao tentar atualizar.")
        return

    token = config.get("token")
    domain = config.get("domain")
    ip_configurado = config.get("ip_interno")

    if not token or not domain:
        print(f"[-] Configuração inválida: token ou domínio não encontrados.")
        log_message("[-] Erro: Configuração inválida - token ou domínio não encontrados.")
        return

    ip_atual = get_adapter_ip()
    if ip_atual:
        if ip_atual != ip_configurado:
            print(f"[+] IP mudou. Atualizando DuckDNS...")
            atualiza_duckdns(domain, ip_atual, token)
            """Debug"""
            os.system("pause")
            config_json(token, domain, ip_atual)
        else:
            print(f"[+] O IP atual ({ip_atual}) é o mesmo que o configurado. Nenhuma atualização necessária.")
    else:
        print(f"[-] IP não encontrado.")

def verificar_dns(domain, ip_atual):
    """ Verifica se o DNS está apontando para o IP correto. """
    try:
        resposta = socket.gethostbyname(f"{domain}.duckdns.org")
        if resposta == ip_atual:
            print(f"[+] DNS está corretamente configurado para {ip_atual}.")
            return True
        else:
            print(f"[*] DNS está apontando para {resposta}, mas o IP atual é {ip_atual}.")
            return False
    except socket.gaierror as e:
        print(f"[+] Erro ao consultar o DNS: {e}")
        log_message(f"[+] Erro ao consultar o DNS: {e}")
        return False

def verificar_permissoes_admin():
    """ Verifica se o script está sendo executado com permissões de administrador no Windows. """
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False
    return is_admin

def reexecutar_como_admin():
    """ Reexecuta o script com permissões de administrador no Windows. """
    if not verificar_permissoes_admin():
        print(f"[*] Reexecutando com permissões de administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

def configurar_cron():
    """ Configura um cron job ou uma tarefa agendada para executar o script periodicamente. """
    file_name = "domgen.py"
    config = carregar_config()
    if not config:
        print(f"[-] Nenhuma configuração encontrada. Execute o script com --config para configurar.")
        log_message("[-] Erro: Nenhuma configuração encontrada ao tentar configurar o cron job ou tarefa agendada.")
        return
    
    token = config.get("token")
    domain = config.get("domain")
    if not token or not domain:
        print(f"[-] Configuração inválida: token ou domínio não encontrados.")
        log_message("[-] Erro: Configuração inválida - token ou domínio não encontrados.")
        return

    executavel_path = os.path.join(SCRIPT_DIR, file_name)
    
    if platform.system() == "Windows":
        reexecutar_como_admin()
        task_name = "DuckDNSUpdaterTask"
        command = f'schtasks /create /tn "{task_name}" /tr "{pythonw_path} {executavel_path} --update" /sc minute /mo 1 /f'
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"[+] Tarefa agendada configurada com sucesso para executar a cada minuto.")
            log_message("[+] Tarefa agendada configurada com sucesso para executar a cada minuto.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Erro ao configurar a tarefa agendada: {e}")
            log_message(f"[-] Erro ao configurar a tarefa agendada: {e}")
    else:
        cron_job = f"* * * * * {sys.executable} {executavel_path} --update\n"
        try:
            crontab = subprocess.check_output(['crontab', '-l']).decode('utf-8')
        except subprocess.CalledProcessError:
            crontab = ""

        if cron_job not in crontab:
            crontab += cron_job
            try:
                with open('domgencron', 'w') as f:
                    f.write(crontab)
                subprocess.run(['crontab', 'domgencron'], check=True)
                os.remove('domgencron')
                print(f"[+] Cron job configurado para executar a cada minuto.")
                log_message("[+] Cron job configurado para executar a cada minuto.")
            except Exception as e:
                print(f"[-] Erro ao configurar o cron job: {e}")
                log_message(f"[-] Erro ao configurar o cron job: {e}")
        else:
            print(f"[*] Cron job já configurado.")

def main():
    parser = argparse.ArgumentParser(description="Atualiza o DuckDNS com o IP do adaptador VPN.")
    parser.add_argument('--config', nargs=2, help="Configura o script com o token e o domínio DuckDNS.")
    parser.add_argument('--update', help="Atualiza o DuckDNS com o IP atual.", action='store_true')
    parser.add_argument('--cron', help="Configura uma tarefa cron para execução periódica no Linux ou Windows.", action='store_true')

    args = parser.parse_args()

    mostrar_banner()

    if args.config:
        token, domain = args.config
        ip_atual = get_adapter_ip()
        if ip_atual:
            config_json(token, domain, ip_atual)
            print(f"[+] Configuração concluída com sucesso.")
        else:
            print(f"[-] Não foi possível obter o IP atual para configuração.")
            log_message("[-] Erro ao obter o IP atual para configuração.")
    elif args.update:
        verificar_e_atualizar()
    elif args.cron:
        configurar_cron()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()