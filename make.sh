# ls log  | sort -t "." -k3n |awk '{print "log/"$0}' > data.lst
python3 process.py
head -n5000 out > out.txt
