#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

def yamlGenerate(bond0_ifaces, bond1_ifaces, bond0_ip, bond1_ip, bond0_gw, bond0_dns, output_file):
    yaml = f"""network:
  version: 2
  renderer: networkd

  ethernets:
    {bond0_ifaces[0]}: {{}}
    {bond0_ifaces[1]}: {{}}
    {bond1_ifaces[0]}: {{}}
    {bond1_ifaces[1]}: {{}}

  bonds:
    bond0:
      interfaces:
        - {bond0_ifaces[0]}
        - {bond0_ifaces[1]}
      parameters:
        mode: 802.3ad
        mii-monitor-interval: 100
        transmit-hash-policy: layer3+4
      addresses:
        - {bond0_ip}
      gateway4: {bond0_gw}
      nameservers:
        addresses:
          - {bond0_dns}

    bond1:
      interfaces:
        - {bond1_ifaces[0]}
        - {bond1_ifaces[1]}
      parameters:
        mode: 802.3ad
        mii-monitor-interval: 100
        transmit-hash-policy: layer3+4
      addresses:
        - {bond1_ip}
"""
    Path(output_file).write_text(yaml)
    print(f"Arquivo YAML foi gerado em: {output_file}")

def netplanApply():
    subprocess.run(["sudo", "netplan", "apply"])
    print("Configuração aplicada utilizando 'netplan apply'.")

def validateConfiguration():
    print("\nInterfaces configuradas:")
    subprocess.run(["ip", "a"])
    print("\nDetalhes do bond0:")
    subprocess.run(["cat", "/proc/net/bonding/bond0"])
    print("\nDetalhes do bond1:")
    subprocess.run(["cat", "/proc/net/bonding/bond1"])

def main():
    parser = argparse.ArgumentParser(description="Automação de configuração de rede via Netplan")

    parser.add_argument("--bond0", nargs=2, required=True, help="Interfaces para bond0 (ex: eno1 enp1s0f0)")
    parser.add_argument("--bond1", nargs=2, required=True, help="Interfaces para bond1 (ex: enp4s0 enp1s0f1)")
    parser.add_argument("--ip0", required=True, help="Endereço IP para bond0 (ex: 10.1.0.1/24)")
    parser.add_argument("--ip1", required=True, help="Endereço IP para bond1 (ex: 10.2.0.1/24)")
    parser.add_argument("--gw0", required=True, help="Gateway para bond0 (ex: 10.1.0.0)")
    parser.add_argument("--dns0", required=True, help="DNS para bond0 (ex: 10.1.0.100)")
    parser.add_argument("--out", default="/etc/netplan/01-auto-netplan.yaml", help="Caminho de saída do YAML")

    args = parser.parse_args()

    yamlGenerate(args.bond0, args.bond1, args.ip0, args.ip1, args.gw0, args.dns0, args.out)
    netplanApply()
    validateConfiguration()

if __name__ == "__main__":
    main()
