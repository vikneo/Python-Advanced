"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
from pprint import pprint
import os
import re
import itertools
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")

current_dir = os.path.dirname(__file__)
file_name = os.path.join(current_dir, "walk_log_4.txt")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    with open(path_to_log_file, 'r') as file:
        bin_tree = {}
        file_list = file.readlines()
        _root_num = int(re.search(r'[0-9]+', file_list[0]).group())
        _root = BinaryTreeNode(val=_root_num, left=None, right=None)
        # TODO каждую новую ноду надо сразу помещать и bin_tree
        for line in file_list:
            if line.startswith("INFO"):
                node_num = int(re.search(r'[0-9]+', line).group())
                bin_tree[node_num] = BinaryTreeNode(node_num)
                # TODO нужна проверка наличия ноды в bin_tree, в этом случае её не создаём
            elif line.startswith("DEBUG"):
                if "left" in line:
                    left = int(re.search(r'[0-9]+', line.split('.')[1]).group())
                    bin_tree[node_num] = BinaryTreeNode(
                        val=node_num, left=BinaryTreeNode(left), right=None
                    )
                elif "right" in line:
                    right = int(re.search(r'[0-9]+', line.split('.')[1]).group())
                    bin_tree[node_num] = BinaryTreeNode(
                        val=node_num, left=BinaryTreeNode(left), right=BinaryTreeNode(right)
                    )

        return _root
# TODO "Связанного" дерева не получилось, перед созданием новой "ноды", надо учесть, что нода уже может существовать,
#  в таком случае надо использовать её вместо создания новой.


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filemode='w',
        format="%(levelname)s:%(message)s",
        filename=file_name,
    )

    root = get_tree(7)
    walk(root)
    print(f"Корень восстановленного дерева: {restore_tree(file_name)}")
