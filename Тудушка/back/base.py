from typing import List
from models import TaskScheme

tasks: List[TaskScheme] = [
    TaskScheme(index=1, task="Сделать домашнее задание"),
    TaskScheme(index=2, task="Купить продукты"),
    TaskScheme(index=3, task="Позвонить бабушке", done=True),
]
