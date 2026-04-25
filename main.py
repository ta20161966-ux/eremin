import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Настройки ---
JSON_FILE = "movies.json"

# --- Класс приложения ---
class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x500")

        # Загрузка данных из JSON
        self.movies = self.load_movies()

        # --- Создание виджетов ---
        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(root, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(root, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(root, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения фильмов
        self.columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        
        # Настройка заголовков и ширины колонок
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, minwidth=0, width=180)
        
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по году:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.filter_year = tk.Entry(root)
        self.filter_year.grid(row=7, column=1, padx=5, pady=5)

        self.filter_btn = tk.Button(root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=8, column=0, columnspan=2)

        # Кнопка очистки фильтра
        self.clear_btn = tk.Button(root, text="Очистить фильтр", command=self.clear_filter)
        self.clear_btn.grid(row=9, column=0, columnspan=2)

        # Заполнение таблицы при запуске
        self.update_tree()

    # --- Логика работы с данными ---
    def load_movies(self):
        """Загружает фильмы из файла JSON."""
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_movies(self):
        """Сохраняет фильмы в файл JSON."""
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def add_movie(self):
        """Добавляет фильм после проверки данных."""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        
        year_str = self.year_entry.get().strip()
        
        rating_str = self.rating_entry.get().strip()

        # Проверка на пустые поля
        if not title or not genre or not year_str or not rating_str:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

         # Проверка года
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        
         # Проверка рейтинга
        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
            
            year = int(year_str)
            
            # Добавление в список и обновление таблицы
            self.movies.append({
                "title": title,
                "genre": genre,
                "year": year,
                "rating": rating
            })
            
            self.save_movies()
            self.update_tree()
            
            # Очистка полей после добавления
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)
            
            messagebox.showinfo("Успех", "Фильм добавлен!")
            
         except ValueError:
             messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")

    def update_tree(self):
        """Обновляет данные в таблице."""
         for i in self.tree.get_children():
             self.tree.delete(i)
         
         for movie in self.movies:
             self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def apply_filter(self):
         """Применяет фильтры по жанру и году."""
         filtered_movies = self.movies.copy()
         
         genre_filter = self.filter_genre.get().strip().lower()
         if genre_filter:
             filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]
         
         year_filter = self.filter_year.get().strip()
         if year_filter.isdigit():
             filtered_movies = [m for m in filtered_movies if m["year"] == int(year_filter)]
         
         # Обновление таблицы с отфильтрованными данными
         for i in self.tree.get_children():
             self.tree.delete(i)
         
         for movie in filtered_movies:
             self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def clear_filter(self):
         """Очищает фильтры и показывает все фильмы."""
         self.filter_genre.delete(0, tk.END)
         self.filter_year.delete(0, tk.END)
         self.update_tree()


# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
