// Имитация зависшего сервиса
function handle(r) {
    setTimeout(function () {
        r.headersOut['Content-Type'] = 'application/json';
        r.return(200, '{"status": "slow", "endpoint": "slow", "delay": "5000ms"}');
    }, 5000);
}

export default { handle };
