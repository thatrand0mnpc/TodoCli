"""Manages cli argument parser for the application."""
import sys
from argparse import ArgumentParser

from todocli import views


class App:
    """Argument parser class. Create instance of this class to start the application."""

    def run(self) -> None:
        """Entry point for the argument parser class."""
        # main argument parser
        parser = ArgumentParser(
            description='TodoCli, a simple cli todo utility.',
            usage='python todo.py [-h] <command> [<args>]'
        )
        # list of possible commands
        parser.add_argument('command', type=str, choices=[
                            'list', 'add', 'update', 'check', 'uncheck', 'delete'])
        # check first positional argument
        args = parser.parse_args(sys.argv[1:2])
        # call corresponding instance method if available
        getattr(self, args.command)()

    def list(self) -> None:
        """Argument parser and action for listing todo items."""
        parser = ArgumentParser(description='List todo items.',
                                usage='python todo.py list [-h] [id ...]')
        parser.add_argument('id', nargs='*', type=int,
                            default=list(), help='list by id')
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        if args.id:
            if len(args.id) == 1:  # one item
                views.list_todo(args.id[0])
            else:  # main items
                views.list_todo(args.id)
        else:  # all items
            views.list_todo()

    def add(self) -> None:
        """Argument parser and action for adding todo items."""
        parser = ArgumentParser(description='Add todo item.',
                                usage='python todo.py add [-h] title [title ...]')
        parser.add_argument('title', nargs='+', type=str, help='todo title')
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        views.add_todo(' '.join(args.title))

    def update(self) -> None:
        """Argument parser and action for updating todo items."""
        parser = ArgumentParser(description='Update todo item.',
                                usage='python todo.py update [-h] id title [title ...]')
        parser.add_argument('id', type=int, help='update by id')
        parser.add_argument('title', nargs='+', type=str, help='update title')
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        views.update_todo(index=args.id, title=' '.join(args.title))

    def _check_uncheck_helper(self, msg: str, check: bool) -> None:
        """Helper argument parser and action for checking & un-checking todo items."""
        usage = f'python todo.py {msg.replace("-", "").lower()[:-1]} [-h] [-a] [id ...]'
        parser = ArgumentParser(description=f'{msg} todo item.',
                                usage=usage)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('id', nargs='*', type=int,
                           default=list(), help=f'{msg.lower()} by id')
        group.add_argument('-a', '--all', action='store_true',
                           help=f'{msg.lower()} all')
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        if args.id:
            if len(args.id) == 1:  # one item
                views.update_todo(index=args.id[0], check=check)
            else:  # many items
                views.update_todo_check_many(indexes=args.id, check=check)
        elif args.all:  # all items
            views.update_todo_all(check)

    def check(self) -> None:
        """Argument parser and action for checking todo items."""
        self._check_uncheck_helper('Checks', True)

    def uncheck(self) -> None:
        """Argument parser and action for un-checking todo items."""
        self._check_uncheck_helper('Un-checks', False)

    def delete(self) -> None:
        """Argument parser and action for deleting todo items."""
        parser = ArgumentParser(description='Delete todo item.',
                                usage='python todo.py delete [-h] [-a] [id ...]')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('id', nargs='*', type=int,
                           default=list(), help='delete by id')
        group.add_argument(
            '-a', '--all', action='store_true', help='delete all')
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        if args.id:
            if len(args.id) == 1:  # one item
                views.delete_todo(args.id[0])
            else:  # many items
                views.delete_todo(args.id)
        elif args.all:  # all items
            views.delete_todo_all()
