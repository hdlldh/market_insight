WORK_DIR=/home/donglin/Workspace/market_insight
cd $WORK_DIR
mkdir -p $WORK_DIR"/data"
mkdir -p $WORK_DIR"/logs"
DATA_FILE=$WORK_DIR"/data/data_$(date +"%Y-%m-%d").csv"
rm $DATA_FILE
LOG_FILE=$WORK_DIR"/logs/info_$(date +"%Y-%m-%d").log"
rm $LOG_FILE
scrapy crawl yahoo_stocks \
	--output=$DATA_FILE \
	--loglevel=INFO \
	--logfile=$LOG_FILE

