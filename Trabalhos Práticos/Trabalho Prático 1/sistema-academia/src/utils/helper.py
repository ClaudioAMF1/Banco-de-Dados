# src/utils/helper.py
import re

def validar_cpf(cpf):
    return bool(re.match(r'^\d{11}$', cpf))

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))

def validar_telefone(telefone):
    return bool(re.match(r'^\d{11}$', telefone))

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_telefone(telefone):
    return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"