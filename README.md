# process_monitor
Use python 3.9

## Running
Install dependency
``` bash
pip install -r requirements.txt
```

Add full path to process file and monitoring interval
``` bash
# Example
FILE=C:/Users/Administrator/GolandProjects/test/main.exe
INTERVAL=4m
```
Run .py script from root of repository
``` bash
python3 main.py
```

## Workflow
#### After starting, the script starts the selected process, outputs its indicators to the console and writes to a file reports/*.csv at a specified interval
