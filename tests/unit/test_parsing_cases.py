import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.parsing import Parsing

base = os.path.dirname(__file__)

def _write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1) Missing file -> default
p_missing = Parsing(os.path.join(base, 'missing.json'))
res = p_missing.load_json_tree(default='DEFAULT', verbose=False)
assert res == 'DEFAULT', f"Expected DEFAULT for missing file, got {res!r}"
print('Test 1 passed: missing file returns default')

# 2) Invalid JSON -> default
invalid_path = os.path.join(base, 'invalid.json')
_write_file(invalid_path, '{ invalid json: }')
p_invalid = Parsing(invalid_path)
res = p_invalid.load_json_tree(default='DEFAULT', verbose=False)
assert res == 'DEFAULT', f"Expected DEFAULT for invalid json, got {res!r}"
print('Test 2 passed: invalid JSON returns default')

# 3) Path is a directory -> default
dir_path = os.path.join(base, 'testdir')
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
p_dir = Parsing(dir_path)
res = p_dir.load_json_tree(default='DEFAULT', verbose=False)
assert res == 'DEFAULT', f"Expected DEFAULT for directory path, got {res!r}"
print('Test 3 passed: directory path returns default')

# 4) Wrong structure (list) -> default
weird_path = os.path.join(base, 'weird.json')
_write_file(weird_path, json.dumps([1,2,3]))
p_weird = Parsing(weird_path)
res = p_weird.load_json_tree(default='DEFAULT', verbose=False)
assert res == 'DEFAULT', f"Expected DEFAULT for wrong structure, got {res!r}"
print('Test 4 passed: wrong structure returns default')

# 5) Good file -> returns QuestionNode with value
good_path = os.path.join(base, 'good.json')
_write_file(good_path, json.dumps({"value":"Root","yes":None,"no":None}))
p_good = Parsing(good_path)
root = p_good.load_json_tree(default=None, verbose=False)
assert root is not None and getattr(root, 'value', None) == 'Root', f"Expected root with value 'Root', got {root!r}"
print('Test 5 passed: good file returns root node with value Root')

# cleanup
for f in (invalid_path, weird_path, good_path):
    try:
        os.remove(f)
    except Exception:
        pass
try:
    os.rmdir(dir_path)
except Exception:
    pass

print('All parsing cases passed (asserts).')
