## 專案結構

```
main.py                 程式進入點
kana_bot/
  app.py                主流程（登入 → 練習 → 詢問是否再練一次）
  browser.py            瀏覽器操作（登入、開始練習、暫停並退出）
  session.py            自動作答邏輯
  settings.py           終端機設定輸入
  config.py             網址、等級延遲等常數
  kana_map.py           假名對照表
build_kana_bot.sh       mac 編譯成執行檔（輸出到 dist/kana_bot）
requirements.txt
```

## 安裝

先裝 python (https://www.python.org/downloads/) \
打開 terminal (or cmd) 輸入 python --version (mac 用 python3 --version)，如有顯示代表下載成功了\
在 terminal (or cmd) 輸入 pip --version (mac 用 pip3 --version)，如有顯示代表 pip 安裝成功了\
在 terminal (or cmd) 輸入 pip install -r requirements.txt (mac 用 pip3 install -r requirements.txt)，如果怕髒自己開venv\
在 terminal (or cmd) 輸入 playwright install

## 使用

在專案資料夾輸入 python main.py (mac 用 python3 main.py)\
在 terminal 輸入等級、時間、正確率\
在瀏覽器登入後，選擇各項設定按開始練習他就自動開始了\
時間到之後（若設定少於 10 分鐘會自動按「暫停並退出」），回到 terminal 會詢問是否要再練一次，輸入 y 會重新詢問設定並開始新的練習，輸入 n 結束

## 編譯 (mac)

build_kana_bot.sh可以留給mac的朋友們自己編譯\
輸入這個\
chmod +x build_kana_bot.sh\
./build_kana_bot.sh\
執行檔會在 dist/kana_bot
