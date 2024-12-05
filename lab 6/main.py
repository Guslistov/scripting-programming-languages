import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
                             QComboBox, QTextEdit, QLineEdit, QSizePolicy)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

class DataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ данных")
        self.setGeometry(100, 100, 900, 600)

        self.df = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создание омпоновщиков
        self.layout_main = QVBoxLayout()

        self.layout_center = QHBoxLayout()
        self.layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()

        # Кнопка для загрузки данных
        self.button_load = QPushButton("Загрузить данные из CSV")
        self.button_load.clicked.connect(self.load_data)
        # Комбобокс для выбора типа графика
        self.combo_graph = QComboBox()
        self.combo_graph.addItems(['Линейный график', 'Гистограмма', 'Круговая диаграмма'])
        self.combo_graph.currentIndexChanged.connect(self.update_graph)
        # Кнопка для добавления данных
        self.label_date = QLabel("Date: ")
        self.input_date = QLineEdit("2023-04-10")
        self.label_value1 = QLabel("Value 1: ")
        self.input_value1 = QLineEdit("0")
        self.label_value2 = QLabel("Value 2: ")
        self.input_value2 = QLineEdit("0")
        self.button_add_value = QPushButton("Добавить значение")
        self.button_add_value.clicked.connect(self.add_data)
        # Поле для отображения статистики
        self.label_stats = QLabel("Статистика: ")
        self.text_stats = QTextEdit()
        self.text_stats.setReadOnly(True)

        # Создание области для графика matplotlib
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.msg = QLabel("")

        # Компоновка
        self.layout_left.addWidget(self.button_load)
        self.layout_left.addWidget(self.combo_graph)

        self.layout_left.addWidget(self.label_date)
        self.layout_left.addWidget(self.input_date)
        self.layout_left.addWidget(self.label_value1)
        self.layout_left.addWidget(self.input_value1)
        self.layout_left.addWidget(self.label_value2)
        self.layout_left.addWidget(self.input_value2)
        self.layout_left.addWidget(self.button_add_value)

        self.layout_left.addWidget(self.label_stats)
        self.layout_left.addWidget(self.text_stats)

        self.layout_right.addWidget(self.canvas)
        
        self.layout_center.addLayout(self.layout_left)
        self.layout_center.addLayout(self.layout_right)

        self.layout_main.addLayout(self.layout_center)
        self.layout_main.addWidget(self.msg)
        
        self.central_widget.setLayout(self.layout_main)
        
    def load_data(self):
        try:
            file_path = "sample_data.csv"
            self.df = pd.read_csv(file_path)
            # Преобразование столбца Date в datetime и затем в строковый формат
            self.df['Date'] = pd.to_datetime(self.df['Date']).dt.strftime('%Y-%m-%d')
            self.update_graph()
            self.update_stats()
        except Exception as e:
            self.msg.setText(f"Ошибка обновления графика: {str(e)}")
    
    def add_data(self):

        try:
            date_object = datetime.strptime(self.input_date.text(), "%Y-%m-%d")
            date_object.date()

            date_object = str(date_object)[:10]
            print(date_object)
        except ValueError:
            self.msg.setText("Неверный формат даты. Требуется %Y-%m-%d")
            return None

        try:
            value1 = float(self.input_value1.text())
            value2 = float(self.input_value2.text())
            date = str(date_object)
            
            row = pd.DataFrame({
                'Date': [date],
                'Value1': [value1],
                'Value2': [value2],
                'Category': ['Ручной ввод']
            })

            self.df = pd.concat([self.df, row], ignore_index=True)

            self.update_graph()
            self.update_stats()
            self.msg.setText("")

        except Exception as e:
            self.msg.setText(f"Ошибка добавления данных: {str(e)}")

    def update_graph(self):
        graph_type = self.combo_graph.currentText()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        try:
            if graph_type == "Линейный график":
                ax.plot(self.df['Date'], self.df['Value1'])
                ax.set_title('Линейный график: Date и Value1')
                ax.set_xlabel('Date')
                ax.set_ylabel('Value1')
                dates = self.df['Date'].unique()
                ax.set_xticks(dates[::len(dates)//6]) 
            elif graph_type == "Гистограмма":
                ax.bar(self.df['Date'], self.df['Value2'])
                ax.set_title('Гистограмма: Date и Value2')
                ax.set_xlabel('Date')
                ax.set_ylabel('Value2')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right') # Поворот подписей дат
                dates = self.df['Date'].unique()
                ax.set_xticks(dates[::len(dates)//6]) 
            elif graph_type == "Круговая диаграмма":
                ax.set_title('Круговая диаграмма: Category')
                category_counts = self.df['Category'].value_counts()
                ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')       

            self.figure.tight_layout()
            self.canvas.draw()
            self.msg.setText("")

        except Exception as e:
            self.msg.setText(f"Ошибка обновления графика: {str(e)}")
    
    def update_stats(self):
        if self.df is not None:
            stats = f"Статистика:\n\n"
            stats += f"Количество строк: {len(self.df)}\n"
            stats += f"Количество столбцов: {len(self.df.columns)}\n\n"
            
            for column in self.df.columns:
                if pd.api.types.is_numeric_dtype(self.df[column]):
                    stats += f"{column}:\n"
                    stats += f"  Минимум: {self.df[column].min()}\n"
                    stats += f"  Максимум: {self.df[column].max()}\n"
                    stats += f"  Среднее: {self.df[column].mean():.2f}\n\n"
            
            self.text_stats.setText(stats)

def main():
    app = QApplication(sys.argv)
    window = DataApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()