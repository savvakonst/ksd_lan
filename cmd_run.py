import subprocess
#  cmd_write --addr 192.168.0.7 --lun 7 -N 0 -I WC01 -V 1 -S 1

#subprocess.call(["C:\Python27.14\python.exe","cmd_write.py ",'--addr 192.168.0.7 --lun 7 -N 0 -I WC01 -V 1 -S 1'])
def cmd_run(addr,lun,N,ID,VER,SER ):
    #subprocess.call(["C:\Python27.14\python.exe","cmd_write.py "]+'-h'.split(),shell=True)
    st=str('--addr '+addr+' --lun '+str(lun)+' -N '+str(N)+' -I '+ID+' -V '+VER+' -S '+SER+' ').split()
    proc=subprocess.Popen(["C:\Python27.14\python.exe","cmd_write.py "]+st,stdout=subprocess.PIPE)

    while True:
      line = proc.stdout.readline()
      if line != '':
        #the real code does filtering here
        None
        print  line.rstrip()
      else:
        break
    proc.kill()
    del(proc)
    exit()