"""Views for todo model."""
from typing import Iterator

from todocli.base import Base, Session, engine
from todocli.models import Todo

Base.metadata.create_all(engine)  # create tables for models


def add_todo(title: str, check: bool = False) -> None:
    """Add todo items.

    :param title: todo title
    :type title: str
    :param check: todo status, defaults to False
    :type check: bool, optional
    """
    todo = Todo(title, check)
    session = Session()
    session.add(todo)
    session.commit()
    session.close()


def list_todo(indexes: int | list[int] | None = None) -> None:
    """List todo items.

    :param indexes: todo item id, defaults to None
    :type indexes: int | list[int], optional
    """
    session = Session()
    if isinstance(indexes, int):  # one item
        todo = session.query(Todo).get(indexes)
        if todo:
            print(todo)
        else:
            print(f'{indexes} not found!!')
    else:
        if isinstance(indexes, list):  # many items
            todos: Iterator[Todo] = session.query(
                Todo).filter(Todo.id.in_(indexes)).all()
        else:  # all items
            todos: Iterator[Todo] = session.query(Todo).all()
        print('\nid | title | status')
        print('-------------------')
        for todo in todos:
            print(todo)
        print('\n')
    session.close()


def update_todo(index: int, title: str | None = None, check: bool | None = None) -> None:
    """Update todo items.

    :param index: todo item id
    :type index: int
    :param title: todo title, defaults to None
    :type title: str, optional
    :param check: todo status, defaults to None
    :type check: bool, optional
    """
    session = Session()
    todo: Todo = session.query(Todo).get(index)
    if todo:
        if title is not None:
            todo.title = title
        if check is not None:
            todo.check = check
        session.commit()
    else:
        print(f'{index} not found!!')
    session.close()


def update_todo_check_many(indexes: list[int], check: bool | None = None) -> None:
    """Update status of many todo items.

    :param indexes: todo item id
    :type indexes: list[int]
    :param check: todo status, defaults to None
    :type check: bool, optional
    """
    session = Session()
    if check is not None:
        todos: Iterator[Todo] = session.query(
            Todo).filter(Todo.id.in_(indexes)).all()
        for todo in todos:
            todo.check = check
        session.commit()
    session.close()


def update_todo_all(check: bool | None = None) -> None:
    """Update status of all todo items.

    :param check: todo status, defaults to None
    :type check: bool, optional
    """
    session = Session()
    if check is not None:
        todos: Iterator[Todo] = session.query(Todo).all()
        for todo in todos:
            todo.check = check
        session.commit()
    session.close()


def delete_todo(indexes: int | list[int]) -> None:
    """Delete todo items.

    :param indexes: todo item id
    :type indexes: int | list[int]
    """
    session = Session()
    if isinstance(indexes, int):
        todo: Todo = session.query(Todo).get(indexes)
        if todo:
            session.delete(todo)
            session.commit()
        else:
            print(f'{indexes} not found!!')
    else:
        todos: Iterator[Todo] = session.query(
            Todo).filter(Todo.id.in_(indexes)).all()
        if todos:
            for todo in todos:
                session.delete(todo)
            session.commit()
        else:
            print(f'{indexes} not found!!')
    session.close()


def delete_todo_all() -> None:
    """Delete all todo items."""
    session = Session()
    session.query(Todo).delete()
    session.commit()
    session.close()
