python node.py DC1 5000 #  Start DC1 and connect to DC2 and DC3
python node.py DC2 5001 DC1 5000  #  Start DC2 and connect to DC1 and DC3
python node.py DC3 5002 DC1 5001 DC2 5001 #  Start DC3 and connect to DC1 and DC2
python node.py DC4 5003 DC1 5002