# coding: utf-8
import sys
from logic.train import train

def main():
    args = sys.argv

    if(len(args) < 2):
        print('引数が足りません')
        return 0
    
    t = args[1]
    if(t == 'train'):
        print('train')
    elif(t == 'eval'):
        print('eval')
    elif(t == 'pred'):
        print('predict')
    else:
        print('Invalid args')
    

if __name__ == "__main__":
    main()
