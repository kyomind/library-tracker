#bin/bash
# 以crontab每日更新一次資料庫中的圖書狀態
source /home/kyo/.bashrc
source /home/kyo/library-tracker/wolf/bin/activate
python /home/kyo/library-tracker/crawler.py >> /home/kyo/update.log
deactivate