import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

def verificar_jogos(planilha, numeros_sorteados):
    try:
        # Carregan a planilha
        df = pd.read_excel(planilha)
        
        # Verificando se as colunas esperadas estão na planilha
        if 'Nome' not in df.columns or 'Jogo' not in df.columns:
            messagebox.showerror("Erro", "A planilha deve conter as colunas 'Nome' e 'Jogo'.")
            return None
        
        # Convertendo os jogos no formato separado por hífens para listas de números
        df['Jogo'] = df['Jogo'].apply(lambda x: list(map(int, str(x).split('-'))))
        
        # Calculando os acertos para cada jogo
        df['Acertos'] = df['Jogo'].apply(lambda jogo: len(set(jogo) & set(numeros_sorteados)))
        
        # Ordenando os jogadores pelo número de acertos (decrescente)
        df = df.sort_values(by='Acertos', ascending=False)
        
        return df
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a planilha: {e}")
        return None

def gerar_numeros_sorteados():
    return random.sample(range(1, 61), 6)

def selecionar_arquivo():
    filename = filedialog.askopenfilename(title="Escolha o arquivo da planilha", filetypes=[("Excel files", "*.xlsx")])
    if filename:
        return filename
    return None

def processar_jogos():
    # Obtendo o arquivo selecionado
    planilha = selecionar_arquivo()
    if not planilha:
        return
    
    # Obtendo os números sorteados
    entrada = numeros_sorteados_entry.get()
    try:
        numeros_sorteados = list(map(int, entrada.split(',')))
    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de digitar apenas números separados por vírgula.")
        return
    
    # Processando os jogos
    resultado = verificar_jogos(planilha, numeros_sorteados)
    
    if resultado is not None:
        # Exibindo os resultados
        resultados_text.delete(1.0, tk.END)  # Limpa resultados anteriores
        for index, row in resultado.iterrows():
            resultados_text.insert(tk.END, f"{row['Nome']} - Acertos: {row['Acertos']}\n")
        
        # Salvando os resultados em uma nova planilha
        resultado.to_excel('resultado_bolao.xlsx', index=False)
        messagebox.showinfo("Sucesso", "Resultados salvos em 'resultado_bolao.xlsx'.")
    else:
        messagebox.showerror("Erro", "Não foi possível processar os jogos. Verifique os dados e tente novamente.")

# Criando a interface gráfica
root = tk.Tk()
root.title("Bolão Mega da Virada")

# Layout
tk.Label(root, text="Digite os números sorteados (separados por vírgula):").pack(padx=10, pady=5)
numeros_sorteados_entry = tk.Entry(root, width=40)
numeros_sorteados_entry.pack(padx=10, pady=5)

processar_button = tk.Button(root, text="Processar Jogos", command=processar_jogos)
processar_button.pack(padx=10, pady=10)

resultados_label = tk.Label(root, text="Resultados:")
resultados_label.pack(padx=10, pady=5)

resultados_text = tk.Text(root, width=50, height=10)
resultados_text.pack(padx=10, pady=5)

root.mainloop()
