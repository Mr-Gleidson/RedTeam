import requests
import sys
import asyncio
import base64
import urllib.parse
import html

# Função para testar vulnerabilidades de XSS
def testar_xss(url, ponto_injecao, payload, tipo_vulnerabilidade, metodo_http, codificacao):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Custom-Header": "valor personalizado"
    }
    cookies = {
        "session_id": "abcdef123456"
    }
    proxies = {
        "http": "http://10.10.1.10:3128",
        "https": "http://10.10.1.10:1080",
    }

    # Modifica a solicitação com base no ponto de injeção e método HTTP
    if ponto_injecao == "url":
        if metodo_http == "get":
            # Testa a vulnerabilidade de XSS no parâmetro da URL
            r = requests.get(url, params={ponto_injecao: payload}, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
        elif metodo_http == "post":
            # Testa a vulnerabilidade de XSS no parâmetro da URL
            r = requests.post(url, data={ponto_injecao: payload}, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
    elif ponto_injecao == "header":
        if metodo_http == "get":
            # Testa a vulnerabilidade de XSS no cabeçalho HTTP
            headers["X-Custom-Header"] = payload
            r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
        elif metodo_http == "post":
            # Testa a vulnerabilidade de XSS no cabeçalho HTTP
            headers["X-Custom-Header"] = payload
            r = requests.post(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
    elif ponto_injecao == "Cookie":
        if metodo_http == "get":
            # Testa a vulnerabilidade de XSS no cookie
            cookies["X-Custom-Cookie"] = payload
            r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
        elif metodo_http == "post":
            # Testa a vulnerabilidade de XSS no cookie
            cookies["X-Custom-Cookie"] = payload
            r = requests.post(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
    elif ponto_injecao == "javascript":
        if metodo_http == "get":
            # Testa a vulnerabilidade de XSS no código JavaScript
            if codificacao == "base64":
                payload = base64.b64encode(payload.encode("utf-8")).decode("utf-8")
            elif codificacao == "url":
                payload = urllib.parse.quote(payload)
            elif codificacao == "html":
                payload = html.escape(payload)
            else:
                print(f"Codificação inválida: {codificacao}")
            r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))

    # Verifica a resposta em busca do payload
    if tipo_vulnerabilidade == "refletida":
        if payload in r.text:
            print(f"VULNERABILIDADE DE XSS ENCONTRADA em {url} com payload {payload}")
        else:
            print(f"Nenhuma vulnerabilidade de XSS encontrada em {url} com payload {payload}")
    elif tipo_vulnerabilidade == "persistente":
        # Verifica a vulnerabilidade de XSS persistente
        # TODO: Implementar a verificação de XSS persistente
        pass
    else:
        print(f"Tipo de vulnerabilidade inválido: {tipo_vulnerabilidade}")

    return r

# Função assíncrona para escanear com vários payloads
async def escanear(url, payloads, tipo_vulnerabilidade, ponto_injecao, metodo_http, codificacao):
    tarefas = []
    for payload in payloads:
        tarefa = asyncio.ensure_future(testar_xss(url, ponto_injecao, payload, tipo_vulnerabilidade, metodo_http, codificacao))
        tarefas.append(tarefa)
    respostas = await asyncio.gather(*tarefas)
    return respostas

# Função principal
def principal(url, arquivo_payloads, tipo_vulnerabilidade, ponto_injecao, metodo_http, codificacao):
    with open(arquivo_payloads, "r") as f:
        payloads = f.read().splitlines()
    loop = asyncio.get_event_loop()
    respostas = loop.run_until_complete(escanear(url, payloads, tipo_vulnerabilidade, ponto_injecao, metodo_http, codificacao))
    return respostas

if __name__ == "__main__":
    url = sys.argv[1]
    arquivo_payloads = sys.argv[2]
    tipo_vulnerabilidade = sys.argv[3]
    ponto_injecao = sys.argv[4]
    metodo_http = sys.argv[5]
    codificacao = sys.argv[6]
    principal(url, arquivo_payloads, tipo_vulnerabilidade, ponto_injecao, metodo_http, codificacao)