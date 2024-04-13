from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
import requests
import json

class Book:
    def __init__(self, book_id: str, title: str, author: str) -> None:
        self.book_id = book_id
        self.title = titleauthor
        self.author =

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        return Book(
            book_id=data.get('id', ''),
            title=data.get('title', ''),
            author=data.get('author', '')
        )

    @staticmethod
    def from_list(data: list) -> 'Book':
        return Book(
            book_id=str(data[0]),
            title=data[1],
            author=data[2]
        )

class MyBoxLayout(BoxLayout):
    def close_app(self):
        App.get_running_app().stop()

    def add_book(self):
        book_id = self.ids.id_input.text.strip()
        title = self.ids.title_input.text.strip()
        author = self.ids.author_input.text.strip()
        if not book_id or not title or not author:
            self.ids.message_label.text = "Please enter valid book ID, title, and author."
            return

        payload = {"id": book_id, "title": title, "author": author}
        try:
            response = requests.post("http://192.168.1.42:5000/books", json=payload)
            if response.status_code == 200:
                self.ids.id_input.text = ''
                self.ids.title_input.text = ''
                self.ids.author_input.text = ''
                self.get_all_books()
                self.ids.message_label.text = "Book added successfully."
            else:
                self.ids.message_label.text = "Failed to add book. Please try again."
        except requests.RequestException as e:
            print(f"Error: {e}")
            self.ids.message_label.text = "Failed to add book. Please try again."

    def update_book(self):
        book_id = self.ids.id_input.text.strip()
        title = self.ids.title_input.text.strip()
        author = self.ids.author_input.text.strip()
        if not book_id or not title or not author:
            self.ids.message_label.text = "Please enter valid book ID, title, and author."
            return

        payload = {"id": book_id, "title": title, "author": author}
        try:
            response = requests.put(f"http://192.168.1.42:5000/books/{book_id}", json=payload)
            if response.status_code == 200:
                self.ids.id_input.text = ''
                self.ids.title_input.text = ''
                self.ids.author_input.text = ''
                self.get_all_books()
                self.ids.message_label.text = "Book updated successfully."
            else:
                self.ids.message_label.text = "Failed to update book. Please try again."
        except requests.RequestException as e:
            print(f"Error: {e}")
            self.ids.message_label.text = "Failed to update book. Please try again."

    def delete_book(self):
        book_id = self.ids.id_input.text.strip()
        if not book_id:
            self.ids.message_label.text = "Please enter a valid book ID."
            return

        try:
            response = requests.delete(f"http://192.168.1.42:5000/books/{book_id}")
            if response.status_code == 200:
                self.ids.id_input.text = ''
                self.ids.title_input.text = ''
                self.ids.author_input.text = ''
                self.get_all_books()
                self.ids.message_label.text = "Book deleted successfully."
            else:
                self.ids.message_label.text = "Failed to delete book. Please try again."
        except requests.RequestException as e:
            print(f"Error: {e}")
            self.ids.message_label.text = "Failed to delete book. Please try again."

    def get_all_books(self):
        try:
            response = requests.get("http://192.168.1.42:5000/books")
            if response.status_code == 200:
                data = response.json()
                books_data = data.get("books", [])
                books = []
                for book_data in books_data:
                    if isinstance(book_data, dict):
                        book = Book.from_dict(book_data)
                    elif isinstance(book_data, list) and len(
                            book_data) == 3:
                        book = Book.from_list(book_data)
                    else:
                        print(f"Invalid book data: {book_data}")
                        continue
                    books.append({'text': f'[Title: {book.title} , Author: {book.author} ]'})
                self.ids.rv.data = books
            else:
                self.ids.message_label.text = "Failed to retrieve books. Please try again."
        except requests.RequestException as e:
            print(f"Error: {e}")
            self.ids.message_label.text = "Failed to retrieve books. Please try again."

    def get_specific_book(self):
        book_id = self.ids.get_specific_input.text
        if not book_id:
            self.ids.message_label.text = "Please enter a valid book ID."
            return
        try:
            response = requests.get(f"http://192.168.1.42:5000/books/{book_id}")
            if response.status_code == 200:
                book_data = response.json()
                rv_data = [{'text': json.dumps(book_data)}]
                self.ids.rv.data = rv_data
                self.ids.message_label.text = "Book retrieved successfully."
            else:
                self.ids.message_label.text = "Book with the given ID not found."
                print("Error: Book with the given ID not found.")
        except requests.RequestException as e:
            print(f"Error: {e}")
            self.ids.message_label.text = "Failed to retrieve book. Please try again."
            print("Error: Failed to retrieve book. Please try again.")


class RV(RecycleView):
    pass

class CustomLabel(Label):
    pass

class MyApp(App):
    def build(self):
        Window.clearcolor = (0.7, 0.7, 0.8, 1)
        return MyBoxLayout()

if __name__ == '__main__':
    MyApp().run()
