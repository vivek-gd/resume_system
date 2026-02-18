import traceback
try:
    import app
    print('Import successful')
except Exception as e:
    traceback.print_exc()