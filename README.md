# jetson_oled_ssd1306

<b> ip.py final code
sudo nano /etc/systemd/system/ip-display.service

``` bash
[Unit]
Description=IP Display OLED Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/donkey/ip.py
Restart=always
User=donkey
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload
sudo systemctl restart ip-display.service

result
oled->  wan0 : 192.168.0.159
