#### 這個應用是**python製作的CLI**用來使用Selenium操作Chrome，自動化操作"新北市復康巴士訂車"。

**動機**:給需要讓家人訂車的人方便使用

有build一個**Windows執行檔**可以供大家試試。

**這個小程式需要編輯裡面的文字檔(ycbus_data.txt):**

***********************

姓名代號=徐明(姓名前後字，例如:徐小明)

編號=A12345(身分證後5碼，開頭加上A)

搭車日期=11/11(MM/DD)

去程搭車時間=07:30(HH:mm,可參照"bus_time.txt")

回程搭車時間=13:30(HH:mm,可參照"bus_time.txt")

去程_上車_縣市=a("a"=新北市,b=台北市,c=桃園市,d=基隆市)

去程_上車_區域=萬里(可參照"ycbus_addr.txt")

去程_上車_地址=萬里地址

去程_下車_縣市=b

去程_下車_區域=信義

去程_下車_地址=信義地址

message=留言訊息

回程_上車_縣市=c

回程_上車_區域=龜山

回程_上車_地址=龜山地址

回程_下車_縣市=b

回程_下車_區域=大安

回程_下車_地址=大安地址

****************************

最後在DOS視窗

確認使用完瀏覽器,請輸入 "y" Enter離開此程式與瀏覽器