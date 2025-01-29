import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime, timedelta
import threading

# Ваш API ключ
NEWS_API_KEY = '53bc8fb462aa4fdaad274fba9f2ecd98'
NEWS_API_URL = f'https://newsapi.org/v2/everything?q=депутаты OR законы OR президент OR госдума OR конституция&apiKey={NEWS_API_KEY}&language=ru&sortBy=publishedAt'

class NewsWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Новости")
        self.geometry("600x400")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.news_frame = ttk.Frame(self)
        self.news_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.news_label = tk.Label(self.news_frame, text="Загрузка...", font=("Arial", 14), wraplength=580, justify="left", bg="#ffffff", fg="#333333", anchor="w", padx=10, pady=10)
        self.news_label.pack(fill=tk.BOTH, expand=True)

        self.loading_label = ttk.Label(self, text="Загрузка...", foreground="blue")
        self.loading_label.pack_forget()

        # Запуск первого запроса к API и установка таймера для автоматического обновления
        self.fetch_and_display_news()
        self.after(5000, self.auto_update_news)

    def fetch_and_display_news(self):
        self.loading_label.pack()
        self.update_idletasks()

        threading.Thread(target=self._fetch_news).start()

    def _fetch_news(self):
        try:
            response = requests.get(NEWS_API_URL)
            if response.status_code == 200:
                news_data = response.json()
                self.display_news(news_data)
            else:
                self.news_label.config(text=f"Ошибка при получении новостей: {response.status_code}")
        except Exception as e:
            self.news_label.config(text=f"Ошибка: {str(e)}")
        finally:
            self.loading_label.pack_forget()

    def display_news(self, news_data):
        articles = news_data.get('articles', [])
        if articles:
            latest_article = articles[0]  # Берем самую первую (самую актуальную) новость
            title = latest_article.get('title', '') or "Заголовок не найден."
            description = latest_article.get('description', '') or "Описание не найдено."
            published_at = latest_article.get('publishedAt', '') or "Дата публикации не указана."
            source = latest_article.get('source', {}).get('name', '') or "Источник не указан."

            formatted_article = f"{title}\n\n{description}\n\nИсточник: {source}\nДата публикации: {published_at[:10]}"
            self.news_label.config(text=formatted_article)
        else:
            self.news_label.config(text="Новостей не найдено.")

    def auto_update_news(self):
        self.fetch_and_display_news()
        self.after(5000, self.auto_update_news)  # Устанавливаем таймер на следующее обновление через 5 секунд

if __name__ == "__main__":
    app = NewsWidget()
    app.mainloop()