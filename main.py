__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import server

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8000)