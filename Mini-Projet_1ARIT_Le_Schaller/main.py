import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import random
import re

class Fleissner:
    def __init__(self, root):
        self.root = root
        self.root.title("Grilles Tournantes de Fleissner")
        self.root.geometry('550x600')
        self.root.configure(bg='#323232')
        self.create_mode = False

        self.n = simpledialog.askinteger("Taille de la grille", "Entrez la taille de la grille (6 à 12):", minvalue=6, maxvalue=12)
        if self.n is None:
            messagebox.showinfo("Erreur", "Vous devez entrer une taille de grille valide.")
            self.root.quit()

        self.grid = [[0] * self.n for _ in range(self.n)]

        self.border_frame = tk.Frame(self.root, bg='black', padx=30, pady=30)
        self.border_frame.grid(row=0, column=0, padx=(10, 0), pady=(0, 5), sticky='nsew')
        self.grid_window = tk.Frame(self.border_frame, bg='black')
        self.grid_window.pack(fill='both', expand=True)

        self.side_window = tk.Frame(self.root, bg='#323232')
        self.side_window.grid(row=0, column=1, sticky='ns', padx=5, pady=5)

        self.lower_window = tk.Frame(self.root, bg='#323232')
        self.lower_window.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.grid_data = [[0] * self.n for _ in range(self.n)]
        self.setup_side()
        self.setup_lower()
        self.setup_grid(self.grid_window)


    def load_grid(self):
        filename = tk.filedialog.askopenfilename(title="Ouvrir un fichier grille", filetypes=[("Text files", "*.txt")])
        if not filename:
            return

        with open(filename, "r") as file:
            lines = file.readlines()

        if len(lines) < self.n:
            messagebox.showerror("Erreur", "Le fichier ne contient pas suffisamment de données pour la grille et le texte chiffré.")
            return

        self.clear()

        for i in range(self.n):
            line = lines[i].strip()
            if len(line) != self.n:
                messagebox.showerror("Erreur", f"Erreur à la ligne {i + 1}: le nombre de caractères ne correspond pas à n.")
                return
            for j, char in enumerate(line):
                self.grid[i][j].config(bg='white' if char == '1' else '#808080')
                self.grid_data[i][j] = int(char)

        encrypted_text = lines[self.n].strip()
        self.load_ciphertext_into_grid(encrypted_text)

    def load_ciphertext_into_grid(self, ciphertext):
        chars = list(ciphertext)
        index = 0
        total_holes = sum(row.count(1) for row in self.grid_data)

        if len(chars) < total_holes:
            chars += ['X'] * (total_holes - len(chars))

        for i in range(self.n):
            for j in range(self.n):
                if self.grid_data[i][j] == 1:
                    if index < len(chars):
                        self.grid[i][j].config(text=chars[index])
                        index += 1

    def rotate_grid(self, grid):
        size = len(grid)
        new_grid = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                new_grid[j][size - 1 - i] = grid[i][j]
        return new_grid

    def is_valid_grid(self, grid):
        size = len(grid)
        current_grid = [row[:] for row in grid]

        for _ in range(3):
            new_grid = self.rotate_grid(current_grid)
            for i in range(size):
                for j in range(size):
                    if grid[i][j] == 1 and new_grid[i][j] == 1:
                        return False
            current_grid = new_grid

        return True

    def cipher(self):
        input_text = self.entry_clear.get("1.0", "end-1c")
        filtered_text = re.sub('[^a-zA-Z]', '', input_text)
        filtered_text = list(filtered_text.upper())

        rotations = 4
        index = 0

        for _ in range(rotations):
            if index >= len(filtered_text):
                self.read_grid_text()
                break

            for i in range(self.n):
                for j in range(self.n):
                    if self.grid_data[i][j] == 1 and self.grid[i][j].cget('text') == '':
                        if index < len(filtered_text):
                            self.grid[i][j].config(text=filtered_text[index], fg='black', font=('b'))
                            index += 1
                        else:
                            break

            if index < len(filtered_text):
                self.grid_data = self.rotate_grid(self.grid_data)
                self.update_grid_from_data()

    def read_grid_text(self):
        grid_text = ""
        for row in range(self.n):
            for col in range(self.n):
                label_text = self.grid[row][col].cget("text")
                grid_text += label_text

        self.entry_cipher.delete("1.0", "end")
        self.entry_cipher.insert("1.0", grid_text)

        return grid_text

    def update_grid_from_data(self):
        for i in range(self.n):
            for j in range(self.n):
                current_text = self.grid[i][j].cget("text")
                color = 'white' if self.grid_data[i][j] == 1 else '#808080'
                self.grid[i][j].config(bg=color, text=current_text)

    def decipher(self):
        extracted_letters = []
        total_holes = sum(row.count(1) for row in self.grid_data)
        chars_in_grid = sum(1 for i in range(self.n) for j in range(self.n) if self.grid_data[i][j] == 1 and self.grid[i][j].cget('text'))

        if chars_in_grid < total_holes:
            for i in range(self.n):
                for j in range(self.n):
                    if self.grid_data[i][j] == 1 and not self.grid[i][j].cget('text'):
                        self.grid[i][j].config(text='X')

        for _ in range(4):
            for i in range(self.n):
                for j in range(self.n):
                    if self.grid_data[i][j] == 1:
                        extracted_letters.append(self.grid[i][j].cget('text'))
            self.rotate_and_update()

        decrypted_message = ''.join(extracted_letters)
        self.entry_clear.delete("1.0", "end")
        self.entry_clear.insert("1.0", decrypted_message)

    def rotate_and_update(self):
        new_grid_data = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                new_grid_data[j][self.n - 1 - i] = self.grid_data[i][j]

        self.grid_data = new_grid_data
        for i in range(self.n):
            for j in range(self.n):
                color = 'white' if self.grid_data[i][j] == 1 else '#808080'
                self.grid[i][j].config(bg=color)

    def random_grid(self):
        attempt = 0
        max_attempts = 100
        while attempt < max_attempts:
            grid = [[0] * self.n for _ in range(self.n)]
            holes = set()
            while len(holes) < self.n * self.n // 4:
                row = random.randint(0, self.n - 1)
                col = random.randint(0, self.n - 1)
                if (row, col) not in holes:
                    grid[row][col] = 1
                    holes.add((row, col))
                    if not self.is_valid_grid(grid):
                        grid[row][col] = 0
                        holes.remove((row, col))
                if len(holes) == self.n * self.n // 4:
                    self.grid_data = grid
                    self.update_grid_from_data()
                    break
            attempt += 1

    def update_random_grid(self, grid):
        for row in range(self.n):
            for col in range(self.n):
                color = 'white' if grid[row][col] == 1 else '#808080'
                self.grid[row][col].config(bg=color)
                self.grid_data[row][col] = grid[row][col]

    def save_grid(self):
        with open("key.txt", "w") as file:
            for row in self.grid_data:
                line = ''.join(str(cell) for cell in row)
                file.write(line + '\n')
        messagebox.showinfo("Sauvegarde", "La clé de chiffrement a été sauvegardée avec succès.")

    def is_valid_grid(self, grid):
        size = self.n
        current_grid = [row[:] for row in grid]

        for _ in range(3):
            new_grid = self.rotate_grid(current_grid)
            for i in range(size):
                for j in range(size):
                    if grid[i][j] == 1 and new_grid[i][j] == 1:
                        return False
            current_grid = new_grid

        return True

    def setup_grid(self, frame):
        self.grid = []
        for row in range(self.n):
            row_labels = []
            for col in range(self.n):
                label = tk.Label(frame, bg='black', highlightbackground='blue', highlightcolor='blue', highlightthickness=1, padx=10, pady=10, borderwidth=1, relief="solid")
                label.bind("<Button-1>", lambda e, r=row, c=col: self.handle_click(r, c))
                label.grid(row=row, column=col, sticky='nsew')
                frame.grid_columnconfigure(col, weight=1)
                frame.grid_rowconfigure(row, weight=1)
                row_labels.append(label)
            self.grid.append(row_labels)
        if self.n % 2 != 0:
            self.grid[(self.n // 2)][(self.n // 2)].config(bg='#808080', state='disabled')

    def handle_click(self, row, col):
        if self.create_mode:
            label = self.grid[row][col]
            if label['bg'] == 'black':
                label.config(bg='white')
                self.grid_data[row][col] = 1
            else:
                label.config(bg='black')
                self.grid_data[row][col] = 0
            self.update_rotations(row, col)

    def update_rotations(self, row, col):
        positions = [(row, col), (col, self.n - 1 - row), (self.n - 1 - row, self.n - 1 - col), (self.n - 1 - col, row)]
        for r, c in positions:
            if (r, c) != (row, col):
                self.grid[r][c].config(bg='#808080')

    def toggle_create_mode(self):
        self.create_mode = not self.create_mode
        if not self.create_mode:
            for row in range(self.n):
                for col in range(self.n):
                    self.grid[row][col].config(bg='black')
                    if self.n % 2 != 0:
                        self.grid[(self.n // 2)][(self.n // 2)].config(bg='#808080', state='disabled')

    def clear(self):
        self.entry_clear.delete("1.0", "end")
        self.entry_cipher.delete("1.0", "end")

        for row in self.grid:
            for cell in row:
                cell.config(bg='#808080', text='')

        self.grid_data = [[0] * self.n for _ in range(self.n)]


    def setup_side(self):
        self.side_window.grid_columnconfigure(0, weight=1)

        self.side_window.grid_rowconfigure(0, weight=1)
        self.side_window.grid_rowconfigure(2, weight=1)

        button_frame = tk.Frame(self.side_window, bg='#323232')
        button_frame.grid(row=1, column=0, sticky='nsew')

        side_buttons = [('Load', self.load_grid), ('Random', self.random_grid), ('Save', self.save_grid), ('Create', self.toggle_create_mode)]
        for i, text in enumerate(side_buttons):
            btn = tk.Button(button_frame, text=text[0], command=text[1], bg='black', fg='white')
            btn.grid(row=i, column=0, sticky='ew', padx=10, pady=2)

    def setup_lower(self):
        self.lower_window.grid_columnconfigure(0, weight=1)
        self.lower_window.grid_columnconfigure(1, weight=1)
        self.lower_window.grid_columnconfigure(2, weight=1)
        self.lower_window.grid_columnconfigure(3, weight=1)

        self.entry_clear = tk.Text(self.lower_window, bg='#1E1E1E', fg='white', height=4)
        self.entry_clear.grid(row=0, column=0, columnspan=4, sticky='ew', padx=10, pady=10)

        self.entry_cipher = tk.Text(self.lower_window, bg='#1E1E1E', fg='white', height=4)
        self.entry_cipher.grid(row=2, column=0, columnspan=4, sticky='ew', padx=10, pady=10)

        lower_buttons = [
            ('Cipher', self.cipher),
            ('Decipher', self.decipher),
            ('Clear', self.clear),
            ('Clock', lambda: None)
        ]
        for i, (text, command) in enumerate(lower_buttons):
            btn = tk.Button(self.lower_window, text=text, command=command, bg='black', fg='white', width=10)
            btn.grid(row=1, column=i, sticky='ew', padx=10, pady=5)

def main():
    root = tk.Tk()
    app = Fleissner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
