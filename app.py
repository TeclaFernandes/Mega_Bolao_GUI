import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

def verificar_jogos(planilha, numeros_sorteados):
    try:
        df = pd.read_excel(planilha)
        
        if 'Nome' not in df.columns or 'Jogo' not in df.columns:
            messagebox.showerror("Erro", "A planilha deve conter as colunas 'Nome' e 'Jogo'.")
            return None
        
        df['Jogo'] = df['Jogo'].apply(lambda x: list(map(int, str(x).split('-'))))
        df['Acertos'] = df['Jogo'].apply(lambda jogo: len(set(jogo) & set(numeros_sorteados)))
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
    planilha = selecionar_arquivo()
    if not planilha:
        return
    
    entrada = numeros_sorteados_entry.get()
    try:
        numeros_sorteados = list(map(int, entrada.split(',')))
    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de digitar apenas números separados por vírgula.")
        return
    
    resultado = verificar_jogos(planilha, numeros_sorteados)
    
    if resultado is not None:
        resultados_text.delete(1.0, tk.END) 
        for index, row in resultado.iterrows():
            resultados_text.insert(tk.END, f"{row['Nome']} - Acertos: {row['Acertos']}\n")
        
        resultado.to_excel('resultado_bolao.xlsx', index=False)
        messagebox.showinfo("Sucesso", "Resultados salvos em 'resultado_bolao.xlsx'.")
    else:
        messagebox.showerror("Erro", "Não foi possível processar os jogos. Verifique os dados e tente novamente.")

root = tk.Tk()
root.title("Bolão Mega da Virada")
root.configure(bg="#FFF68F")

largura_janela = 500
altura_janela = 400
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
''
root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
root.resizable(False, False)

tk.Label(root, text="Digite os números sorteados (separados por vírgula):", bg="#FFF68F", font=("Arial", 13, "bold")).pack(padx=28, pady=5, anchor="w")
numeros_sorteados_entry = tk.Entry(root, width=50)
numeros_sorteados_entry.pack(padx=28, pady=5, anchor="w")

processar_button = tk.Button(root, text="Processar Jogos", command=processar_jogos, bg="#9ACD32", font=("Arial", 13, "bold"))
processar_button.pack(padx=28, pady=10, anchor="w")

resultados_label = tk.Label(root, text="Resultados:", bg="#FFF68F", font=("Arial", 13, "bold"))
resultados_label.pack(padx=28, pady=5, anchor="w")

resultados_text = tk.Text(root, width=55, height=14)
resultados_text.pack(padx=10, pady=5)

root.mainloop()