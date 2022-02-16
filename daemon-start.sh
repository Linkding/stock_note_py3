stop() {
    for i in ` ps aux|grep runserver|grep -v grep|awk '{print $2}'`
    do
    kill -9 $i
    done
}
start() {
    nohup env/bin/python stock_notes_pro.py runserver > log.log 2>&1 &
}
status(){
    ps aux|grep runserver|grep -v grep
}
get_stock_daily(){
    curl -X POST http://127.0.0.1:8888/todo/api/v1.0/tasks/auto_get_stock > /tmp/curl.log
}

case "$1" in
    start)
        start
    ;;
    stop)
        stop
    ;;
    status)
        status
    ;;
    3)
        get_stock_daily
    ;;
    *)
        echo "Usage: {start|stop|restart}"
        exit 1
esac
