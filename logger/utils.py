def clear_empty_item(arr: list[str]) -> list[str]:
    """Удаляет пустые элементы из списка.

    Примеры:
    - [''] -> []
    - ['name', ''] -> ['name']
    """
    return [item for item in arr if item != '']


def subtract_sets(set1: set[str], set2: set[str]) -> set[str]:
    result = set()
    # Удаляем дочерние элементы и элементы из set2
    for item in set1:
        is_child = False
        for parent in set2:
            if item.startswith(parent + '.'):
                is_child = True
                break
        if not is_child and item not in set2:
            result.add(item)

    # Удаляем родительские элементы, если их дочерние элементы есть в set2
    to_remove = set()  # Множество для хранения элементов, которые нужно удалить
    for item in set2:
        if '.' in item:
            item_list = item.split('.')
            item_list.pop()
            for _ in range(len(item_list)):
                parent = '.'.join(item_list)
                if parent in result:
                    to_remove.add(parent)
                    try:
                        item_list.pop()
                    except IndexError:
                        pass

    result -= to_remove
    return result



# Пример 1
# set1 = {'api.routers.routers', 'bg.routers', 'api', 'bg.services', 'api.routers', 'logger', 'bg'}
# set2 = {'bg'}
# result = subtract_sets(set1, set2)

