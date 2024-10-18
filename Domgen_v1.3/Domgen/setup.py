from setuptools import setup, find_packages

setup(
    name='domgen',
    version='1.3',
    description='Atualiza o DuckDNS com o IP do adaptador VPN.',
    author='Seu Nome',
    author_email='johnathan.frabetti@lecom.com.br',
    packages=find_packages(),
    install_requires=[
        'requests',  # Para requisições HTTP
        'psutil',    # Para obter informações sobre processos e uso do sistema
    ],
    entry_points={
        'console_scripts': [
            'duckdns_updater=domgen:main',  # Nome do arquivo é duckdns_updater.py
        ],
    },
    python_requires='>=3.6',  # Especifica a versão mínima do Python
)
