import os
from pathlib import Path

#
# def _validate_existing(base_path: Path, seq):
#
#     # Обходим директории и файлы
#     for file_name in seq:
#         result = []
#         file_name = file_name.split('/')[-1]
#         for root, dirs, filenames in os.walk(base_path):
#             # Исключаем папку .venv из дальнейшего обхода
#             if '.venv' in dirs:
#                 dirs.remove('.venv')
#
#             # Ищем файл с указанным именем
#             for f in filenames:
#                 if file_name is None or os.path.basename(f).split('/')[-1] == file_name:
#                     result.append(os.path.join(root, f))
#


_validate_existing(Path('/home/pavel/PycharmProjects/fastapi_faststream_apscheduler_logger'), ['bg/app.py', 'api.py'])
