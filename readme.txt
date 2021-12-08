中華民國統計資訊網 http://statdb.dgbas.gov.tw/pxwebP/Dialog/varval.asp?ma=PR0101A2M&ti=%AE%F8%B6O%AA%CC%AA%AB%BB%F9%B0%F2%A5%BB%A4%C0%C3%FE%BA[%B6%B5%A5%D8%B8s%AB%FC%BC%C6-%A4%EB&path=../PXfile/PriceStatistics/&lang=9&strList=L
爬的內容是物價指數
應該有滿足80分的標準

在config.ini中加入收尋條件
因查詢的資料只有一頁因此刪除中間讀取link的部分

SStart()查詢尚未儲存過的資料月份
因此之後內政部公布新的資料時就不會讀取到以前已經讀取過的部分

刪除大量沒用到的function

所有的function都有修改過但是都有加註記#

資料表欄位完全不一樣