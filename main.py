import tkinter as tk
from tkinter import messagebox
import requests


# Função para obter a taxa de câmbio
def obter_taxa_cambio(api_key, moeda_origem, moeda_destino):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_origem}"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()

            if dados["result"] == "success":
                taxa = dados["conversion_rates"].get(moeda_destino)
                if taxa:
                    return taxa
                else:
                    messagebox.showerror("Erro", f"Moeda {moeda_destino} não encontrada.")
                    return None
            else:
                messagebox.showerror("Erro", "Erro ao obter dados da API. Result: failure.")
                return None
        else:
            messagebox.showerror("Erro", f"Erro ao acessar a API. Status: {resposta.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro na requisição: {str(e)}")
        return None


# Função para converter o valor
def converter_moeda():
    valor = entry_valor.get().strip()  # Remove espaços extras

    # Exibir o valor que o usuário digitou (para depuração)
    print(f"Valor digitado: '{valor}'")

    if not valor:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        return

    # Tentar substituir vírgula por ponto e converter para float
    valor = valor.replace(",", ".")

    try:
        valor = float(valor)  # Converte para número flutuante
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        return

    moeda_origem = combo_origem.get()
    moeda_destino = combo_destino.get()

    taxa = obter_taxa_cambio(api_key, moeda_origem, moeda_destino)

    if taxa:
        resultado = valor * taxa
        label_resultado.config(text=f"{valor} {moeda_origem} = {resultado:.5f} {moeda_destino}")
    else:
        label_resultado.config(text="Erro na conversão.")


# Criando a janela principal
root = tk.Tk()
root.title("Conversor de Moedas")

# Definindo a chave da API
api_key = "d720029456592b339a868ec9"  # Substitua pela sua chave da API

# Labels
label_titulo = tk.Label(root, text="Conversor de Moedas", font=("Arial", 16))
label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

label_valor = tk.Label(root, text="Valor:")
label_valor.grid(row=1, column=0, padx=10, pady=5)

# Entry para o valor
entry_valor = tk.Entry(root)
entry_valor.grid(row=1, column=1, padx=10, pady=5)

label_origem = tk.Label(root, text="Moeda de Origem:")
label_origem.grid(row=2, column=0, padx=10, pady=5)

# ComboBox para seleção de moedas
def obter_moedas_disponiveis(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados["result"] == "success":
                # Retorna apenas os códigos das moedas (ex: 'USD', 'BRL', etc.)
                return [codigo for codigo, nome in dados["supported_codes"]]
            else:
                messagebox.showerror("Erro", "Erro ao obter lista de moedas.")
                return []
        else:
            messagebox.showerror("Erro", f"Erro ao acessar a API. Status: {resposta.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro na requisição: {str(e)}")
        return []

moedas = obter_moedas_disponiveis(api_key)
if not moedas:
    moedas = ["USD", "BRL", "EUR"]  # fallback para caso a API falhe
combo_origem = tk.StringVar()
combo_origem.set(moedas[0])
dropdown_origem = tk.OptionMenu(root, combo_origem, *moedas)
dropdown_origem.grid(row=2, column=1, padx=10, pady=5)

combo_destino = tk.StringVar()
combo_destino.set(moedas[1])
dropdown_destino = tk.OptionMenu(root, combo_destino, *moedas)
dropdown_destino.grid(row=3, column=1, padx=10, pady=5)

label_destino = tk.Label(root, text="Moeda de Destino:")
label_destino.grid(row=3, column=0, padx=10, pady=5)

# ComboBox para seleção de moedas
combo_destino = tk.StringVar()
combo_destino.set(moedas[1])
dropdown_destino = tk.OptionMenu(root, combo_destino, *moedas)
dropdown_destino.grid(row=3, column=1, padx=10, pady=5)

# Botão para realizar a conversão
botao_converter = tk.Button(root, text="Converter", command=converter_moeda)
botao_converter.grid(row=4, column=0, columnspan=2, pady=10)

# Label para exibir o resultado
label_resultado = tk.Label(root, text="Resultado: ", font=("Arial", 12))
label_resultado.grid(row=5, column=0, columnspan=2, pady=10)

# Iniciar a interface gráfica
root.mainloop()
