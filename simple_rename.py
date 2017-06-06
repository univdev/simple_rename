import os
import sys
from app import SimpleRename

app = SimpleRename();

def main():
    app.dir = input("설정하실 파일들이 들어있는 경로를 입력해주세요: ")
    app.start();

main();
