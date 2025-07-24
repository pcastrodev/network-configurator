# Network Configurator 

Automação da configuração de interfaces de rede com agregação LACP (Netplan) para servidores Ubuntu 22.04.

Projeto desenvolvido como parte do processo seletivo para a Associação GigaCandanga.

---

## Requisitos

- Python 3.7+
- Sistema de destino: Ubuntu Server 22.04 com Netplan
- Execução recomendada com permissões de administrador (sudo)

---

## Uso (gerar arquivo YAML no Windows)

```powershell
python network_configurator.py `
  --bond0 eno1 enp1s0f0 `
  --bond1 enp4s0 enp1s0f1 `
  --ip0 10.1.0.1/24 `
  --ip1 10.2.0.1/24 `
  --gw0 10.1.0.0 `
  --dns0 10.1.0.100 `
  --out .\teste-netplan.yaml
```

---

## Uso no Ubuntu (gerar + aplicar + validar)

1. Descomente no final do script:
```python
# netplanApply()
# validateConfiguration()
```

2. Execute com sudo:
```bash
sudo python3 network_configurator.py   --bond0 eno1 enp1s0f0   --bond1 enp4s0 enp1s0f1   --ip0 10.1.0.1/24   --ip1 10.2.0.1/24   --gw0 10.1.0.0   --dns0 10.1.0.100
```

---

##  Validação

O script mostra:
- Interfaces com IPs via `ip a`
- Estado dos bonds via `/proc/net/bonding/bondX`

---

**Desenvolvido por Pedro Henrique Almeida Castro**
